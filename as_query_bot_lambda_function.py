import json
import os
import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from pip._vendor import requests
import asyncio
import itertools
import boto3
from boto3.dynamodb.conditions import Key, Attr

# 設置日誌基本配置
logging.basicConfig(level=logging.INFO)

# 從環境變量中獲取 Telegram Token
TOKEN = os.environ['TELEGRAM_TOKEN']

# 初始化 Telegram Bot
bot = Bot(token=TOKEN)

# 處理 /start 命令的函數
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot.')

'''AS 查詢'''
# 讀取 JSON 文件
def load_locations():
    with open('as_code.json', 'r', encoding='utf-8') as f:
        return json.load(f)

locations = load_locations()

# connect to the database
def connect_to_db():
    region = 'region'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('table')
    return table

def get_cities(table):
    response = table.scan()['Items']
    cities = []
    for city in response:
        cities.append(city['city'])
        unique_cities = list(set(cities))
    return unique_cities

def get_towns(table, city):
    response = table.scan(FilterExpression=Attr('city').eq(city), ProjectionExpression='town')['Items']
    towns = []
    for town in response:
        towns.append(town['town'])
        unique_towns = list(set(towns))
    return unique_towns

def get_sites(table, city, town):
    response = table.scan(FilterExpression=Attr('city').eq(city) & Attr('town').eq(town))['Items']
    return response

def get_site_details(table, city, town, site):
    response = table.scan(FilterExpression=Attr('city').eq(city) & Attr('town').eq(town) & Attr('name').eq(site))['Items']
    return response

# 全域建立 DynamoDB 連線
TABLE = connect_to_db()
CITIES = get_cities(TABLE)

# 處理 /as 命令的函數
async def city_button(update: Update, context: CallbackContext) -> None:
    
    # cities = list(locations.keys())
    city_keyboard = []
    for a, b in itertools.zip_longest(CITIES[::2], CITIES[1::2], fillvalue=None):
        if b is not None:
            city_keyboard.append([InlineKeyboardButton(a, callback_data=a), InlineKeyboardButton(b, callback_data=b)])
        else:
            city_keyboard.append([InlineKeyboardButton(a, callback_data=a)])
    reply_markup = InlineKeyboardMarkup(city_keyboard)
    await update.message.reply_text('Please choose the city: ', reply_markup=reply_markup)

# 處理按鈕點擊的回調函數
async def button(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data in CITIES:
        town_keyboard = []
        towns = get_towns(TABLE, data)
        for a, b in itertools.zip_longest(towns[::2], towns[1::2], fillvalue=None):
            if b is not None:
                town_keyboard.append([InlineKeyboardButton(a, callback_data=f"{data}-{a}"), InlineKeyboardButton(b, callback_data=f"{data}-{b}")])
            else:
                town_keyboard.append([InlineKeyboardButton(a, callback_data=f"{data}-{a}")])
        reply_markup = InlineKeyboardMarkup(town_keyboard)
        await query.edit_message_text(text=f"You choose {data}, please choose town: ", reply_markup=reply_markup)

    elif '-' in data:
        as_keyboard = []
        city, town = data.split('-')
        places = get_sites(TABLE, city, town)
        sites = [place['name'] for place in places]
        # as_no = [place['No'] for place in places]

        for a, b in itertools.zip_longest(sites[::2], sites[1::2], fillvalue=None):
            if b is not None:
                as_keyboard.append([InlineKeyboardButton(a, callback_data=f"{city}_{town}_{a}"), InlineKeyboardButton(b, callback_data=f"{city}_{town}_{b}")])
            else:
                as_keyboard.append([InlineKeyboardButton(a, callback_data=f"{city}_{town}_{a}")])
        reply_markup = InlineKeyboardMarkup(as_keyboard)
        await query.edit_message_text(text=f"You choose {town}, please choose site: ", reply_markup=reply_markup)
    else:
        city, town, site = data.split('_')
        site_details = get_site_details(connect_to_db(), city, town, site)
        chat_id = query.message.chat.id

        await query.edit_message_text(text=f"You choose: {site}"), 
        await context.bot.send_venue(chat_id=chat_id, latitude=site_details[0]['lat'], longitude=site_details[0]['lng'], title=site_details[0]['name'], address="NONE")

# 主函數，處理 Telegram webhook 事件
async def tgbot_main(application, event):
    async with application:
        await application.initialize()
        await application.process_update(Update.de_json(json.loads(event["body"]), application.bot))

# Lambda 函數處理程序
def lambda_handler(event, context):
    
    # 記錄接收到的事件
    logging.info("Receive event: %s", event)

    # 建立 bot
    application = ApplicationBuilder().token(TOKEN).build()

    # 添加命令處理程序
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('as', city_button))

    # 添加函式處理程序，過濾文本消息且非命令的消息
    application.add_handler(CallbackQueryHandler(button))

    # 運行主函數來處理事件
    asyncio.run(tgbot_main(application, event))

    return {
        # 返回成功的 HTTP 狀態碼和消息
        'statusCode': 200,
        'body': json.dumps('OK')
    }
