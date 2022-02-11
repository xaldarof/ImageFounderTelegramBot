import json
import random
import requests
import telebot

botToken = "5285770077:AAFvGmK28FYcfVkm4Q6vMAgie8WHsHUt6II"
apiKey = "18372265-23dd084a52fad58a52dd60195"

bot = telebot.TeleBot(botToken)


@bot.message_handler(commands=['start'])
def entrance(message):
    bot.send_message(message.chat.id, "Привет отправь мне имя картинки и я найду его 😊")


@bot.message_handler(content_types=['text'])
def main(message):
    bot.send_message(message.chat.id, "Идет поиск... 🔎")

    try:
        images = find_image_by_name(message.text)['hits']
        if len(images) != 0:
            randomSingleImage = images[random.randint(0, len(images) - 1)]
            bot.send_photo(message.chat.id, photo=randomSingleImage['largeImageURL'])

        else:
            bot.send_message(message.chat.id, "Ой ой ничего не нашлось...")
    except:
        bot.send_message(message.chat.id, "Ой что-то пошло не так 🤔")


def find_image_by_name(name):
    response = requests.get(f"https://pixabay.com/api/?key={apiKey}&q={name}&total=5")
    return json.loads(response.text)


bot.infinity_polling()
