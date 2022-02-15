import json
import os
import random
import sqlite3
import time

import requests
import telebot

botToken = os.getenv("botToken", "")
apiKey = os.getenv("apiKey", "")
historyKey = os.getenv("historyKey", "")
adminChatId = os.getenv("adminChatId", "")

bot = telebot.TeleBot(botToken)


@bot.message_handler(commands=['start'])
def entrance(message):
    bot.send_message(message.chat.id, "Привет отправь мне имя картинки и я найду его 😊")


@bot.message_handler(commands=['my_history'])
def history(message):
    bot.send_message(message.chat.id, "Ищем...")
    results = get_query_by_id(str(message.chat.id))

    if len(results) != 0:
        for result in results:
            bot.send_message(message.chat.id,
                             f"🌎 User id : {result[0]}\n"
                             f"🕵️ ‍User name : {result[1]}\n"
                             f"🔎 User query : {result[2]}\n"
                             f"🧭 Query date: {result[3]}\n"
                             f"👀 Query result : {result[4]}")
    else:
        bot.send_message(message.chat.id, "Вы не искали ничего ;(")


def start_searching(message):
    bot.send_message(message.chat.id, "Идет поиск... 🔎")

    commands = message.text.split()
    requestDate = str(time.strftime("%m/%d/%Y, %H:%M:%S"))

    if commands[0] == str(historyKey):
        if len(commands) > 1:
            try:
                check_command(commands, message)
            except Exception as e:
                print(e)
                bot.send_message(message.chat.id, "Недействительный id")

        else:
            send_all_queries(message)
    else:
        find_image(message, requestDate)


@bot.message_handler(content_types=['text'])
def main(message):
    if message.chat.type == 'supergroup':
        if message.text.startswith('/'):
            start_searching(message)
        else:
            bot.reply_to(message, "Если хотит искать рисунки напишите /имя рисунка\n"
                                  "Например : /Dog")

    else:
        start_searching(message)


def check_command(commands, message):
    if commands[1] != "" and type(int(commands[1])) == int:
        results = get_query_by_id(commands[1])
        if len(results) != 0:
            for result in results:
                bot.send_message(message.chat.id,
                                 f"🌎 User id : {result[0]}\n"
                                 f"🕵️ ‍User name : {result[1]}\n"
                                 f"🔎 User query : {result[2]}\n"
                                 f"🧭 Query date: {result[3]}\n"
                                 f"👀 Query result : {result[4]}")
        else:
            bot.send_message(message.chat.id, "Ничего не нашлось по данному id")


def send_all_queries(message):
    queries = get_all_queries()
    if len(queries) != 0:
        for data in queries:
            bot.send_message(message.chat.id,
                             f"🌎 User id : {data[0]}\n"
                             f"🕵️ ‍User name : {data[1]}\n"
                             f"🔎 User query : {data[2]}\n"
                             f"🧭 Query date: {data[3]}\n"
                             f"👀 Query result : {data[4]}")
    else:
        bot.send_message(message.chat.id, "База данных пуст")


def find_image(message, request_date):
    images = find_image_by_name(message.text)['hits']
    if len(images) != 0:
        randomSingleImage = images[random.randint(0, len(images) - 1)]
        bot.send_photo(message.chat.id, photo=randomSingleImage['largeImageURL'])
        save_query_to_db(message.from_user.id, message.from_user.first_name, message.text,
                         randomSingleImage['largeImageURL'])

        if str(message.chat.id) != str(adminChatId):
            bot.send_message(adminChatId,
                             f"User named `{message.from_user.first_name}`\n"
                             f"Date {request_date}\n"
                             f"Searched `{message.text}` and get result: \n"
                             f" {randomSingleImage['largeImageURL']}")
        else:
            bot.send_message(message.chat.id, "Ой ой ничего не нашлось...")


def find_image_by_name(name):
    formatted = str(name).replace("/","")
    response = requests.get(f"https://pixabay.com/api/?key={apiKey}&q={formatted}")

    return json.loads(response.text)


def get_all_queries():
    connect = sqlite3.connect("queries.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM queries")
    data = cursor.fetchall()
    return data


def get_query_by_id(user_id):
    connect = sqlite3.connect("queries.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM queries WHERE userId = {user_id}")
    data = cursor.fetchall()
    return data


def save_query_to_db(user_id, user_name, query, query_result):
    connect = sqlite3.connect("queries.db")
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS queries(userId,userName,query,date,queryResult)""")
    connect.commit()
    cursor.execute("INSERT INTO queries(userId,userName,query,date,queryResult) VALUES(?,?,?,?,?)",
                   (user_id, user_name, query, str(time.strftime("%m/%d/%Y, %H:%M:%S")), query_result,))

    connect.commit()


bot.infinity_polling()
