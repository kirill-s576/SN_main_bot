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
from math import radians, cos, sin, asin, sqrt





token = "887034287:AAEXBOlrOcazilvc-BkUTxeWTXg-6Xis86o"
bot = telebot.TeleBot(token)


WEBHOOK_HOST = '213.226.124.119'
WEBHOOK_PORT = 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '213.226.124.119'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '/SNtelebot/ssl/webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '/SNtelebot/ssl/webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)

# Функция подсчета расстояния между объектами по координатам
def haversine(lat1, lon1, lat2, lon2):


    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


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
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(commands=["start"])
def start(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Какой ближайший магазин?", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Я могу помочь с поиском ближайшего магазина.", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    # Массив с геолокациями всех магазинов
    geo_array = read_db_array_universe("geolocation", "shop_location")
    # Формируем словарь, в котором ключ- расстояние от точки, аргумент - геолокация.

    range_dict = {}
    for i in geo_array:
        #Вытаскиваем координаты объека из списка.
        cord1 = str(i)
        lat1 = float(cord1.split(",")[0])
        lon1 = float(cord1.split(",")[1])
        # Вычисляем расстояние до него.
        c = haversine(lat, lon, lat1, lon1)
        range_dict[c] = i
    print(range_dict)
    # Находим ключ с минимальным значением.

    minkey = 0
    for key in range_dict:
        if minkey == 0:
            minkey = key
        elif key < minkey:
            minkey = key
    # Берем все данные объекта по минимальному ключу
    object1 = read_db_row("geolocation", shop_location = range_dict[minkey])
    print(object1)
    # И все ключи со значением не более, чем на 2 Км больше.
    other_keys = []
    for key in range_dict:
        if key < (minkey + 2):
            other_keys.append(key)
    print(other_keys)

    # Формируем и отправляем сообшение с ближайшим магазином.
    picture_url = '<a href=' + '"' +str(object1["shop_picture_url"]) + '"' + '>.</a>'
    site_url = object1["shop_site_url"]
    message_text = object1["shop_name"] + "\n" + object1["shop_adress"] + "\n" + object1["shop_name"] + "\n" \
                   + "Время работы: " + str(object1["shop_opentime"])[:-3] + " - " + str(object1["shop_closetime"])[:-3] + "\n" \
                    + "Расстояние до магазина: " + str(minkey)[0:3] + "км."
    keyboard = types.InlineKeyboardMarkup()
    geo_button = types.InlineKeyboardButton(text="Показать на карте", callback_data="location:"+str(object1["shop_location"]))
    site_button = types.InlineKeyboardButton(text="Ссылка на сайт", url=site_url)
    phone_button = types.InlineKeyboardButton(text="Узнать наличие", callback_data = "phone")
    keyboard.add(geo_button)
    keyboard.add(site_button)
    keyboard.add(phone_button)
    bot.send_message(message.chat.id, message_text + picture_url, reply_markup=keyboard, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: "location" in call.data)
def view_location(call):
    loc = call.data.split(":")[1]
    lat = loc.split(",")[0]
    lon = loc.split(",")[1]
    bot.send_location(call.message.chat.id, lat, lon)

@bot.callback_query_handler(func=lambda call: "phone" in call.data)
def phone(call):
    # bot.send_message(call.message.chat.id, '<a href="tel:+375296621313">Нажми для звонка</a>', parse_mode="HTML")
    # bot.send_message(call.message.chat.id, '<a href="tel:+375296621313">Нажми для звонка</a>', parse_mode="HTML")

    bot.send_message(call.message.chat.id,
        "Номер телефона колл-центра: \n Vel: [+375296621313](tel:+375296621313) \n MTC: [+375336621313](tel:+375336621313) \n Life :): [+375256621313](tel:+375256621313)",
        parse_mode='Markdown')
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