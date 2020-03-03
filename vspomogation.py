import telebot
from telebot import types
import pymysql
import pymysql.cursors
import ast
import datetime
from datetime import *
import time
from time import strftime
import bdfunc
from bdfunc import *
import os  # библиотека для работы с файлами и каталогами
import openpyxl  # библиотека для обработки Excel-файлов
import random
from test_func import * # Модуль функция для работы с тестированием.
from excel import * # Модуль функций для работы с Excel- документами.

markerlist = [
            # Авторизовать нового пользователя
            "Авторизация нового"
]

def function_mother(input_call, input_message):

    if input_call in markerlist:
        data = input_call
    else:
        data = ""
    print(data)
    if input_message is None:
        input_message = ""

    # Дополнительные функции
        # Авторизовать нового пользователя
    if "Авторизация нового" in data:
        autorisation_user(input_call, input_message)



# Функция авторизует пользователя.
def autorisation_user(input_call, input_message):
    try:
        call = input_message
        user_id = call.data.split(":")[1]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        user_info = read_db_row("user_base", chat_id=user_id)
        if user_info['status'] == "confirm":
            bot.send_message(call.message.chat.id, "Кто-то уже авторизовал пользователя до вас.")
        else:
            write_db_update_ultimate("user_base", find__chat_id=user_id, status="confirm", operation='mainmenu')
            bot.send_message(user_id, "Вы авторизованы. Можете нажать Главное меню и начать пользоваться")
            bot.send_message(call.message.chat.id, "Польщователь авторизован и извещен об этом сообщением")

    except:
        print("Что-то пошло не так с подтверждением авторизации нового пользователя.")
