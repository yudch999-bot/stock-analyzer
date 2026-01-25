#!/usr/bin/env python3
"""项目测试脚本"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_module_imports():
    """测试模块导入"""
    print("开始测试模块导入...")
    
    modules = [
        ('data_fetcher', 'src.data_fetcher'),
        ('ai_analyzer', 'src.ai_analyzer'),
        ('telegram_bot', 'src.telegram_bot'),
        ('report_generator', 'src.report_generator'),
        ('scheduler', 'src.scheduler'),
    ]
    
    success_count = 0
    total_count = len(modules)
    
    for module_name, import_path in modules:
        try:
            __import__(import_path)
            print(f"✓ {module_name} 模块导入成功")
            success_count += 1
        except Exception as e:
            print(f"✗ {module_name} 模块导入失败: {e}")
    
    print(f"\n模块导入测试完成: {success_count}/{total_count} 成功")
    return success_count == total_count

def test_telegram_bot():
    """测试Telegram机器人"""
    print("\n开始测试Telegram机器人...")
    
    try:
        from src.telegram_bot import get_telegram_bot
        bot = get_telegram_bot()
        monitored_stocks = bot.get_monitored_stocks()
        print(f"✓ Telegram机器人初始化成功")
        print(f"  监控股票列表: {monitored_stocks}")
        return True
    except Exception as e:
        print(f"✗ Telegram机器人测试失败: {e}")
        return False

def test_data_fetcher():
    """测试数据抓取器"""
    print("\n开始测试数据抓取器...")
    
    try:
        from src.data_fetcher import StockDataFetcher
        fetcher = StockDataFetcher()
        print(f"✓ 数据抓取器初始化成功")
        return True
    except Exception as e:
        print(f"✗ 数据抓取器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("========== 项目测试 ==========")
    
    tests = [
        ('模块导入', test_module_imports),
        ('Telegram机器人', test_telegram_bot),
        ('数据抓取器', test_data_fetcher),
    ]
    
    success_count = 0
    total_count = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n测试: {test_name}")
        if test_func():
            success_count += 1
    
    print(f"\n========== 测试结果 ==========")
    print(f"总测试数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"失败数: {total_count - success_count}")
    
    if success_count == total_count:
        print("✓ 所有测试通过！")
        return 0
    else:
        print("✗ 部分测试失败，需要检查")
        return 1

if __name__ == "__main__":
    sys.exit(main())