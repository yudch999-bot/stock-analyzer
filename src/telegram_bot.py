#!/usr/bin/env python3
"""Telegram机器人模块"""

import os
import logging
import json
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logger = logging.getLogger(__name__)

class TelegramBot:
    """Telegram机器人"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.monitored_stocks = self._load_monitored_stocks()
        self.application = None
    
    def _load_monitored_stocks(self):
        """
        加载监控股票列表
        
        Returns:
            list: 监控股票列表
        """
        try:
            if os.path.exists('monitored_stocks.json'):
                with open('monitored_stocks.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载监控股票列表失败: {e}")
        return []
    
    def _save_monitored_stocks(self):
        """
        保存监控股票列表
        """
        try:
            with open('monitored_stocks.json', 'w', encoding='utf-8') as f:
                json.dump(self.monitored_stocks, f, ensure_ascii=False, indent=2)
            logger.info(f"监控股票列表已保存: {len(self.monitored_stocks)} 只股票")
        except Exception as e:
            logger.error(f"保存监控股票列表失败: {e}")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        处理/start命令
        """
        await update.message.reply_text(
            "欢迎使用股票分析机器人！\n"+
            "\n命令说明：\n"+
            "- 直接发送股票代码：添加监控\n"+
            "- /remove 股票代码：移除监控\n"+
            "- /list：查看监控列表\n"+
            "- /help：查看帮助"
        )
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        处理/help命令
        """
        await update.message.reply_text(
            "帮助信息：\n"+
            "\n添加监控：直接发送股票代码（如：600519）\n"+
            "移除监控：/remove 股票代码（如：/remove 600519）\n"+
            "查看列表：/list\n"+
            "开始使用：/start"
        )
    
    async def list_stocks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        处理/list命令
        """
        if not self.monitored_stocks:
            await update.message.reply_text("当前无监控股票")
        else:
            stocks_list = "\n".join([f"- {stock}" for stock in self.monitored_stocks])
            await update.message.reply_text(f"监控股票列表：\n{stocks_list}")
    
    async def remove_stock(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        处理/remove命令
        """
        if not context.args:
            await update.message.reply_text("请指定要移除的股票代码")
            return
        
        stock_code = context.args[0]
        if stock_code in self.monitored_stocks:
            self.monitored_stocks.remove(stock_code)
            self._save_monitored_stocks()
            await update.message.reply_text(f"已移除监控：{stock_code}")
        else:
            await update.message.reply_text(f"{stock_code} 不在监控列表中")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        处理普通消息（添加监控）
        """
        message_text = update.message.text.strip()
        
        # 简单验证股票代码格式
        if self._is_valid_stock_code(message_text):
            if message_text not in self.monitored_stocks:
                self.monitored_stocks.append(message_text)
                self._save_monitored_stocks()
                await update.message.reply_text(f"已添加监控：{message_text}")
            else:
                await update.message.reply_text(f"{message_text} 已在监控列表中")
        else:
            await update.message.reply_text("请发送有效的股票代码")
    
    def _is_valid_stock_code(self, code):
        """
        验证股票代码格式
        
        Args:
            code: 股票代码
            
        Returns:
            bool: 是否有效
        """
        # 简单验证：6位数字
        return len(code) == 6 and code.isdigit()
    
    def send_message(self, text):
        """
        发送消息到指定聊天
        
        Args:
            text: 消息内容
        """
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram Bot未配置")
            return
        
        try:
            bot = Bot(token=self.bot_token)
            bot.send_message(chat_id=self.chat_id, text=text)
            logger.info("消息发送成功")
        except Exception as e:
            logger.error(f"消息发送失败: {e}")
    
    def send_photo(self, photo_path, caption=None):
        """
        发送图片到指定聊天
        
        Args:
            photo_path: 图片路径
            caption: 图片说明
        """
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram Bot未配置")
            return
        
        try:
            bot = Bot(token=self.bot_token)
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id=self.chat_id, photo=photo, caption=caption)
            logger.info("图片发送成功")
        except Exception as e:
            logger.error(f"图片发送失败: {e}")
    
    def run(self):
        """
        运行机器人
        """
        if not self.bot_token:
            logger.warning("Telegram Bot未配置，无法运行")
            return
        
        try:
            self.application = ApplicationBuilder().token(self.bot_token).build()
            
            # 添加命令处理器
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(CommandHandler("help", self.help))
            self.application.add_handler(CommandHandler("list", self.list_stocks))
            self.application.add_handler(CommandHandler("remove", self.remove_stock))
            
            # 添加消息处理器
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            logger.info("Telegram Bot已启动")
            self.application.run_polling()
            
        except Exception as e:
            logger.error(f"Telegram Bot运行失败: {e}")
    
    def get_monitored_stocks(self):
        """
        获取监控股票列表
        
        Returns:
            list: 监控股票列表
        """
        return self.monitored_stocks
    
    def update_monitored_stocks(self):
        """
        更新监控股票列表（从文件重新加载）
        """
        self.monitored_stocks = self._load_monitored_stocks()
        logger.info(f"监控股票列表已更新: {len(self.monitored_stocks)} 只股票")

def get_telegram_bot():
    """便捷函数：获取Telegram机器人实例"""
    return TelegramBot()