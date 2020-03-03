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
from test_func import *

token = "817361693:AAFadWYZfaDiu9YUTgvPnNvisdx7-SwYnL4"
bot = telebot.TeleBot(token)



def input_document_question(message):
    # Получаем и сохраняем отправленный в телеграм файл.
    name = message.document.file_name
    document = message.document.file_id
    file_info = bot.get_file(document)
    downloaded_file = bot.download_file(file_info.file_path)
    new_path = "/SNtelebot/learnbot/download/" + name
    with open(new_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Обрабатываем Excel документ
    excel = openpyxl.load_workbook(new_path)
    sheet = excel.get_sheet_by_name("Тест")
    question = {}
    answer = {}
    # Цикл, который перебирает блоки вопросов.
    # Формируем переменные, которые будут испольщованы в подтвеждении загрузки теста
    text = "Вопрос загружен успешно!\n"
    test_ids = []
    num = 1
    for count in range(1, 5000, 22):
        count = count+1
        if sheet['A%s'%(count)].value is not None:
            # Записывем данные ячеек в переменные.
            category = sheet['A%s' % count].value
            brandorchapter = sheet['A%s' % (count+2)].value.replace('"', "*").replace("'", "*")
            name = sheet['A%s' % (count+4)].value.replace('"', "*").replace("'", "*")
            print(count)
            print(name)
            tags = sheet['A%s' % (count+6)].value.replace('"', "*").replace("'", "*")
            quest = str(sheet['A%s' % (count+8)].value).replace('"', "*").replace("'", "*")
            answer[1] = str(sheet['A%s' % (count+10)].value).replace('"', "*").replace("'", "*")
            answer[2] = str(sheet['A%s' % (count+12)].value).replace('"', "*").replace("'", "*")
            answer[3] = str(sheet['A%s' % (count+14)].value).replace('"', "*").replace("'", "*")
            answer[4] = str(sheet['A%s' % (count+16)].value).replace('"', "*").replace("'", "*")
            answer[5] = str(sheet['A%s' % (count+18)].value).replace('"', "*").replace("'", "*")
            #AJhv
            trueanswers_string = str(sheet['A%s' % (count+20)].value)
            trueanswers = trueanswers_string.split("*")
            trueanswers_int = []
            for trueanswer in trueanswers:
                trueanswers_int.append(int(trueanswer))

            #формируем словарь question для передачи в Базу данных
            question['type'] = "Тестирование"
            question['category'] = str(category)
            question['brand_or_chapter'] = str(brandorchapter)
            question['test_name'] = str(name)
            question['tag'] = str(tags)
            question['question'] = str(quest)
            question['answers'] = answer
            question['truenumbers'] = str(trueanswers_int)
            print(question)
            write_db_insert("tests", dictionary=question)
            # Дополняем текст подтверждающего сообщения.

            text += "\n" + str(num) + ". " + str(question["question"])
            test_ids.append(read_db_row("tests", question=question['question'])['id'])
            num += 1
        else:
            pass
    bd_id = write_db_insert("utility", operand="test_ids", value=test_ids, comment="Удалить вопросы")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text="Добавить", callback_data="Добавить:" + str(bd_id))
    callback_button1 = types.InlineKeyboardButton(text="Удалить", callback_data="Удалить вопросы:" + str(bd_id))
    keyboard.add(callback_button, callback_button1)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    # Удаляем уже ненужный файл.
    os.remove(new_path)


def remove_question(call):

    bd_id = call.data.split(":")[1]
    bd_id_info = read_db_row("utility", id=bd_id)
    value = bd_id_info['value']
    value = ast.literal_eval(value)
    for val in value:
        print("Удалить вопрос" + str(val))
        deteterow_db_universe('tests', "id", str(val))
    # Удаление добавленной записи товара из БД
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(callback_query_id=call.id,
                              text="Все загруженные вопросы удалены. Нажмите 'Главное меню' для выхода из режима"
                                   "добавления вопросов или попробуйте загрузить заново...",
                              show_alert=True)
    deteterow_db_universe('utility', "id", bd_id)

def confirm_question(call):
    bd_id = call.data.split(":")[1]
    deteterow_db_universe('utility', "id", bd_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(callback_query_id=call.id,
                              text="Все вопросы успешно добавлены. Нажмите 'Главное меню' для выхода из режима"
                                   " добавления вопросов или загрузите еще...",
                              show_alert=True)



# Загрузка шаблона EXCEL с карточкой товара(Срабатывает только если включен режим добавления товара)
def input_document_goose(message):
    # Получаем и сохраняем отправленный в телеграм файл.
    name = message.document.file_name
    document = message.document.file_id
    file_info = bot.get_file(document)
    downloaded_file = bot.download_file(file_info.file_path)
    new_path = ".\\download\\" + name
    with open(new_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Обрабатываем Excel документ
    excel = openpyxl.load_workbook(new_path)
    sheet = excel.get_sheet_by_name("Товар")
    goose = {}
    goose['category'] = sheet['A2'].value
    goose['brand'] = sheet['A4'].value
    goose['name'] = sheet['A6'].value
    goose['description'] = sheet['A8'].value
    goose['site_url'] = sheet['A10'].value
    goose['video_url'] = sheet['A12'].value
    goose['text'] = sheet['A14'].value
    goose['features'] = sheet['A16'].value
    goose['comments'] = sheet['A18'].value
    write_db_insert("goose", dictionary = goose)

    # Удаляем уже ненужный файл.
    os.remove(new_path)

    # Выводим сообщение о подтверждении загрузки файла.
    text = "Файл загружен успешно!\n"
    for key in goose:
        text += "\n"+key.split("(")[0]+": "+str(goose[key])

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text="Оставить", callback_data="Оставить")
    callback_button1 = types.InlineKeyboardButton(text="Удалить", callback_data="Удалить товар:"+str(goose['name']))
    keyboard.add(callback_button, callback_button1)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

def remove_goose(call):
    goosename = call.data.split(":")[1]
    # Удаление добавленной записи товара из БД
    deteterow_db_universe('goose', "name", goosename)
    bot.edit_message_text("Удалено!", call.message.chat.id, call.message.message_id)
    time.sleep(2)
    bot.delete_message(call.message.chat.id, call.message.message_id)

def confirm_goose(call):
    bot.edit_message_text("Sucsess!",call.message.chat.id, call.message.message_id)
    time.sleep(2)
    bot.delete_message(call.message.chat.id, call.message.message_id)