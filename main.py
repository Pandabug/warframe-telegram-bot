import texts as text
from Constants import TOKEN
from db import users_collection

import telebot
from telebot import types

import os
import requests
from flask import Flask, request


bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


# Calculate length
def calc_len(keyword, num_char):
    tabs_to_append = num_char - len(keyword)
    new_keyword = (keyword[:num_char-1] + "." if (tabs_to_append <= 0) else keyword[:num_char] + " "*tabs_to_append)

    return new_keyword


en_help_names = ['/time', '/search', '/sortie', '/trader', '/arbitration', '/nightwave', '/events']

ru_mission_names = ['Улей', 'Шпионаж', 'Спасение', 'Оборона', 'Выживание', 'Стычка', 'Летучий', 'Разрушение', 'Разкопки', 'Перехват', 'Мобильная Оборона', 'Саботаж']
en_mission_names =['Hive', 'Spy', 'Rescue', 'Defense', 'Survival', 'Skirmish', 'Volatile', 'Disruption', 'Excavation', 'Interception', 'Mobile Defense', 'Sabotage']


# Start
@bot.message_handler(commands=['start'])
def start(message):
    if not users_collection.find_one({'_id': message.chat.id}):
        users_collection.insert_one({'_id': message.chat.id, 'language': (message.from_user.language_code if message.from_user.language_code == 'ru' or message.from_user.language_code == 'en' else 'en'), 'notification': 'off'})

    bot.send_message(message.chat.id, 'Hi Tenno!')
    bot.send_message(message.chat.id, text.start_text[message.from_user.language_code])


# Helo
@bot.message_handler(commands=['help'])
def help(message):
    user_data = users_collection.find_one({'_id': message.chat.id})

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(*[types.KeyboardButton(text) for text in en_help_names])

    bot.send_message(message.chat.id, text.help_text[user_data['language']])
    bot.send_message(message.chat.id, ('Выберете команду: ' if user_data['language'] == 'ru' else 'Select a command: '), reply_markup=markup)


# Info
@bot.message_handler(commands=['info'])
def info(message):
    user_data = users_collection.find_one({'_id': message.chat.id})

    bot.send_message(message.chat.id, text.description_text[user_data['language']])


@bot.message_handler(commands=['language'])
def language(message):
    user_data = users_collection.find_one({'_id': message.from_user.id})

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('En', callback_data='en'), types.InlineKeyboardButton('Ru', callback_data='ru'))

    bot.send_message(message.chat.id, ('Выберете язык:' if user_data['language'] == 'ru' else 'Select language:'), reply_markup=markup)


@bot.callback_query_handler(func=lambda query: query.data in ['ru', 'en'])
def callback_query(message):
    user_data = users_collection.find_one({'_id': message.from_user.id})

    if message.data == 'ru':
        if user_data['language'] != 'ru':
            users_collection.update_one({'_id': message.from_user.id}, {'$set': {'language': 'ru'}})
            bot.answer_callback_query(callback_query_id=message.id, text="Установлен русский язык!")
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text='Установлен русский язык!')
        else:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text='У вас уже установлен русский язык!')
    else:
        if user_data['language'] != 'en':
            users_collection.update_one({'_id': message.from_user.id}, {'$set': {'language': 'en'}})
            bot.answer_callback_query(callback_query_id=message.id, text="English Language installed!")
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text='English Language installed!')
        else:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text='English language already installed!')


@bot.message_handler(commands=['support'])
def support(message):
    bot.send_message(chat_id=message.chat.id, parse_mode='html', text='Support creator: \n<pre>IBAN</pre>')


# Cetus current time
@bot.message_handler(commands=['time'])
def wordl_time(message):
    user_data = users_collection.find_one({'_id': message.from_user.id})

    try:
        response = requests.get('https://ws.warframestat.us/pc/').json()

        if user_data['language'] == 'ru':
            msg = f'Ровнины Ейдолона: {response["cetusCycle"]["shortString"]}\n------------------------------\nВаллис: {response["vallisCycle"]["shortString"]}\n------------------------------\nКамбион: {response["cambionCycle"]["timeLeft"]}'
        else:
            msg = f'Plains of Eidolon: {response["cetusCycle"]["shortString"]}\n------------------------------\nOrb Vallis: {response["vallisCycle"]["shortString"]}\n------------------------------\nCambion Drift: {response["cambionCycle"]["timeLeft"]}'

        bot.send_message(message.chat.id, msg)

    except:
        bot.send_message(message.chat.id, f'{text.error_text[user_data["language"]]}')


@bot.message_handler(commands=['sortie'])
def sortie(message):
    user_data = users_collection.find_one({'_id': message.from_user.id})

    try:
        response = requests.get(f'https://ws.warframestat.us/pc/{user_data["language"]}/sortie').json()
        msg = ''

        if user_data['language'] == 'ru':
            for mission in response["variants"]:
                msg += f'\n<b>{response["variants"].index(mission) + 1}</b> -----------------------------\n<b>Тип миссии:</b> {mission["missionType"]}\n<b>Планета:</b> {mission["node"]}'
        else:
            for mission in response['variants']:
                msg += f'\n<b>{response["variants"].index(mission) + 1}</b> -----------------------------\n<b>Mission Type:</b> {mission["missionType"]}\n<b>Mission:</b> {mission["node"]}'

        bot.send_message(message.chat.id, parse_mode='html', text=f'{msg}')

    except:
        bot.send_message(message.chat.id, f'{text.error_text[user_data["language"]]}')


@bot.message_handler(commands=['trader'])
def void_trader(message):
    user_data = users_collection.find_one({'_id': message.from_user.id})

    try:
        response = requests.get(f'https://ws.warframestat.us/pc/{user_data["language"]}/voidTrader').json()

        if response['active']:
            bot.send_message(message.chat.id, (f'Конец через: {response["endString"]}' if user_data['language'] == 'ru' else f'End in: {response["endString"]}'))
        else:
            bot.send_message(message.chat.id, (f'Приедет через: {response["startString"]}' if user_data['language'] == 'ru' else f'Start in: {response["startString"]}'))

    except:
        bot.send_message(message.chat.id, f'{text.error_text[user_data["language"]]}')


def keyboard(language):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(*[types.InlineKeyboardButton(text, callback_data=callback_query) for text, callback_query in zip((ru_mission_names if language == 'ru' else en_mission_names), en_mission_names)])

    return markup


# Search with message buttons
@bot.message_handler(commands=['search'])
def search_for(message):
    user_data = users_collection.find_one({'_id': message.chat.id})

    bot.send_message(message.chat.id, 'Выберете между: ', reply_markup=keyboard(user_data['language']))


@bot.callback_query_handler(func=lambda query: query.data in en_mission_names)
def mission_search(message):
    user_data = users_collection.find_one({'_id': message.from_user.id})

    try:
        checkMission = False
        msg = ''

        if user_data['language'] == 'ru':
            msg = f'<b>{calc_len("Планета", 21)}|{calc_len("Реликвия", 8)}|{calc_len("Окончания", 11)}</b>\n---------------------|--------|----------\n'
        else:
            msg = f'<b>{calc_len("Planet", 21)}|{calc_len("Relic", 8)}|{calc_len("Time-left", 11)}</b>\n---------------------|--------|----------\n'
        
        response = requests.get(f'https://ws.warframestat.us/pc/{user_data["language"]}/fissures').json()
        for mission in response:
            if mission['missionKey'] == message.data:
                msg += f'{calc_len(mission["node"], 21)}|{calc_len(mission["tier"], 8)}|{calc_len(mission["eta"], 11)}\n'
                checkMission = True
        

        if checkMission:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, parse_mode='html', text=f'<b><u>{message.data}</u></b>\n<pre>{msg}</pre>')
        else:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=('Миссии не найдено.' if user_data["language"] == 'ru' else 'No mission found.'))

    except:
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'{text.error_text[user_data["language"]]}')


@bot.message_handler(commands=['arbitration'])
def arbitration(message):
    user_data = users_collection.find_one({'_id': message.chat.id})

    try:
        response = requests.get(f'https://ws.warframestat.us/pc/{user_data["language"]}/arbitration').json()

        if user_data['language'] == 'ru':
            bot.send_message(message.chat.id, f'Планета: {response["node"]}\nТип миссии: {response["type"]}\nВраги: {response["enemy"]}')
        else:
            bot.send_message(message.chat.id, f'Planet: {response["node"]}\nMission Type: {response["type"]}\nEnemys: {response["enemy"]}')

    except:
        bot.send_message(message.chat.id, f'{text.error_text[user_data["language"]]}')


@bot.message_handler(commands=['nightwave'])
def nightwave(message):
    user_data = users_collection.find_one({'_id': message.chat.id})

    try:
        response = requests.get(f'https://ws.warframestat.us/pc/{user_data["language"]}/nightwave').json()
        msg = (f'Сезон {response["season"]}' if user_data['language'] == 'ru' else f'Season {response["season"]}')

        for mission in response['activeChallenges']:
            msg += f'\n--------------------------\n{mission["desc"]}\n{mission["startString"]}'

        bot.send_message(message.chat.id, parse_mode='html', text=f'{msg}')

    except:
        bot.send_message(message.chat.id, f'{text.error_text[user_data["language"]]}')


@bot.message_handler(commands=['events'])
def events(message):
    user_data = users_collection.find_one({'_id': message.chat.id})

    try:
        response = requests.get('https://ws.warframestat.us/pc/en/events').json()
        msg = ''

        for mission in response:
            msg += f'<b>{response.index(mission) + 1}</b> ----------------\n{mission["description"]}\n{mission["node"]}\n'

        bot.send_message(message.chat.id, parse_mode='html', text=msg)

    except:
        bot.send_message(message.chat.id, f'{text.error_text[user_data["language"]]}')


# Receive all message sent from user
@bot.message_handler(content_types=['text'])
def user_message(message):
    user_data = users_collection.find_one({'_id': message.chat.id})
    print(f'From: {message.from_user.first_name}, message: {message.text}')

    bot.send_message(message.chat.id, ('Команды не найдено.' if user_data['language'] == 'ru' else 'No command available.'))


@server.route('/' + TOKEN, methods=['GET', 'POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://warframe-telegram-bot.herokuapp.com/{TOKEN}')
    return "!", 200


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    main()