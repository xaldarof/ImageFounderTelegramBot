import json
import random
import sqlite3
import time

import requests
import telebot

# apiKey = os.getenv("api", "")
# botToken = os.getenv("botToken", "")
# historyKey = os.getenv("historyKey", "")
botToken = "5285770077:AAFvGmK28FYcfVkm4Q6vMAgie8WHsHUt6II"
apiKey = "18372265-23dd084a52fad58a52dd60195"
historyKey = "123"

bot = telebot.TeleBot(botToken)


@bot.message_handler(commands=['start'])
def entrance(message):
    bot.send_message(message.chat.id, "Привет отправь мне имя картинки и я найду его 😊")


@bot.message_handler(content_types=['text'])
def main(message):
    bot.send_message(message.chat.id, "Идет поиск... 🔎")

    commands = message.text.split(' ')

    if commands[0] == str(historyKey):
        if len(commands) > 1:
            try:
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
            except:
                bot.send_message(message.chat.id, "Недействительный id")

        else:
            for data in get_all_queries():
                bot.send_message(message.chat.id,
                                 f"🌎 User id : {data[0]}\n"
                                 f"🕵️ ‍User name : {data[1]}\n"
                                 f"🔎 User query : {data[2]}\n"
                                 f"🧭 Query date: {data[3]}\n"
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


def find_image_by_name(name):
    response = requests.get(f"https://pixabay.com/api/?key={apiKey}&q={name}")
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
