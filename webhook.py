import telebot
import cherrypy
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
from test_func import *
from navigation import *
from vspomogation import *
# !!!!!!! Надо сделать проверку на
# данные для доступа к боту.


token = "817361693:AAFadWYZfaDiu9YUTgvPnNvisdx7-SwYnL4"
bot = telebot.TeleBot(token)


WEBHOOK_HOST = '213.226.124.119'
WEBHOOK_PORT = 443 # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '213.226.124.119'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '/SNtelebot/ssl/webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '/SNtelebot/ssl/webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            print(json_string)
            return ''
        else:
            raise cherrypy.HTTPError(403)



# ************************************************************************************************
@bot.message_handler(func=lambda message: True, commands=['reset3043198'])
def handle_start(message):
    deteterow_db_universe("user_base", "chat_id", message.chat.id)
    bot.send_message(message.chat.id, "Профиль удален!")

# ************************************************************************************************
@bot.message_handler(func=lambda message: True, commands=['main'])
def handle_start(message):
    write_db_update_ultimate("user_base", find__chat_id=message.chat.id, operation="mainmenu")
    main_menu_to_user(message=message)



# *************Блок регистрации************

# Обход бага пустого operation
@bot.message_handler(func=lambda message: message.chat.id not in read_db_array("user_base", "chat_id"))
def new_user0(message):
    print("new_user0")
    write_db_insert("user_base", chat_id=message.chat.id, operation="Register")
    handle_start(message)

# Обработка обычных сообщений
@bot.message_handler(content_types=['text'], func=lambda message: "Register" in str(read_db_row("user_base", chat_id=message.chat.id)['operation']))
def new_user1(message):
    print("new_user1")
    registration_new_user(message=message)
    #main_menu_to_user(message=message)

# Обработка callback сообщений
@bot.callback_query_handler(func=lambda call: "Register" in str(read_db_row("user_base", chat_id=call.message.chat.id)['operation']))
def new_user2(call):
    print("new_user2")
    registration_new_user(call=call)


# ************************************************************************************************

# *************Блок ниверсальных кнопок************

# Показать кнопку отображения главного меню по команде "Старт"

@bot.message_handler(func=lambda message: True, commands=['start'])
def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text="Главное меню")
    keyboard.add(button1)
    bot.send_message(message.chat.id, "Это база-знаний компании SigaretNet.by. Добро пожаловать", reply_markup=keyboard)
    registration_new_user(message=message)



# Обрабатываем нажатие кнопки "Закрыть"
@bot.callback_query_handler(func=lambda call: "Закрыть" in call.data)
def close(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    write_db_update_ultimate("user_base", find__chat_id=call.message.chat.id, operation="mainmenu")
    #main_menu_to_user(message=call.message)


# ************************************************************************************************



# Шухерит нажатия на инлайн кнопки для функции "function_mother", которая передает значение по назначению.
@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] in markerlist)
def main_menu(call):
    print("input_for_function_mother")
    #Передает полный месседж во втором параметре.
    function_mother(call.data.split(":")[0], call)


# *************Блок главного меню************

@bot.message_handler(content_types=['text'], func=lambda message: str(read_db_row("user_base", chat_id=message.chat.id)['operation']) == "mainmenu")
def main_menu(message):
    print("main_menu")
    main_menu_to_user(message=message)

@bot.callback_query_handler(func=lambda call: str(read_db_row("user_base", chat_id=call.message.chat.id)['operation']) == "mainmenu")
def main_menu(call):
    print("main_menu")
    main_menu_to_user_onclick(call)

@bot.callback_query_handler(func = lambda call: str(read_db_row("user_base", chat_id=call.message.chat.id)['operation']) == "submainmenu")
def main_menu(call):
    print("submainmenu")
    main_menu_to_user_onclick(call)



# ************************************************************************************************


# *************Обработчик ввода для конечных функций("function_father")************

# Шухерит введенные сообщения для функции "function_father", которая передает значение по назначению.
@bot.message_handler(content_types=['text'], func=lambda message: str(read_db_row("user_base", chat_id=message.chat.id)['operation']) in functionlist)
def main_menu(message):
    print("input_for_function_father")
    function_father(str(read_db_row("user_base", chat_id=message.chat.id)['operation']), message)

# Шухерит нажатия на инлайн кнопки для функции "function_father", которая передает значение по назначению.
@bot.callback_query_handler(func=lambda call: str(read_db_row("user_base", chat_id=call.message.chat.id)['operation']) in functionlist)
def main_menu(call):
    print("input_for_function_father")
    #Передает полный месседж во втором параметре.
    function_father(str(read_db_row("user_base", chat_id=call.message.chat.id)['operation']), call)

# Шухерит отосланные документы для функции "function_father", которая передает значение по назначению.
@bot.message_handler(content_types=['document'], func=lambda message: str(read_db_row("user_base", chat_id=message.chat.id)['operation']) in functionlist)
def main_menu(message):
    print("input_for_function_father")
    #Передает полный месседж во втором параметре.
    function_father(str(read_db_row("user_base", chat_id=message.chat.id)['operation']), message)

# ************************************************************************************************




# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

 # Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))


# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})