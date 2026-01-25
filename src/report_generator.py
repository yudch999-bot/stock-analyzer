#!/usr/bin/env python3
"""PDF研报生成模块"""

import os
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

class ReportGenerator:
    """PDF研报生成器"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # 自定义样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#333333'),
            spaceAfter=20
        )
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#555555'),
            spaceAfter=15
        )
        self.content_style = ParagraphStyle(
            'CustomContent',
            parent=self.styles['BodyText'],
            fontSize=12,
            textColor=colors.HexColor('#333333'),
            leading=20
        )
    
    def generate_kline_chart(self, stock_data, symbol, output_path):
        """
        生成K线图
        
        Args:
            stock_data: 股票数据DataFrame
            symbol: 股票代码
            output_path: 输出路径
        """
        if stock_data.empty:
            logger.warning(f"无数据，无法生成K线图: {symbol}")
            return False
        
        try:
            plt.figure(figsize=(12, 6))
            
            # 绘制K线图
            for i, (idx, row) in enumerate(stock_data.iterrows()):
                open_price = row['open']
                close_price = row['close']
                high_price = row['high']
                low_price = row['low']
                
                # 确定K线颜色
                if close_price >= open_price:
                    color = 'red'  # 上涨
                else:
                    color = 'green'  # 下跌
                
                # 绘制实体
                plt.bar(idx, abs(close_price - open_price), bottom=min(open_price, close_price), 
                        width=0.0001, color=color)
                # 绘制影线
                plt.vlines(idx, low_price, high_price, color=color, linewidth=1)
            
            # 设置图表属性
            plt.title(f'{symbol} 1分钟K线图', fontsize=16)
            plt.xlabel('时间', fontsize=12)
            plt.ylabel('价格', fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # 设置x轴日期格式
            ax = plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.xticks(rotation=45)
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图片
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"K线图生成成功: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"生成K线图失败: {e}")
            return False
    
    def generate_pdf_report(self, stock_data, analysis_result, symbol, output_path):
        """
        生成PDF研报
        
        Args:
            stock_data: 股票数据DataFrame
            analysis_result: 分析结果
            symbol: 股票代码
            output_path: 输出路径
        """
        try:
            # 创建PDF文档
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # 生成K线图
            chart_path = f'{symbol}_kline.png'
            chart_generated = self.generate_kline_chart(stock_data, symbol, chart_path)
            
            # 构建PDF内容
            story = []
            
            # 标题
            title = Paragraph(f'股票分析报告 - {symbol}', self.title_style)
            story.append(title)
            story.append(Spacer(1, 10))
            
            # 报告时间
            report_time = Paragraph(f'报告时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', self.content_style)
            story.append(report_time)
            story.append(Spacer(1, 20))
            
            # 数据摘要
            if not stock_data.empty:
                story.append(Paragraph('一、数据摘要', self.subtitle_style))
                
                latest_price = stock_data['close'].iloc[-1]
                open_price = stock_data['open'].iloc[0]
                high_price = stock_data['high'].max()
                low_price = stock_data['low'].min()
                volume = stock_data['volume'].sum()
                change_percent = ((latest_price - open_price) / open_price) * 100
                
                data_summary = [
                    ['指标', '数值'],
                    ['最新价格', f'{latest_price:.2f}'],
                    ['开盘价格', f'{open_price:.2f}'],
                    ['最高价格', f'{high_price:.2f}'],
                    ['最低价格', f'{low_price:.2f}'],
                    ['涨跌幅', f'{change_percent:.2f}%'],
                    ['总成交量', f'{volume:,}']
                ]
                
                table = Table(data_summary, colWidths=[6*cm, 6*cm])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#333333')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd'))
                ]))
                story.append(table)
                story.append(Spacer(1, 20))
            
            # K线图
            if chart_generated:
                story.append(Paragraph('二、K线图分析', self.subtitle_style))
                img = Image(chart_path, width=16*cm, height=8*cm)
                story.append(img)
                story.append(Spacer(1, 20))
            
            # AI分析结果
            if analysis_result:
                story.append(Paragraph('三、AI分析报告', self.subtitle_style))
                story.append(Paragraph(f'分析引擎: {analysis_result.get("engine", "未知")}', self.content_style))
                story.append(Spacer(1, 10))
                
                analysis_text = analysis_result.get('analysis', '')
                # 分段处理
                for paragraph in analysis_text.split('\n'):
                    if paragraph.strip():
                        story.append(Paragraph(paragraph.strip(), self.content_style))
                        story.append(Spacer(1, 10))
            
            # 生成PDF
            doc.build(story)
            
            # 清理临时文件
            if chart_generated and os.path.exists(chart_path):
                os.remove(chart_path)
            
            logger.info(f"PDF研报生成成功: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"生成PDF研报失败: {e}")
            # 清理临时文件
            if os.path.exists(chart_path):
                os.remove(chart_path)
            return False

def generate_pdf_report(stock_data, analysis_result, symbol, output_path):
    """便捷函数：生成PDF研报"""
    generator = ReportGenerator()
    return generator.generate_pdf_report(stock_data, analysis_result, symbol, output_path)