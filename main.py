#!/usr/bin/env python3
"""股票分析系统主入口文件"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('stock_analyzer.log')
    ]
)

logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_fetcher import fetch_minute_data
from src.ai_analyzer import analyze_with_ai
from src.telegram_bot import TelegramBot
from src.report_generator import generate_pdf_report
from src.scheduler import run_scheduled_tasks

def main():
    """主函数"""
    logger.info("股票分析系统启动")
    
    try:
        # 运行调度任务
        run_scheduled_tasks()
        
    except Exception as e:
        logger.error(f"系统运行出错: {e}", exc_info=True)

if __name__ == "__main__":
    main()