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
from navigation import *
from vspomogation import *
# !!!!!!! Надо сделать проверку на
# данные для доступа к боту.


token = "817361693:AAFadWYZfaDiu9YUTgvPnNvisdx7-SwYnL4"
bot = telebot.TeleBot(token)


# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
global operationlist     #Хранится словарь ChatID пользователя и название выполняемой операции.
operationlist = {}       #Справка:
operationlist[356080087] = ""
operationlist[315317443] = ""



#**********************************БЛОК УНИВЕРСАЛЬНЫХ ФУНКЦИЙ**************************************************

# Функция поиска.
def find(message, find_goose, user_type):
    gooses = read_db_array("goose", "name")
    findarray = []
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for goose in gooses:
        if str(find_goose).lower() in str(goose).lower():
            findarray.append(goose)
            callback_button = types.InlineKeyboardButton(text=goose,
                                                         callback_data="findgoose:" + str(goose) + ":"+str(user_type))
            keyboard.row(callback_button)
    callback_button = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
    keyboard.row(callback_button)
    bot.send_message(message.chat.id, "Найденные товары", reply_markup=keyboard)
    return findarray




# ************************************************************************************************
@bot.message_handler(commands=['reset3043198'])
def handle_start(message):
    deteterow_db_universe("user_base", "chat_id", message.chat.id)
    bot.send_message(message.chat.id, "Профиль удален!")



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

@bot.message_handler(commands=['start'])
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

# Шухерит нажатия на инлайн кнопки для функции "function_mother", которая передает значение по назначению.
@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] in markerlist)
def main_menu(call):
    print("input_for_function_mother")
    #Передает полный месседж во втором параметре.
    function_mother(call.data.split(":")[0], call)



#Обработчик основного меню и меню товаров
@bot.callback_query_handler(func=lambda call: "changemenu" in call.data)
def change_menu(call):
    if "Back" in call.data:
        call.data = call.data[5:]
        print(call.data)
    # Обрабатываем входящий коллбэк формата changemenu:"Название кнопки"
    menu1 = call.data.split(":")[1]
    # Если основная часть меню, основанная на БД Menulist
    if menu1 in set(read_db_array("menulist","menu")):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        menulist = read_db_array("menulist", "next_menu", menu=menu1)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for menu in menulist:
            callback_button = types.InlineKeyboardButton(text=menu, callback_data="changemenu:" + str(menu))
            keyboard.row(callback_button)
        # Добавляем к списку меню кнопку "Назад"
        callback_button = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        keyboard.row(callback_button)
        bot.send_message(call.message.chat.id, "<b>"+menu1+"</b>", reply_markup=keyboard, parse_mode="HTML")

    # Если вспомогательная часть меню, основанная на БД Goose
    elif menu1 in set(read_db_array("goose", "category")):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        brands = read_db_array('goose', "brand", category=str(menu1))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for brand in set(brands):
            callback_button = types.InlineKeyboardButton(text=brand, callback_data="changemenu:" + str(brand))
            keyboard.row(callback_button)
        # Добавляем к списку меню кнопку "Назад"
        callback_button = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        keyboard.row(callback_button)
        bot.send_message(call.message.chat.id, "<b>" + menu1 + "</b>", reply_markup=keyboard, parse_mode="HTML")

    # Вывод перечня производителей.
    elif menu1 in set(read_db_array("goose", "brand")):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        gooses = read_db_array('goose', "name", brand=str(menu1))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for goose in set(gooses):
            callback_button = types.InlineKeyboardButton(text=goose, callback_data="changemenu:" + str(goose))
            keyboard.row(callback_button)
        # Добавляем к списку меню кнопку "Назад"
        callback_button = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        keyboard.row(callback_button)
        bot.send_message(call.message.chat.id, "<b>" + menu1 + "</b>", reply_markup=keyboard, parse_mode="HTML")

    # Вывод информации о товаре.
    elif menu1 in set(read_db_array("goose", "name")):

        goose_info = read_db_row("goose", name=menu1)
        goose_message = ""
        item1 = ""
        goose_id = goose_info['id']
        print(goose_id)
        for item in goose_info:
            if item == "category":
                item1 = "Категория"
            if item == "brand":
                item1 = "Производитель"
            if item == "name":
                item1 = "Модель"
            if item == "description":
                item1 = "Краткое описание"
            if item == "site_url":
                item1 = "Ссылка на сайт"
            if item == "video_url":
                item1 = "Ссылка на видео"
            if item == "text":
                item1 = "Расширенное описание"
            if item == "features":
                item1 = "Особенности"
            if item == "comments":
                item1 = "Примечания"
            goose_message += "<b>" + str(item1) + "</b>" + "\n" + str(goose_info[item]) + "\n"

        # +Добавляем кнопку "Закрыть и Добавить примечание"
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
        callback_button1 = types.InlineKeyboardButton(text="Примечание",
                                                      callback_data="Добавить примечание:Юзер:"+str(goose_id))
        keyboard.add(callback_button)
        keyboard.add(callback_button1)
        # Cообщение вывода информации о товаре.
        bot.send_message(call.message.chat.id, goose_message, parse_mode="HTML", disable_web_page_preview=True,reply_markup=keyboard)

    # Режим добавления товара. Включен/выключен.
    elif menu1 == "Добавить товар":
        status = read_db_row("menulist", menu="Добавление товара")['next_menu']
        if status == "On":
            write_db_update_ultimate('menulist', find__menu="Добавление товара", next_menu="Off")
            bot.answer_callback_query(callback_query_id=call.id,
                                      text="Режим добавления товара выключен",
                                      show_alert=True)
        else:
            write_db_update_ultimate('menulist', find__menu="Добавление товара", next_menu="On")
            bot.answer_callback_query(callback_query_id=call.id,
                                      text="Теперь можно добавлять товар.\nПеретяните Excel документ в любое время в чат.\nНе забудьте выключить после использования.",
                                      show_alert=True)


    # Если вспомогательная часть меню, основанная на БД TESTS
    elif menu1 in read_db_array("tests", "type"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        category = read_db_array('tests', "category")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for cat in set(category):
            callback_button = types.InlineKeyboardButton(text=cat, callback_data="changetestmenu:" + str(cat))
            print(str(cat))
            keyboard.row(callback_button)
        # Добавляем к списку меню кнопку "Назад"
        callback_button = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        keyboard.row(callback_button)
        bot.send_message(call.message.chat.id, "<b>" + "Все вопросы" + "</b>", reply_markup=keyboard, parse_mode="HTML")


    # Если нечего показать - выводим сообщение о том, что "Скоро будет"
    else:
        bot.answer_callback_query(callback_query_id=call.id, text="Coming soon...", show_alert=True)

#бработчик меню тестирования
@bot.callback_query_handler(func=lambda call: "changetestmenu" in call.data)
def change_test_menu(call):
    if "Back" in call.data:
        call.data = call.data[5:]
        print(call.data)
    print(call.data)

    menu0 = call.message.text
    print("Предыдущее меню"+menu0)
    menu1 = call.data.split(":")[1]
    print("Следующее меню" + menu1)
    # Вывод перечня производителей или названий глав.
    if menu1 in read_db_array("tests", "category"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        tests = read_db_array('tests', "brand_or_chapter", category=str(menu1))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for test in set(tests):
            callback_button = types.InlineKeyboardButton(text=test, callback_data="changetestmenu:" + str(test))
            keyboard.row(callback_button)
        # Добавляем к списку меню кнопку "Назад"
        callback_button = types.InlineKeyboardButton(text="Назад", callback_data="Back:"+"changemenu:" + str(menu0))
        keyboard.row(callback_button)
        bot.send_message(call.message.chat.id, "<b>" + menu1 + "</b>", reply_markup=keyboard, parse_mode="HTML")
    #Вывод названий тестов
    elif "Сделать по бренду или главе" in menu1: #(read_db_array("tests", "brand_or_chapter"))):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        tests = read_db_array('tests', "test_name", brand_or_chapter=str(menu1))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for test in set(tests):
            callback_button = types.InlineKeyboardButton(text=test, callback_data="changetestmenu:" + str(test))
            keyboard.row(callback_button)
        # Добавляем к списку меню кнопку "Назад"
        callback_button = types.InlineKeyboardButton(text="Назад", callback_data="Back:"+"changetestmenu:" + str(menu0))
        keyboard.row(callback_button)
        bot.send_message(call.message.chat.id, "<b>" + menu1 + "</b>", reply_markup=keyboard, parse_mode="HTML")
    #Обработка нажатия кнопки с выбором теста.
    elif menu1 in set(read_db_array("tests", "test_name")):
        pass

    # Если нечего показать - выводим сообщение о том, что "Скоро будет"
    else:
        bot.answer_callback_query(callback_query_id=call.id, text="Coming soon...", show_alert=True)




# Обработка поиска!
# Тут мы обрабатываем текст, который ввел пользователь и выводим список товара.
@bot.message_handler(content_types=['text'], func=lambda message: "Ввод названия товара для поиска" in str(operationlist[message.chat.id]))
def find_goose(message):
    find(message, message.text, "Юзер")
    operationlist[message.chat.id] = ""


# Обработка нажатия на найденный товар.
@bot.callback_query_handler(func=lambda call: "findgoose" in call.data)
def find_goose_operation(call):
    # Разбиваем коллбэк на данные
    goose_name = call.data.split(":")[1]
    user_type = call.data.split(":")[2]
    if user_type == "Юзер":
        goose_info = read_db_row("goose", name=goose_name)
        goose_message = ""
        item1 = ""
        for item in goose_info:
            if item == "category":
                item1 = "Категория"
            if item == "brand":
                item1 = "Производитель"
            if item == "name":
                item1 = "Модель"
            if item == "description":
                item1 = "Краткое описание"
            if item == "site_url":
                item1 = "Ссылка на сайт"
            if item == "video_url":
                item1 = "Ссылка на видео"
            if item == "text":
                item1 = "Расширенное описание"
            if item == "features":
                item1 = "Особенности"
            if item == "comments":
                item1 = "Примечания"
            goose_message += "<b>" + str(item1) + "</b>" + "\n" + str(goose_info[item]) + "\n"
        # +Добавляем кнопку "Закрыть и Добавить примечание"
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
        callback_button1 = types.InlineKeyboardButton(text="Примечание",
                                                      callback_data="Добавить примечание:Юзер:" + str(goose_info['id']))
        keyboard.add(callback_button)
        keyboard.add(callback_button1)
        # Cообщение вывода информации о товаре.
        bot.send_message(call.message.chat.id, goose_message, parse_mode="HTML", disable_web_page_preview=True,
                         reply_markup=keyboard)

#Редактировать примечание к товару.
@bot.callback_query_handler(func=lambda call: "Добавить примечание" in call.data)
def edit_comment(call):
    # Разбиваем коллбэк на данные
    user_type = call.data.split(":")[1]
    goose_id = call.data.split(":")[2]
    if user_type == "Юзер":
        bot.send_message(call.message.chat.id, "Введите Ваш комментарий формате Фамилия:Примечание ")
        operationlist[call.message.chat.id] = "Ввод примечания:"+str(goose_id)
    else:
        pass  # !!!!Добавление комментария для администратора. В перспективе возможность добавления модерации.


# Принимаем комментарий от пользователя и добавляем комментарий к БД
@bot.message_handler(func = lambda message: "Ввод примечания" in str(operationlist[message.chat.id]))
def edit_comment_confirm(message):
    #Разбиваем на данные
    goose_id = str(operationlist[message.chat.id]).split(":")[1]
    goose_comment = read_db_row("goose", id=goose_id)['comments']
    if "None" in str(goose_comment):
        goose_comment = ""
    goose_comment = str(goose_comment) + "\n"+message.text
    write_db_update_ultimate("goose", find__id=goose_id, comments=goose_comment)
    operationlist[message.chat.id] = ""
    msg = bot.send_message(message.chat.id, "Комментарий добавлен")
    time.sleep(1)
    bot.delete_message(message.chat.id, msg.message_id)



@bot.message_handler(commands=['12345'])
def test(message):
    pass
    view_test(message, '22', '1')

@bot.callback_query_handler(func=lambda call: "testform" in call.data)
def testform(call):
    testform_buttons_click(call.message, call.data, call)


if __name__ == '__main__':
    bot.polling(none_stop=True)
