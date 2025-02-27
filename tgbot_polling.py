import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, Updater

# 記錄 log
logging.basicConfig(filename='tgbot_polling.log', level=logging.DEBUG)

# 機器人的 Token
TOKEN = '6967308037:AAEvv3Kp8Ito8fJryVEAHkS8J8Ot9KId4C0'

# 定義/start命令的回應函數
async def start(Update, ContextTypes) -> None:
    await Update.message.reply_text('你好！這是我的第一條消息。') 

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    # print(update)
    """Echo the user message."""
    await update.message.reply_text(f'你說了: {user_input}')


def main() -> None:
    
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
