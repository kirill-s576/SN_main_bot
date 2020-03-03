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
from math import radians, cos, sin, asin, sqrt

# Объявляем токен бота.
token = "385467625:AAF8EjbdekUijHlaXlcrdkh4jwPAqatCrzs"
bot = telebot.TeleBot(token)

shop_latlong = {"Skala": "53.908809, 27.469838",
                "Titan": "53.860556, 27.479068",
                "Siluet": "53.916268, 27.579516",
                "Bigz": "53.964146, 27.623896",
                "Riga": "53.928764, 27.587658"}

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

@bot.message_handler(commands=["start"])
def start(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Какой ближайший магазин", request_location=True)
    keyboard.add( button_geo)
    bot.send_message(message.chat.id, "Нажми кнопку и получи ближайший магазин", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def msg(message):
    lat = message.location.latitude
    lon = message.location.longitude

    shop = ""
    cord1 = ""
    cord2 = ""
    lat1 = 0
    lat2 = 0
    lon1 = 0
    lon2 = 0
    for i in shop_latlong:
        if shop == "":
            cord1 = "0,0"
        else:
            cord1 = str(shop_latlong[shop])
            lat1 = float(cord1.split(",")[0])
            lon1 = float(cord1.split(",")[1])

        cord2 = str(shop_latlong[i])
        lat2 = float(cord2.split(",")[0])
        lon2 = float(cord2.split(",")[1])

        c1 = haversine(lat, lon, lat1, lon1)
        c2 = haversine(lat1, lon1, lat2, lon2)
        if c1 > c2:
            shop = i
        else:
            shop = shop

    print(shop)
    final_cord = shop_latlong[shop]
    final_lat = float(final_cord.split(",")[0])
    final_lon = float(final_cord.split(",")[1])
    url = "https://yandex.by/maps/157/minsk/?ll=" + str(final_lon) + "%2C" + str(final_lat) + "&mode=search&oid=60035317958&ol=biz&sll=" + str(final_lon) + "%2C" + str(final_lat) + "&sspn=0.005212%2C0.002582&text=sigaretnetby"
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url=url)
    keyboard.add(url_button)
    bot.send_message(message.chat.id, shop, reply_markup=keyboard)
    bot.send_location(message.chat.id, final_lat, final_lon)

if __name__ == '__main__':
    bot.polling(none_stop=True)