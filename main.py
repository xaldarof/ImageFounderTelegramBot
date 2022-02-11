import telebot
import telebot
import json

botToken = "5285770077:AAFvGmK28FYcfVkm4Q6vMAgie8WHsHUt6II"

bot = telebot.TeleBot(botToken)


@bot.message_handler(commands=['start'])
def entrance(message):
    bot.send_message(message.chat.id, "Hello send me image name and found image by name 😊")


def find_image_by_name():

bot.infinity_polling()
