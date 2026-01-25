#!/usr/bin/env python3
"""A股1分钟K线数据抓取模块"""

import os
import time
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class StockDataFetcher:
    """股票数据抓取器"""
    
    def __init__(self):
        self.api_key = os.getenv('STOCK_API_KEY')
        self.base_url = "https://api.example.com/stock"
    
    def fetch_minute_data(self, symbol, start_date=None, end_date=None):
        """
        获取股票1分钟K线数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            DataFrame: 包含1分钟K线数据
        """
        try:
            logger.info(f"开始获取 {symbol} 的1分钟K线数据")
            
            # 如果未指定日期，使用今天
            if not end_date:
                end_date = datetime.now()
            if not start_date:
                start_date = end_date - timedelta(days=1)
            
            # 构建请求参数
            params = {
                'symbol': symbol,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'interval': '1min',
                'api_key': self.api_key
            }
            
            # 发送请求
            response = requests.get(f"{self.base_url}/minute", params=params, timeout=30)
            response.raise_for_status()
            
            # 解析数据
            data = response.json()
            df = pd.DataFrame(data['data'])
            
            # 处理时间戳
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            logger.info(f"成功获取 {symbol} 的1分钟K线数据，共 {len(df)} 条")
            return df
            
        except Exception as e:
            logger.error(f"获取 {symbol} 数据失败: {e}")
            return pd.DataFrame()
    
    def fetch_multiple_stocks(self, symbols):
        """
        批量获取多个股票的数据
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            dict: 股票代码到数据的映射
        """
        result = {}
        for symbol in symbols:
            data = self.fetch_minute_data(symbol)
            result[symbol] = data
            # 避免API调用过于频繁
            time.sleep(1)
        return result

def fetch_minute_data(symbol, start_date=None, end_date=None):
    """便捷函数：获取股票1分钟K线数据"""
    fetcher = StockDataFetcher()
    return fetcher.fetch_minute_data(symbol, start_date, end_date)

def fetch_multiple_stocks(symbols):
    """便捷函数：批量获取多个股票的数据"""
    fetcher = StockDataFetcher()
    return fetcher.fetch_multiple_stocks(symbols)