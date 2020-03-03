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
from test_func import * # Модуль функций для работы с тестированием.
from excel import * # Модуль функций для работы с Excel- документами.
from vspomogation import *

token = "817361693:AAFadWYZfaDiu9YUTgvPnNvisdx7-SwYnL4"
bot = telebot.TeleBot(token)

#Функции для регистрации нового пользователя.
#1. Попросить выбрать тип пользователя.
#2. Запросить пароль доступа. (Кстати сделать его(их) отдельно в базе данных с возможностью менять админу)
#3. Попросить ввести сначала полное имя. После номер телефона, внести все в БД.
#4. Поприветствовать и выкатить соответствующее меню.

#***********************
# Формат ввода (message = message, call = call)
def registration_new_user(**inputdata):
    pass
    # Смотрим что отправили в функции. Call или Message. Выдергиваем нужные значения.
    message = ""
    data = ""
    call = ""
    for key, value in inputdata.items():
        if key == "message":
            message = value
        elif key == "call":
            call = value
            message = call.message
            data = call.data
            bot.delete_message(message.chat.id, message.message_id)
        else:
            print("Ошибка ввода данных в функции регистрации")

    user_info = read_db_row("user_base", chat_id=message.chat.id)

    if (user_info['user_type'] is None) and (str(user_info['operation']) == "Register"):  # Проверяем есть ли пользователь в базе. user_info - вся строка из БД о пользователе.
        typeslist = read_db_array("user_types", "user_type")
        keyboard = types.InlineKeyboardMarkup()

        for type in typeslist:
            user_type_button = types.InlineKeyboardButton(text=str(type), callback_data="Register:type:" + str(type))
            keyboard.add(user_type_button)
        write_db_update_ultimate("user_base", find__chat_id=message.chat.id,
                                  operation="Register:typewait")
        bot.send_message(message.chat.id, "Выберите тип пользователя", reply_markup=keyboard)


    # Обработка коллбэка, если он есть
    if len(data) > 0:
        step = data.split(":")[1]
        callback = data.split(":")[2]
        if step == "type":
            write_db_update_ultimate("user_base", find__chat_id=message.chat.id,
                                                  user_type=str(callback), operation="Register:inputpassword")
            bot.send_message(message.chat.id, "Введите пароль пользователя:")

    if "inputpassword" in str(user_info['operation']):
        # Проверяем пароль на соответствие с инвайт-паролем в БД
        true_password = read_db_row("user_types", user_type=str(user_info['user_type']))['password']
        if message.text == true_password:
            newoperation = "Register:inputname"
            write_db_update_ultimate("user_base", find__chat_id=message.chat.id, operation=newoperation)
            bot.send_message(message.chat.id, "Введите полные ФИО:")
        else:
            bot.send_message(message.chat.id, "Пароль введен неверно. Повторите ввод.")

    elif "inputname" in str(user_info['operation']):
        name = message.text
        splitname = name.split(" ")
        if len(splitname) > 2:
            newoperation = "Register:inputphone"
            write_db_update_ultimate("user_base", find__chat_id=message.chat.id, full_name= name, operation=newoperation)
            bot.send_message(message.chat.id, "Введите свой номер телефона в формате 375291234567:")
        else:
            bot.send_message(message.chat.id, "Некорректный ввод имени. Требуются полные ФИО через пробел.")

    elif "inputphone" in str(user_info['operation']):
        phone = str(message.text)
        if (len(phone) == 12) and (phone[:-9] == "375"):
            newoperation = "moderwait"
            write_db_update_ultimate("user_base", find__chat_id=message.chat.id, phone_number=phone,
                                     operation=newoperation, status="modering")
            bot.send_message(message.chat.id, "Регистрация пройдена успешно. \n "
                                              "Вы сможете пользоваться сервисом как только "
                                              "Ваша заявка будет рассмотрена администратором.")
            admins = read_db_array("user_base", "chat_id", user_type="Администратор")
            if len(admins) > 0:

                for admin in admins:
                    user_info = read_db_row("user_base", chat_id=message.chat.id)
                    full_name = user_info['full_name']
                    keyboard = types.InlineKeyboardMarkup()
                    autorisation_button = types.InlineKeyboardButton(text="Авторизовать",
                                                                  callback_data="Авторизация нового:" + str(message.chat.id))
                    close_button = types.InlineKeyboardButton(text="Закрыть",
                                                                     callback_data="Закрыть")
                    keyboard.add(autorisation_button, close_button)
                    bot.send_message(admin, "Новый польователь %s ждет модерации профиля" % full_name, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Некорректный ввод номера")
    elif "moderwait" in str(user_info['operation']):
        bot.send_message(message.chat.id, "Ожидайте. \n "
                                          "Вы сможете пользоваться сервисом как только "
                                          "Ваша заявка будет рассмотрена администратором.")



#***********************


# Отображение основноно меню с для разного типа пользователей.
# Типы пользователей: Продавец, Стажер, Администратор, Модератор. Тип пользователя подтягивает из БД по chat_id.

def main_menu_to_user(**inputdata):
    #Выдергиваем исходные данные функции.
    message = ""
    data = ""
    call = ""
    for key, value in inputdata.items():
        if key == "message":
            message = value
        elif key == "call":
            call = value
            message = call.message
            data = call.data
            bot.delete_message(message.chat.id, message.message_id)
        else:
            print("Ошибка ввода данных в функции главного меню")

    # Меню, в котором мы находимся сейчас.
    nowmenu = message.text
    if nowmenu not in read_db_array("menulist", "menu"):
        nowmenu = "Главное меню"

    # Определяем тип пользователя.
    user_info = read_db_row("user_base", chat_id=str(message.chat.id))
    user_type = user_info['user_type']

    # Выводим перечень пунктов меню, котоырые доступны нашему пользователю.
    menulist = read_db_array_like("menulist", "next_menu", menu=nowmenu, user_type=user_type)
    keyboard = types.InlineKeyboardMarkup()
    for menu in menulist:
        menu_button = types.InlineKeyboardButton(text=str(menu), callback_data=str(menu))
        keyboard.add(menu_button)
    menu_button = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
    keyboard.add(menu_button)
    bot.send_message(message.chat.id, nowmenu, reply_markup=keyboard)


def main_menu_to_user_onclick(call):

    # Смотрим какое меню было предыдущим.
    previous_menu = call.message.text
    # Какое хотим отобразить следующим.
    nowmenu = call.data

    if nowmenu == "Главное меню":
        main_menu_to_user(call=call)
    # Обрабатываем нажатие кнопки "Назад"
    elif nowmenu == "Назад":
        try:
            nowmenu = read_db_row("menulist", next_menu=previous_menu)['menu']
            view_menu(call, nowmenu)
        except:
            main_menu_to_user(call=call)
    else:
        view_menu(call, nowmenu)


# Вспомогательная функция вывода меню.
def view_menu(call, nowmenu):
    # Данные пользователя
    chat_id = call.message.chat.id
    user_info = read_db_row("user_base", chat_id=chat_id)
    user_type = user_info['user_type']

    # Выводим перечень пунктов меню, котоырые доступны нашему пользователю.
    menulist = read_db_array_like("menulist", "next_menu", menu=nowmenu, user_type=user_type)
    if len(menulist) > 0:
        keyboard = types.InlineKeyboardMarkup()
        for menu in menulist:
            menu_button = types.InlineKeyboardButton(text=str(menu), callback_data=str(menu))
            keyboard.add(menu_button)
        # Добавляем "Назад"
        menu_button = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        keyboard.add(menu_button)
        # Добавляем "Закрыть"
        menu_button = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
        keyboard.add(menu_button)
        # Удаляем сообщение, из которого пришли.
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, nowmenu, reply_markup=keyboard)
    else:
        # Точка выхода из меню к исполняющим функциям.!!!!!!!!!
        function_father(call, None)

functionlist = [
    # Управление
        # База знаний
            "Добавить товар",
            "Редактировать товар",
            "Удалить товар",
        # Тестирование
            "Добавить вопросы",
            "Вcе вопросы",
            "Сделать по бренду или главе",
            "Сделать по тегу",
            "Сделать по названию теста",
            "Итоги тестов",
    # Использование
        # База знаний
            # Товар
            "Стартовые наборы",
            "Батарейные моды",
            "Атомайзеры",
            "Жидкости",
            "Поиск",
            # Стандарты работы
        # Тестирование
            "Надо пройти",
            "Результаты"
]
def function_father(input_call, input_message):

    if input_call in functionlist:
        data = input_call
    else:
        data = input_call.data
    print(data)
    if input_message is None:
        input_message = ""

    if data in functionlist:
        print("Есть такая функция.")

    # Управление
        # База знаний
        if data == "Добавить товар":
            pass
        elif data == "Редактировать товар":
            pass
        elif data == "Удалить товар":
            pass
        # Тесты
        elif data == "Добавить вопросы":
            add_new_questions(input_call, input_message)
        elif data == "Вcе вопросы":
            pass
        elif data == "Сделать по бренду или главе":
            pass
        elif data == "Сделать по тегу":
            pass
        elif data == "Сделать по названию теста":
            create_test_on_name(input_call, input_message)
        elif data == "Итоги тестов":
            admin_tests_result(input_call, input_message)
    #  Использование
        # База знаний
            # Товар

        elif data == "Сделать по названию теста":
            pass
        elif data == "Поиск":
            find_goose(input_call, input_message)
            # Стандарты работы

        # Тестирование
        elif data == "Надо пройти":
            view_test_and_start(input_call, input_message)
        elif data == "Результаты":
            pass

        elif data == "Стартовые наборы" or "Батарейные моды" or "Атомайзеры" or "Жидкости":
            view_goose_menu(input_call, input_message)
    else:
        bot.answer_callback_query(input_call.id, "Не работает...", show_alert=True)






# Функция поиска.

def find_goose(call, message):
    #Проверяем что из этого настоящий мессэдж, а что обычный текст.
    # try - обработчик первичного коллбэка
    # except - обработчик вторичного ввода текста с клавиатуры.
    try:
        chat_id = call.message.chat.id
        user_info = read_db_row("user_base", chat_id=chat_id)
        user_type = user_info['user_type']
        bot.send_message(chat_id, "Введите название товара")
        write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="Поиск")

    except:
        chat_id = message.chat.id
        print(message.text)
        write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="mainmenu")

# Вспомогательная функция поиска
def find_array(message, find_goose, user_type):
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

def goose_view(goose_name, user_type):
    # Разбиваем коллбэк на данные
    if user_type == "Продавец" or "Стажер":
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
                                                      callback_data="Добавить примечание:Продавец:" + str(goose_info['id']))
        keyboard.add(callback_button)
        keyboard.add(callback_button1)
        # Cообщение вывода информации о товаре.
        bot.send_message(call.message.chat.id, goose_message, parse_mode="HTML", disable_web_page_preview=True,
                         reply_markup=keyboard)


