#!/usr/bin/env python3
"""智能调度模块"""

import os
import time
import logging
import schedule
from datetime import datetime
from src.data_fetcher import fetch_minute_data
from src.ai_analyzer import analyze_with_ai
from src.telegram_bot import get_telegram_bot
from src.report_generator import generate_pdf_report

logger = logging.getLogger(__name__)

class Scheduler:
    """智能调度器"""
    
    def __init__(self):
        self.telegram_bot = get_telegram_bot()
        self.monitored_stocks = []
    
    def update_monitored_stocks(self):
        """
        更新监控股票列表
        """
        try:
            self.telegram_bot.update_monitored_stocks()
            self.monitored_stocks = self.telegram_bot.get_monitored_stocks()
            logger.info(f"监控股票列表已更新: {len(self.monitored_stocks)} 只股票")
        except Exception as e:
            logger.error(f"更新监控股票列表失败: {e}")
    
    def analyze_stocks(self):
        """
        分析监控的股票
        """
        if not self.monitored_stocks:
            logger.info("无监控股票，跳过分析")
            return
        
        logger.info(f"开始分析 {len(self.monitored_stocks)} 只股票")
        
        for symbol in self.monitored_stocks:
            try:
                # 获取股票数据
                stock_data = fetch_minute_data(symbol)
                if stock_data.empty:
                    logger.warning(f"无数据: {symbol}")
                    continue
                
                # AI分析
                analysis_result = analyze_with_ai(stock_data, symbol)
                if not analysis_result:
                    logger.warning(f"分析失败: {symbol}")
                    continue
                
                # 生成PDF研报
                report_path = f"{symbol}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                report_generated = generate_pdf_report(stock_data, analysis_result, symbol, report_path)
                
                if report_generated:
                    # 发送研报到Telegram
                    self.telegram_bot.send_message(f"📊 {symbol} 分析完成，请查收研报")
                    # 这里可以添加发送PDF的逻辑
                    logger.info(f"研报生成并发送成功: {symbol}")
                else:
                    logger.warning(f"研报生成失败: {symbol}")
                
                # 避免API调用过于频繁
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"分析股票失败: {symbol}, {e}")
                continue
        
        logger.info("股票分析完成")
    
    def run_midday_analysis(self):
        """
        午盘分析
        """
        logger.info("开始午盘分析")
        self.update_monitored_stocks()
        self.analyze_stocks()
        logger.info("午盘分析完成")
    
    def run_close_analysis(self):
        """
        收盘分析
        """
        logger.info("开始收盘分析")
        self.update_monitored_stocks()
        self.analyze_stocks()
        logger.info("收盘分析完成")
    
    def setup_schedule(self):
        """
        设置调度任务
        """
        # 午盘分析 (12:00)
        schedule.every().day.at("12:00").do(self.run_midday_analysis)
        logger.info("已设置午盘分析任务: 每天 12:00")
        
        # 收盘分析 (15:15)
        schedule.every().day.at("15:15").do(self.run_close_analysis)
        logger.info("已设置收盘分析任务: 每天 15:15")
        
        # 每30分钟更新监控列表
        schedule.every(30).minutes.do(self.update_monitored_stocks)
        logger.info("已设置监控列表更新任务: 每30分钟")
    
    def run(self):
        """
        运行调度器
        """
        logger.info("智能调度器启动")
        
        # 初始更新监控列表
        self.update_monitored_stocks()
        
        # 设置调度任务
        self.setup_schedule()
        
        # 持续运行
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                logger.error(f"调度器运行出错: {e}")
                time.sleep(60)

def run_scheduled_tasks():
    """
    运行调度任务
    """
    scheduler = Scheduler()
    scheduler.run()