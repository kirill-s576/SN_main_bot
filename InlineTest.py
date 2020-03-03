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

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb = types.InlineKeyboardMarkup()
    # Добавляем колбэк-кнопку с содержимым "test"
    kb.add(types.InlineKeyboardButton(text="Без проблем.", callback_data="test"))
    kb.add(types.InlineKeyboardButton(text="Нет, спасибо.", callback_data="no"))
    results = []
    single_msg = types.InlineQueryResultArticle(
        id="1", title="Опрос",
        input_message_content=types.InputTextMessageContent(message_text="Добрый день. \n Я система автоматического опроса SigaretNet.by \n Ответьте пожалуйста на 3 вопроса. "),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    # Если сообщение из инлайн-режима
    if call.inline_message_id:
        if call.data == "test":
            kb = types.InlineKeyboardMarkup()
            # Добавляем колбэк-кнопку с содержимым "test"
            kb.add(types.InlineKeyboardButton(text="До 30", callback_data="after 30"))
            kb.add(types.InlineKeyboardButton(text="Больше 30", callback_data="before 30"))
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Сколько вам лет?", reply_markup= kb)
        elif call.data == "no":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Окей. Может быть в соедующий раз... :(")


        elif call.data == "before 30":
            kb = types.InlineKeyboardMarkup()
            # Добавляем колбэк-кнопку с содержимым "test"
            kb.add(types.InlineKeyboardButton(text="Да", callback_data="avto"))
            kb.add(types.InlineKeyboardButton(text="Нет", callback_data="no avto"))
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Вы водите машину?", reply_markup=kb)
        elif call.data == "after 30":
            kb = types.InlineKeyboardMarkup()
            # Добавляем колбэк-кнопку с содержимым "test"
            kb.add(types.InlineKeyboardButton(text="Да", callback_data="lisina"))
            kb.add(types.InlineKeyboardButton(text="Нет", callback_data="no lisina"))
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="У вас уже есть лысина?", reply_markup=kb)

        elif call.data == "lisina":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Очень жаль")
        elif call.data == "no lisina":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Очень рад за вас")

        elif call.data == "avto":
            kb = types.InlineKeyboardMarkup()
            # Добавляем колбэк-кнопку с содержимым "test"
            kb.add(types.InlineKeyboardButton(text="Легковая", callback_data="small"))
            kb.add(types.InlineKeyboardButton(text="Что-то побольше", callback_data="big"))
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Это легковая машина или что-то побольше?", reply_markup=kb)

        elif call.data == "small":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="https://ru.wikipedia.org/wiki/%D0%9B%D0%B5%D0%B3%D0%BA%D0%BE%D0%B2%D0%BE%D0%B9_%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C")
        elif call.data == "big":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="https://ru.wikipedia.org/wiki/%D0%92%D0%BD%D0%B5%D0%B4%D0%BE%D1%80%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA")



        elif call.data == "no avto":
            kb = types.InlineKeyboardMarkup()
            # Добавляем колбэк-кнопку с содержимым "test"
            kb.add(types.InlineKeyboardButton(text="Да", callback_data="plan"))
            kb.add(types.InlineKeyboardButton(text="Нет", callback_data="no plan"))
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="А планируете в ближайшее время?", reply_markup=kb)

        elif call.data == "plan":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Молодец")
        elif call.data == "big":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Очень жаль")



if __name__ == '__main__':
    bot.polling(none_stop=True)