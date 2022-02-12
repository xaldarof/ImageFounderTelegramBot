import json
import random
import time

import requests
import telebot
import os
import sqlite3

apiKey = os.getenv("api", "")
botToken = os.getenv("botToken", "")
historyKey = os.getenv("historyKey", "")

bot = telebot.TeleBot(botToken)


@bot.message_handler(commands=['start'])
def entrance(message):
    bot.send_message(message.chat.id, "Привет отправь мне имя картинки и я найду его 😊")


@bot.message_handler(content_types=['text'])
def main(message):
    bot.send_message(message.chat.id, "Идет поиск... 🔎")

    try:
        if message.text == str(historyKey):
            for data in get_all_queries():
                bot.send_message(message.chat.id,
                                 f"🌎 User id : {data[0]}\n"
                                 f"🕵️ ‍User name : {data[1]}\n"
                                 f"🔎 User query : {data[2]}\n"
                                 f"🧭 Query date: {data[3]}"
                                 f"👀 Query result : {data[4]}")

        else:
            images = find_image_by_name(message.text)['hits']
            if len(images) != 0:
                randomSingleImage = images[random.randint(0, len(images) - 1)]
                bot.send_photo(message.chat.id, photo=randomSingleImage['largeImageURL'])
                save_query_to_db(message.from_user.id, message.from_user.first_name, message.text,
                                 randomSingleImage['largeImageURL'])

            else:
                bot.send_message(message.chat.id, "Ой ой ничего не нашлось...")

    except Exception as error:
        if message.chat.id == 714707550:
            bot.send_message(message.chat.id, str(error))

        bot.send_message(message.chat.id, "Ой что-то пошло не так 🤔")

def find_image_by_name(name):
    response = requests.get(f"https://pixabay.com/api/?key={apiKey}&q={name}")
    return json.loads(response.text)


def get_all_queries():
    connect = sqlite3.connect("queries.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM queries")
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
