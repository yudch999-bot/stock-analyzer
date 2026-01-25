# 股票分析系统 - 1分钟哨兵

## 项目介绍

1分钟哨兵是一个智能股票分析系统，专注于捕捉A股市场中肉眼难以感知的主力吸筹/派发痕迹。通过双引擎AI分析和Telegram机器人交互，为投资者提供深度市场洞察。

## 核心功能

### 📊 1分钟K线数据抓取
- 自动抓取A股1分钟K线数据
- 实时监控市场变化
- 捕捉主力资金动向

### 🧠 双引擎AI分析
- **主引擎**：Google Gemini Pro (高速、免费)
- **副引擎**：OpenAI GPT-4o (精准、兜底)
- 深度分析供求关系
- 自动识别Spring（弹簧效应）、UT（上冲回落）、LPS（最后支撑点）等威科夫关键行为
- 识别主力吸筹/派发痕迹

### 🤖 Telegram机器人
- **指令管理**：直接在电报群发送代码即可添加/删除监控，无需接触代码
- **研报推送**：自动生成包含红绿高对比K线图的PDF研报，自主到手机
- **实时通知**：重要市场变化及时提醒

### ☁️ Serverless架构
- 运行在GitHub Actions上
- 零服务器成本
- 完全自动化维护

### ⏰ 智能调度
- **午盘 (12:00)**：自动运行分析并主动报告
- **收盘 (15:15)**：自动运行分析并主动报告
- **每30分钟**：自动同步Telegram指令，更新监控列表

## 技术栈

- **主要语言**：Python 3.10+
- **核心依赖**：
  - python-telegram-bot：Telegram机器人
  - requests：HTTP请求
  - python-dotenv：环境变量管理
  - reportlab：PDF生成
  - matplotlib：K线图绘制
  - numpy/pandas：数据处理
  - google-generativeai：Google Gemini Pro API
  - openai：OpenAI GPT-4o API
  - schedule：任务调度

## 安装配置

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/stock-analyzer.git
cd stock-analyzer
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 文件为 `.env` 并填写相应的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Google Gemini API
GOOGLE_API_KEY=your_google_api_key

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# 股票数据API
STOCK_API_KEY=your_stock_api_key

# 项目配置
PROJECT_NAME=stock_analyzer
DEBUG=True
```

### 4. 配置GitHub Actions

在GitHub仓库的 `Settings > Secrets and variables > Actions` 中添加以下密钥：

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `GOOGLE_API_KEY`
- `OPENAI_API_KEY`
- `STOCK_API_KEY`

## 使用方法

### Telegram机器人指令

1. **添加监控**：直接发送股票代码（如：`600519`）
2. **移除监控**：发送 `/remove 股票代码`（如：`/remove 600519`）
3. **查看监控列表**：发送 `/list`
4. **查看帮助**：发送 `/help`
5. **开始使用**：发送 `/start`

### 自动分析

系统会在以下时间自动运行分析：
- 每天午盘 (12:00)
- 每天收盘 (15:15)
- 每30分钟同步一次Telegram指令

分析完成后，系统会自动生成PDF研报并发送到Telegram聊天中。

## 项目结构

```
stock-analyzer/
├── main.py              # 主入口文件
├── requirements.txt     # 依赖配置
├── .env.example         # 环境变量示例
├── src/
│   ├── data_fetcher.py  # 数据抓取模块
│   ├── ai_analyzer.py   # AI分析模块
│   ├── telegram_bot.py  # Telegram机器人模块
│   ├── report_generator.py  # PDF研报生成模块
│   └── scheduler.py     # 智能调度模块
└── .github/
    └── workflows/
        └── stock-analyzer.yml  # GitHub Actions工作流
```

## 注意事项

1. **API密钥安全**：请妥善保管您的API密钥，不要将其提交到版本控制系统
2. **数据来源**：本系统使用的股票数据API需要您自行注册获取
3. **分析结果仅供参考**：AI分析结果不构成投资建议，请结合自身判断进行投资决策
4. **GitHub Actions限制**：免费版GitHub Actions有运行时间限制，可能会影响系统的持续运行

## 故障排除

### 常见问题

1. **Telegram机器人无响应**
   - 检查 `TELEGRAM_BOT_TOKEN` 是否正确
   - 检查机器人是否已添加到聊天群组
   - 检查机器人是否有发送消息的权限

2. **分析报告未生成**
   - 检查股票数据API是否正常
   - 检查AI API密钥是否有效
   - 查看GitHub Actions运行日志

3. **GitHub Actions运行失败**
   - 检查所有API密钥是否正确配置
   - 检查依赖安装是否成功
   - 查看详细的运行日志

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License

## 免责声明

本项目仅供学习和研究使用，不构成任何投资建议。使用本项目产生的任何后果由使用者自行承担。
