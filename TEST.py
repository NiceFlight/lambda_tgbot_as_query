import requests
import json
import telebot

botGetUpdate = 'https://api.telegram.org/bot6967308037:AAEvv3Kp8Ito8fJryVEAHkS8J8Ot9KId4C0/getUpdates'
botSendMessage = 'https://api.telegram.org/bot6967308037:AAEvv3Kp8Ito8fJryVEAHkS8J8Ot9KId4C0/sendMessage'
botSendLocation = 'https://api.telegram.org/bot6967308037:AAEvv3Kp8Ito8fJryVEAHkS8J8Ot9KId4C0/sendlocation'

# https://api.telegram.org/bot[botToken]/sendlocation?chat_id=[UserID]&latitude=51.6680&longitude=32.6546
res = requests.get(botGetUpdate).text
aa = json.loads(res)
chat_id = aa['result'][0]['message']['from']['id']
latitude = aa['result'][0]['message']['location']['latitude']
longitude = aa['result'][0]['message']['location']['longitude']

# print(chat_id)
# print(latitude, longitude)

json = {
	'chat_id': chat_id,
	'text': f'{latitude}, {longitude}',
	'latitude': [latitude, 23.5],
	'longitude': [longitude, 121]
}

alert = requests.post(botSendLocation, json=json)
# alert = requests.post(botSendMessage, json=json)
print(alert.content)


# bot = telebot.TeleBot('6967308037:AAEvv3Kp8Ito8fJryVEAHkS8J8Ot9KId4C0')
# bot.send_location(chat_id, latitude, longitude)
