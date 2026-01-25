#!/usr/bin/env python3
"""AI分析引擎模块"""

import os
import logging
import google.generativeai as genai
from openai import OpenAI
import pandas as pd

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI分析器"""
    
    def __init__(self):
        # 初始化Google Gemini Pro
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if google_api_key:
            genai.configure(api_key=google_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        else:
            self.gemini_model = None
        
        # 初始化OpenAI GPT-4o
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
        else:
            self.openai_client = None
    
    def analyze_with_gemini(self, stock_data, symbol):
        """
        使用Google Gemini Pro分析股票数据
        
        Args:
            stock_data: 股票数据DataFrame
            symbol: 股票代码
            
        Returns:
            dict: 分析结果
        """
        if not self.gemini_model:
            logger.warning("Google Gemini Pro未配置")
            return {}
        
        try:
            # 准备数据摘要
            data_summary = self._prepare_data_summary(stock_data, symbol)
            
            # 构建提示词
            prompt = f"""你是一名专业的股票分析师，擅长使用威科夫理论分析市场。
            请分析以下股票的1分钟K线数据，重点关注：
            1. 供求关系分析
            2. 识别Spring（弹簧效应）、UT（上冲回落）、LPS（最后支撑点）等关键行为
            3. 主力吸筹/派发痕迹
            4. 短期走势预测
            
            股票数据：
            {data_summary}
            
            请提供详细的分析报告，包括：
            - 关键行为识别
            - 市场结构分析
            - 操作建议
            - 风险提示
            """
            
            # 生成分析
            response = self.gemini_model.generate_content(prompt)
            analysis = response.text
            
            logger.info(f"Gemini Pro分析完成: {symbol}")
            return {
                'engine': 'Gemini Pro',
                'analysis': analysis,
                'timestamp': pd.Timestamp.now()
            }
            
        except Exception as e:
            logger.error(f"Gemini Pro分析失败: {e}")
            return {}
    
    def analyze_with_gpt4o(self, stock_data, symbol):
        """
        使用OpenAI GPT-4o分析股票数据
        
        Args:
            stock_data: 股票数据DataFrame
            symbol: 股票代码
            
        Returns:
            dict: 分析结果
        """
        if not self.openai_client:
            logger.warning("OpenAI GPT-4o未配置")
            return {}
        
        try:
            # 准备数据摘要
            data_summary = self._prepare_data_summary(stock_data, symbol)
            
            # 构建提示词
            prompt = f"""你是一名专业的股票分析师，擅长使用威科夫理论分析市场。
            请分析以下股票的1分钟K线数据，重点关注：
            1. 供求关系分析
            2. 识别Spring（弹簧效应）、UT（上冲回落）、LPS（最后支撑点）等关键行为
            3. 主力吸筹/派发痕迹
            4. 短期走势预测
            
            股票数据：
            {data_summary}
            
            请提供详细的分析报告，包括：
            - 关键行为识别
            - 市场结构分析
            - 操作建议
            - 风险提示
            """
            
            # 生成分析
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "你是一名专业的股票分析师，擅长使用威科夫理论分析市场。"},
                    {"role": "user", "content": prompt}
                ]
            )
            analysis = response.choices[0].message.content
            
            logger.info(f"GPT-4o分析完成: {symbol}")
            return {
                'engine': 'GPT-4o',
                'analysis': analysis,
                'timestamp': pd.Timestamp.now()
            }
            
        except Exception as e:
            logger.error(f"GPT-4o分析失败: {e}")
            return {}
    
    def _prepare_data_summary(self, stock_data, symbol):
        """
        准备数据摘要
        
        Args:
            stock_data: 股票数据DataFrame
            symbol: 股票代码
            
        Returns:
            str: 数据摘要
        """
        if stock_data.empty:
            return f"股票代码: {symbol}\n无数据"
        
        # 计算关键指标
        latest_price = stock_data['close'].iloc[-1]
        open_price = stock_data['open'].iloc[0]
        high_price = stock_data['high'].max()
        low_price = stock_data['low'].min()
        volume = stock_data['volume'].sum()
        
        # 计算涨跌幅
        change_percent = ((latest_price - open_price) / open_price) * 100
        
        # 最近几小时的走势
        recent_hours = min(4, len(stock_data) // 60)
        recent_trend = []
        for i in range(recent_hours):
            start_idx = max(0, len(stock_data) - (i+1)*60)
            end_idx = max(0, len(stock_data) - i*60)
            if start_idx < end_idx:
                hour_data = stock_data.iloc[start_idx:end_idx]
                hour_change = ((hour_data['close'].iloc[-1] - hour_data['open'].iloc[0]) / hour_data['open'].iloc[0]) * 100
                recent_trend.append(f"{i+1}小时前: {hour_change:.2f}%")
        
        summary = f"""
        股票代码: {symbol}
        最新价格: {latest_price:.2f}
        开盘价格: {open_price:.2f}
        最高价格: {high_price:.2f}
        最低价格: {low_price:.2f}
        涨跌幅: {change_percent:.2f}%
        总成交量: {volume:,}
        数据条数: {len(stock_data)}
        最近走势:
        {chr(10).join(recent_trend)}
        """
        
        return summary
    
    def analyze_stock(self, stock_data, symbol):
        """
        分析股票数据，优先使用Gemini Pro，失败则使用GPT-4o
        
        Args:
            stock_data: 股票数据DataFrame
            symbol: 股票代码
            
        Returns:
            dict: 分析结果
        """
        # 首先使用Gemini Pro
        result = self.analyze_with_gemini(stock_data, symbol)
        
        # 如果Gemini Pro失败，使用GPT-4o
        if not result and self.openai_client:
            result = self.analyze_with_gpt4o(stock_data, symbol)
        
        return result

def analyze_with_ai(stock_data, symbol):
    """便捷函数：使用AI分析股票数据"""
    analyzer = AIAnalyzer()
    return analyzer.analyze_stock(stock_data, symbol)