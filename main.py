import requests
import telebot
import telebot
import json

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
        if len(find_image_by_name(message.text)['hits']) != 0:
            for image in find_image_by_name(message.text)['hits']:
                bot.send_photo(message.chat.id, photo=image['largeImageURL'])
            bot.send_message(message.chat.id, "Это все что я нашел.")

        else:
            bot.send_message(message.chat.id, "Ой ой ничего не нашлось...")
    except:
        bot.send_message(message.chat.id, "Ой что-то пошло не так 🤔")


def find_image_by_name(name):
    response = requests.get(f"https://pixabay.com/api/?key={apiKey}&q={name}&total=5")
    return json.loads(response.text)


bot.infinity_polling()
