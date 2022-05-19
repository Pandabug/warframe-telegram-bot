import texts as text

import telebot
from telebot import types

import os
import requests
from flask import Flask, request


bot = telebot.TeleBot(os.environ.get("TOKEN"))
server = Flask(__name__)


# Calculate length
def calc_len(keyword, num_char):
    tabs_to_append = num_char - len(keyword)
    new_keyword = (keyword[:num_char-1] + "." if (tabs_to_append <= 0) else keyword[:num_char] + " "*tabs_to_append)

    return new_keyword


# Start
@bot.message_handler(commands=['start'])
def start(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    bot.send_message(message.chat.id, f'{text.mission_text[language][9]}')
    help(message)


# Help
@bot.message_handler(commands=['help'])
def help(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    bot.send_message(message.chat.id, text.help_text[language])


# Info
@bot.message_handler(commands=['info'])
def info(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    bot.send_message(message.chat.id, text.description_text[language])


@bot.message_handler(commands=['repo'])
def creator(message):
    bot.send_message(message.chat.id, 'https://github.com/Pandabug/warframe-telegram-bot')


# Cetus current time
@bot.message_handler(commands=['time'])
def wordl_time(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'
    space = '--------------------|------------'

    try:
        response = requests.get('https://api.warframestat.us/pc/').json()

        msg = f'{calc_len(text.mission_text[language][5], 20)}|{response["cetusCycle"]["shortString"]}\n{space}\n{calc_len(text.mission_text[language][6], 20)}|{response["vallisCycle"]["shortString"]}\n{space}\n{calc_len(text.mission_text[language][7], 20)}|{response["cambionCycle"]["timeLeft"]}'

        bot.send_message(message.chat.id, parse_mode='html', text=f'<pre>{msg}</pre>')

    except:
        bot.send_message(message.chat.id, f'{text.error_text[language]}')


@bot.message_handler(commands=['sortie'])
def sortie(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    try:
        response = requests.get(f'https://api.warframestat.us/pc/{language}/sortie').json()
        msg = ''

        for mission in response["variants"]:
            msg += f'\n-------------- <b>{response["variants"].index(mission) + 1}</b> --------------\n<b>{text.mission_text[language][3]}:</b> {mission["missionType"]}\n<b>{text.mission_text[language][0]}:</b> {mission["node"]}'

        bot.send_message(message.chat.id, parse_mode='html', text=f'{msg}')

    except:
        bot.send_message(message.chat.id, f'{text.error_text[language]}')


@bot.message_handler(commands=['trader'])
def void_trader(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    try:
        response = requests.get(f'https://api.warframestat.us/pc/{language}/voidTrader').json()

        if response['active']:
            bot.send_message(message.chat.id, (f'Конец через: {response["endString"]}' if language == 'ru' else f'End in: {response["endString"]}'))
        else:
            bot.send_message(message.chat.id, (f'Приедет через: {response["startString"]}' if language == 'ru' else f'Start in: {response["startString"]}'))

    except:
        bot.send_message(message.chat.id, f'{text.error_text[language]}')


def keyboard(type, language, check = False):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(*[types.InlineKeyboardButton(type[language][count], callback_data=type['en'][count]) for count in type['en']])

    if check:
        markup.add(types.InlineKeyboardButton('-->', callback_data='-->'))
    else:
        markup.add(types.InlineKeyboardButton('<--', callback_data='<--'))

    return markup


# Search with message buttons
@bot.message_handler(commands=['search'])
def search_for(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    bot.send_message(message.chat.id, f'{text.mission_text[language][8]}: ', reply_markup=keyboard(text.mission_names, language, True))


@bot.callback_query_handler(func=lambda query: query.data in ['-->', '<--'])
def change_keyboard(message):
    language = message.message.from_user.language_code if message.message.from_user.language_code in ['ru', 'en'] else 'en'

    if message.data == '-->':
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'{text.mission_text[language][8]}: ', reply_markup=keyboard(text.relic_names, language))

    if message.data == '<--':
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'{text.mission_text[language][8]}: ', reply_markup=keyboard(text.mission_names, language, True))


@bot.callback_query_handler(func=lambda query: query.data in text.mission_names['en'].values() or query.data in text.relic_names['en'].values())
def mission_search(message):
    language = message.message.from_user.language_code if message.message.from_user.language_code in ['ru', 'en'] else 'en'

    try:
        checkMission = False

        msg = f'<b>{calc_len(text.mission_text[language][0], 21)}|{calc_len(text.mission_text[language][1], 8)}|{calc_len(text.mission_text[language][2], 11)}</b>\n---------------------|--------|----------\n'
        
        response = requests.get(f'https://api.warframestat.us/pc/{language}/fissures').json()
        for mission in response:
            if mission['missionKey'] == message.data:
                msg += f'{calc_len(mission["node"], 21)}|{calc_len(mission["tier"], 8)}|{calc_len(mission["eta"], 11)}\n'
                checkMission = True
            elif mission['tier'] == message.data:
                msg += f'{calc_len(mission["node"], 21)}|{calc_len(mission["tier"], 8)}|{calc_len(mission["eta"], 11)}\n'
                checkMission = True

        if checkMission:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, parse_mode='html', text=f'<b><u>{message.data}</u></b>\n<pre>{msg}</pre>')
        else:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=('Миссии не найдено.' if language == 'ru' else 'No mission found.'))

    except:
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'{text.error_text[language]}')


@bot.message_handler(commands=['arbitration'])
def arbitration(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    try:
        response = requests.get(f'https://api.warframestat.us/pc/{language}/arbitration').json()

        bot.send_message(message.chat.id, parse_mode='html', text=f'<pre>{calc_len(text.mission_text[language][0], 14)}|{response["node"]}\n{calc_len(text.mission_text[language][3], 14)}|{response["type"]}\n{calc_len(text.mission_text[language][4], 14)}|{response["enemy"]}</pre>')

    except:
        bot.send_message(message.chat.id, f'{text.error_text[language]}')


@bot.message_handler(commands=['nightwave'])
def nightwave(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    try:
        response = requests.get(f'https://api.warframestat.us/pc/{language}/nightwave').json()
        msg = (f'Сезон {response["season"]}' if language == 'ru' else f'Season {response["season"]}')

        for mission in response['activeChallenges']:
            msg += f'\n--------------------------\n{mission["desc"]}\n{mission["startString"]}'

        bot.send_message(message.chat.id, parse_mode='html', text=f'{msg}')

    except:
        bot.send_message(message.chat.id, f'{text.error_text[language]}')


@bot.message_handler(commands=['events'])
def events(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    try:
        response = requests.get(f'https://api.warframestat.us/pc/{language}/events').json()
        msg = ''

        for mission in response:
            msg += f'-------------- <b>{response.index(mission) + 1}</b> --------------\n{mission["description"]}\n{mission["node"]}\n'

        bot.send_message(message.chat.id, parse_mode='html', text=msg)

    except:
        bot.send_message(message.chat.id, f'{text.error_text[language]}')


@bot.message_handler(commands=['tenshin'])
def steel_path_reward(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    try:
        response = requests.get(f'https://api.warframestat.us/pc/{language}/steelPath').json()

        bot.send_message(message.chat.id, parse_mode='html', text=f'Current reward: {response["currentReward"]["name"]}\nCost: {response["currentReward"]["cost"]}')

    except:
        bot.send_message(message.chat.id, f'{text.error_text[language]}')


@bot.message_handler(commands=['news'])
def news(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'

    try:
        response = requests.get(f'https://api.warframestat.us/pc/{language}/news').json()
        msg = ''

        for news_data in response:
            msg += f'{news_data["eta"]}\n<a href="{news_data["link"]}">{news_data["message"]}</a>\n------\n'
        bot.send_message(message.chat.id, parse_mode='html', disable_web_page_preview=True, text=msg)
    except:
        bot.send_message(message.chat.id, f'{text.error_text[language]}')


# Receive all message sent from user
@bot.message_handler(content_types=['text'])
def user_message(message):
    language = message.from_user.language_code if message.from_user.language_code in ['ru', 'en'] else 'en'
    print(f'From: {message.from_user.first_name}, message: \n{message.text}')

    bot.send_message(message.chat.id, ('Команды не найдено.' if language == 'ru' else 'No command available.'))


@server.route('/' + os.environ.get("TOKEN"), methods=['GET', 'POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://warframe-telegram-bot.herokuapp.com/{os.environ.get("TOKEN")}')
    return "!", 200


bot.set_my_commands(
    commands=[
        telebot.types.BotCommand('time', 'Get the current time on planets.'),
        telebot.types.BotCommand('search', 'Search for void fissure missions.'),
        telebot.types.BotCommand('sortie', 'Get the details on the current Sortie.'),
        telebot.types.BotCommand('trader', 'Shows the Void Trader time and location.'),
        telebot.types.BotCommand('arbitration', 'Get current arbitration mission.'),
        telebot.types.BotCommand('nightwave', 'Shows the daily and weekly nightwave acts.'),
        telebot.types.BotCommand('events', 'Show events.'),
        telebot.types.BotCommand('tenshin', 'Show weekly tenshin reward.'),
        telebot.types.BotCommand('news', 'The lastest news from warframe.'),
        telebot.types.BotCommand('help', 'Show list of commands.'),
    ]
)


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    bot.infinity_polling()