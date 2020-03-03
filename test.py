import telebot
from telebot import types
import pymysql
import pymysql.cursors
import ast
import datetime
from datetime import *
import time
from time import strftime
import asana2
from asana2 import *
import bdfunc
from bdfunc import *


token = "385467625:AAF8EjbdekUijHlaXlcrdkh4jwPAqatCrzs"
bot = telebot.TeleBot(token)




@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Example bot.
What's your name?
""")




def test(message):
    bot.send_message(message.chat.id, "12345")


if __name__ == '__main__':
    bot.polling(none_stop=True)