import json
import os
import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes, Updater, MessageHandler, filters
from pip._vendor import requests
import asyncio


'''方法一'''
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# 設置日誌基本配置
logging.basicConfig(level=logging.INFO)

# 從環境變量中獲取 Telegram Token
TOKEN = os.environ['TELEGRAM_TOKEN']

# 初始化 Telegram Bot
bot = Bot(token=TOKEN)

# 創建應用程序實例
application = Application.builder().token(TOKEN).build()

# 處理 /start 命令的函數
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot.')

# 處理收到的消息的函數
async def echo(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    userinput = update.message.text
    await update.message.reply_text(f'You said: {userinput}')

# 添加命令處理程序
application.add_handler(CommandHandler('start', start))

# 添加消息處理程序，過濾文本消息且非命令的消息
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# 主函數，處理 Telegram webhook 事件
async def tgbot_main(application, event):
    async with application:
        await application.initialize()
        await application.process_update(Update.de_json(json.loads(event["body"]), application.bot))

# Lambda 函數處理程序
def lambda_handler(event, context):
    # 記錄接收到的事件
    logging.info("Receive event: %s", event)

    try:
        # 運行主函數來處理事件
        asyncio.run(tgbot_main(application, event))
    except Exception as e:
        # 記錄錯誤信息
        logging.error("Error parsing update: %s", e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Oops! Something went wrong"})
        }
    return {
        # 返回成功的 HTTP 狀態碼和消息
        'statusCode': 200,
        'body': json.dumps('OK')
    }

'''方法二'''
# def lambda_handler(event, context):
#     body = json.loads(event.get("body", "{}"))
#     message = body.get("message", {})
#     chat_id = message.get("chat", {}).get("id")
#     text = message.get("text", "")
    
#     if text:
#         reply = f"You said: {text}"
#         token = os.environ["TELEGRAM_TOKEN"]
#         requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
#                       json={"chat_id": chat_id, "text": reply})
    
#     return {"statusCode": 200, "body": json.dumps("OK")}
