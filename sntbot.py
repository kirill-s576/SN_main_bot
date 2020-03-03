import telebot
from telebot import types
import pymysql
import pymysql.cursors
import ast
import datetime
from datetime import date
import time
from time import strftime
import asana2
from asana2 import create_task, get_section_id
import bdfunc
from bdfunc import connect_db, read_db, deteterow_db, write_db, write_db_insert, write_db_update, read_dailycheck, read_db_simple, read_db_universe

WORKSPACE_ID="829874196257517"
WORKSPACE_NAME="sigaretnet.by"
LOGISTIKA_ID='1105325346493274'

userpassword="7007123456789"
adminpassword="80297618745"
flag="ojidanie"


token = "385467625:AAF8EjbdekUijHlaXlcrdkh4jwPAqatCrzs"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['inline'])
def handle_inline(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(message.chat.id,
                     "Отправь мне свой номер телефона или поделись местоположением, жалкий человечишка!",
                     reply_markup=keyboard)

#@bot.callback_query_handler(func=lambda call: call.data == "Исправить фамилию" and operationlist[call.message.chat.id] == "lastname")


"""**************************************************************************************************************"""

"""Функции для рассылок."""

"""**************************************************************************************************************"""

def rassilka(textrassilki, UserGroup):
    connection = connect_db()
    cursor = connection.cursor()
    x = (UserGroup)
    mySQLQuery = "SELECT UserID FROM telegrambase WHERE UserType = '%s'" % x
    cursor.execute(mySQLQuery)
    result = cursor.fetchall()
    print(result)
    print(textrassilki)
    for i in result:
        print(i[0])
        y=str(i[0])
        try:
            bot.send_message(y,textrassilki)
        except:
            print("ошибка рассылки")

"""****************************************"""

def feedbackrassilka(textrassilki, UserGroup):
    print("Рассылка")
    connection = connect_db()
    cursor = connection.cursor()
    x = (UserGroup)
    mySQLQuery = "SELECT UserID FROM telegrambase WHERE UserType = '%s'" % x
    cursor.execute(mySQLQuery)
    result = cursor.fetchall()
    z = read_dailycheck("telegrammessages", "cmid", messagetext = str(textrassilki))
    for j in z:
        s = str(j[0])
        for i in result:
            print(i[0])
            y = str(i[0])
            try:
                keyboard = types.InlineKeyboardMarkup()
                callback_button1 = types.InlineKeyboardButton(text="Принять", callback_data="zaprosbutton:" + s)
                keyboard.add(callback_button1)
                bot.send_message(y, textrassilki, reply_markup=keyboard)
            except:
                print("ошибка функции Feedbackrassilka")


"""Функция проверки наличия невыполненных задач для администратора."""

"""**************************************************************************************************************"""
def check():

           y = read_dailycheck("telegrammessages", "cmid", status = "Ждет выполнения")
           if len(y)>0:
                for i in y:
                    s = str(i[0])
                    x = s.split(":")
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="Принять", callback_data="zaprosbutton:" + s)
                    keyboard.add(callback_button)
                    z = read_dailycheck("telegrambase", "UserID", UserType ="Администратор")
                    for j in z:
                        bot.send_message(str(j[0]),str(read_db_universe("telegrammessages", "messagetext", "cmid", str(x[0]) + ":" + str(x[1]))),reply_markup=keyboard)




"""**************************************************************************************************************"""



"""***********************МЕНЮ ПРОДАВЦА********************************************************************"""

"""ФУНКЦИЯ ГЛАВНОГО МЕНЮ"""
def menu_for_shopper_full(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Помощь руководства')
    markup.row('Дневной чек-лист')
    bot.send_message(message.chat.id,"*****", reply_markup=markup)

"""КНОПКА ДНЕВНОЙ ЧЕК-ЛИСТ"""
@bot.message_handler(func=lambda message: read_db(message.chat.id, "UserType", "telegrambase") == "Продавец" and message.text == "Дневной чек-лист")
def menu_check_list(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Открыть смену')
    """markup.row('Сверить деньги на точке - не работает')
    markup.row('Инвентаризация - не работает')"""
    markup.row('В главное меню')
    bot.send_message(message.chat.id, "*****", reply_markup=markup)

"""ВОЗВРАТ В ГЛАВНОЕ МЕНЮ"""
@bot.message_handler(func=lambda message: read_db(message.chat.id, "UserType", "telegrambase") == "Продавец" and message.text == "В главное меню")
def main_menu(message):
    menu_for_shopper_full(message)

"""**********************ОБРАБОТЧИК КОМАНД ПРОДАВЦА********************************"""

"""ПОМОЩЬ РУКОВОДСТВА"""

@bot.message_handler(func=lambda message: read_db(message.chat.id, "UserType", "telegrambase") == "Продавец" and (message.text == "Помощь руководства" or flag == "zapros") )

def msg_zapros(message):

    global flag,flagoff

    text = message.text
    flagoff = "True"

    if text == "Помощь руководства" and flag == "ojidanie":
        bot.send_message(message.chat.id, "Введите текст запроса:")
        flag = "zapros"
        flagoff = "False"

    elif flagoff == "True" and flag == "zapros":
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Отправить", callback_data="Отправить запрос")
        callback_button2 = types.InlineKeyboardButton(text="Хочу исправить", callback_data="Хочу исправить")
        callback_button3 = types.InlineKeyboardButton(text="Забей", callback_data="Забей")
        keyboard.add(callback_button1, callback_button2, callback_button3)
        bot.send_message(message.chat.id, message.text, reply_markup=keyboard)


        flagoff = "False"
        flag = "ojidanie"

    else:
        bot.send_message(message.chat.id, "Я пока не понимаю эту команду(")

@bot.callback_query_handler(func=lambda call: str(call.data).startswith("zaprosbutton:")==True)

def confirm_zapros(call):
    s = str(call.data)
    x = s.split(":")
    print(x[1])
    print(x[2])
    print(call.message.text)
    write_db_update("telegrammessages",cmid = str(x[1])+":"+str(x[2]), status = "Выполняется")
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выполняется")
    bot.send_message(chat_id = str(x[2]), text = "Запрос " + read_db_universe("telegrammessages", "messagetext", "cmid", str(x[1])+":"+str(x[2])) + " выполняется " + str(read_db_universe("telegrambase", "UserName", "ChatID", call.message.chat.id )))



"""**************************************************************************************************************"""
"""**************************************************************************************************************"""
"""**************************************************************************************************************"""
"""**********************Открытие смены***************************"""


global operationlist
operationlist = {}
operationlist['356080087'] = ""

@bot.message_handler(func=lambda message: read_db(message.chat.id, "UserType", "telegrambase") == "Продавец" and (message.text == "Открыть смену") )

def open_day(message):
    global operationlist
    bot.send_message(message.chat.id, "Введите фамилию:")
    global flag


    operationlist[message.chat.id] = "lastname"


@bot.message_handler(func=lambda message: read_db(message.chat.id, "UserType", "telegrambase") == "Продавец") #and operationlist[message.chat.id] == "lastname")
def enter_lastname(message):
    global operationlist
    nowdate = strftime("%d.%m.%Y")
    print(nowdate)
    status = read_dailycheck("dailycheck", "status", chat_id = message.chat.id, date = nowdate)
    print(status)
    if len(status) > 0:
        status = status[0][0]
    if status == "complete":
        bot.send_message(message.chat.id, "Смена уже открыта. Не тупи.")
    else:
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Точно", callback_data=message.text)
        callback_button2 = types.InlineKeyboardButton(text="Хочу исправить", callback_data="Исправить фамилию")
        keyboard.add(callback_button1, callback_button2)
        bot.send_message(message.chat.id, "Точно " + message.text + "?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data !="Исправить фамилию"  and operationlist[call.message.chat.id] == "lastname")

def confirm_lastname(call):
    global operationlist
    worker = str(call.message.text)
    worker = worker.split(" ")
    worker = str(worker[1])[:-1]
    chat_id =call.message.chat.id
    username = read_db_universe("telegrambase", "UserName", "ChatID", call.message.chat.id)
    nowtime = strftime("%H:%M")
    nowdate = strftime("%d.%m.%Y")
    taskid = asana2.create_task(username + " " + worker + " " + nowtime, "Открытие смены")
    print(taskid)
    write_db_insert("dailycheck", chat_id = chat_id, worker = worker, check_name = "Открытие смены",
                    status = "complete", date = nowdate, dateoff = nowdate, timeoff = nowtime, user_name = username, task_id = str(taskid))

    bot.send_message(call.message.chat.id, "Смена открыта в " + nowtime +". Доброе утро!")
    operationlist[call.message.chat.id] = ""

@bot.callback_query_handler(func=lambda call: call.data == "Исправить фамилию" and operationlist[call.message.chat.id] == "lastname")

def rename(call):
    global operationlist
    bot.send_message(call.message.chat.id, "Повторите ввод:")
    operationlist[call.message.chat.id] = "lastname"
"""**************************************************************************************************************"""
"""**************************************************************************************************************"""
"""**************************************************************************************************************"""

@bot.message_handler(commands=['reset'])
def handle_reset(message):
    pass
    deteterow_db(message.chat.id, "telegrambase")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('/start')
    bot.send_message(message.chat.id, "Вы можете начать новую жизнь!",reply_markup=markup)




"""*************************************************************************"""

@bot.message_handler(commands=['start'])
def handle_start(message):
    pass
    id = str(message.chat.id)
    firstname = str(message.chat.first_name)
    lastname = str(message.chat.last_name)
    if  read_db(id, "UserType", "telegrambase") == None:
        write_db(id, "UserName", "telegrambase", firstname+ " " + lastname)
        write_db(id, "ChatID", "telegrambase", id)
        bot.send_message(id, "Привет, " + firstname +" " + lastname)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Продавец')
        markup.row('Администратор')
        bot.send_message(id, "Выберите тип пользователя:", reply_markup=markup)

    elif read_db(id, "UserType", "telegrambase") == "Администратор":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Объявление')
        markup.row('Обращения')
        markup.row('Открытие смены')
        bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=markup)


    elif read_db(id, "UserType", "telegrambase") == "Продавец":

        menu_for_shopper_full(message)

"""***************************************************************************"""


@bot.message_handler(func=lambda message: read_db(message.chat.id,"UserType", "telegrambase" ) == None)

def msg_auth(message):
    id = message.chat.id
    text = message.text
    """Авторизация"""
    if text == "Продавец":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup= markup)
        bot.send_message(message.chat.id, "Введите пароль:")
    elif text == "Администратор":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup= markup)
        bot.send_message(message.chat.id, "Введите пароль:")
    elif text == str(userpassword):
        bot.send_message(message.chat.id, "Авторизация пройдена!")
        write_db(str(id), "UserType", "telegrambase", "Продавец")
        handle_start(message)
    elif text == str(adminpassword):
        bot.send_message(message.chat.id, "Авторизация пройдена! Теперь вы Администратор!")
        write_db(str(id), "UserType", "telegrambase", "Администратор")
        handle_start(message)
    """Обработка запроса на помощь"""



"""*****************************************************************************"""
#Доработать функцию просмотра запросов.
@bot.message_handler(func=lambda message: read_db(message.chat.id,"UserType","telegrambase") == "Администратор" and message.text == "Обращения")


def msg_obraschenie(message):
    y = read_dailycheck("telegrammessages", "cmid", status = "Ждет выполнения")
    if y == ():
        bot.send_message(message.chat.id,"Обращений нет")
        y = read_dailycheck("telegrammessages", "cmid", status="Выполняется")
        bot.send_message(message.chat.id, "Сейчас выполняются:")
        for i in y:
            s= str(i[0])
            x = s.split(":")
            bot.send_message(message.chat.id, str(i[0]))
    else:
        for i in y:
            s= str(i[0])
            x = s.split(":")
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Принять", callback_data="zaprosbutton:"+ s)
            keyboard.add(callback_button)
            bot.send_message(message.chat.id, str(read_db_universe("telegrammessages", "messagetext", "cmid", str(x[0])+":"+str(x[1]))), reply_markup=keyboard)




@bot.message_handler(func=lambda message: read_db(message.chat.id,"UserType","telegrambase") == "Администратор" and message.text == "Открытие смены")


def msg_otkritie(message):
    nowdate = strftime("%d.%m.%Y")
    y = read_dailycheck("telegrambase", "UserName", UserType = "Продавец")
    S=""
    S1 = ""
    if y == ():
        bot.send_message(message.chat.id,"Открытых смен нет")

    else:
        for i in y:
            nowtime = read_dailycheck("dailycheck", "timeoff", user_name=str(i[0]), date=str(nowdate))
            shop = i[0] #read_dailycheck("dailycheck", "timeoff", user_name=str(i[0]), date=str(nowdate))
            if len(str(nowtime))>6:
                S = S + " \n" + " " + str(shop) + " в " + str(nowtime[0][0])
            else:
                S1 = S1 +  " \n" + " " + str(shop)

        if len(S)>1:
            bot.send_message(message.chat.id,"Смена открыта" + " \n" + S)
        if len(S1) > 1:
            bot.send_message(message.chat.id,"Смена закрыта" + " \n" + S1)




"""*****************************************************************************"""



@bot.message_handler(func=lambda message: read_db(message.chat.id,"UserType","telegrambase") == "Администратор")


def msg_objavlenie(message):
    global flag,flagoff

    flagoff = "True"

    if message.text == "Объявление" and flag == "ojidanie":
        bot.send_message(message.chat.id, "Введите текст объявление:")
        flag = "objavlenie"
        flagoff = "False"


    elif flagoff == "True" and flag == "objavlenie":
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Отправить всем", callback_data="Отправить всем")
        callback_button2 = types.InlineKeyboardButton(text="Хочу исправить", callback_data="Хочу исправить")
        callback_button3 = types.InlineKeyboardButton(text="Забей", callback_data="Забей")
        keyboard.add(callback_button1, callback_button2,callback_button3)
        bot.send_message(message.chat.id, message.text, reply_markup=keyboard)

        flagoff = "False"
        flag = "ojidanie"

    else:
        bot.send_message(message.chat.id, "Я пока не понимаю эту команду")





"""******************************************************************************"""



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    global flag
    if call.message:
        if call.data == "Отправить всем":
            rassilka(str(call.message.text),'Продавец')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Готово")
            flag = "ojidanie"
        if call.data == "Отправить запрос":
            """feedbackrassilka(str(call.message.chat.first_name)+" " + str(call.message.chat.last_name)+": "+ call.message.text,'Администратор')"""
            write_db_insert("telegrammessages",cmid = str(call.message.message_id) + ":" + str(call.message.chat.id),   сhatidfrom = call.message.chat.id, messageid = call.message.message_id, status = "Ждет выполнения", messagetext = call.message.text)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Готово")
            check()
            asana2.create_task(str(call.message.chat.first_name)+" " + str(call.message.chat.last_name)+": "+ call.message.text, "Запросы на помощь")
            flag = "ojidanie"
        if call.data == "Хочу исправить":
            flag = "objavlenie"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите сообщение еще раз:")
        if call.data == "Забей":
            flag = "ojidanie"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Проехали")
        if call.data == "Запрос принят":
            flag = "ojidanie"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text + "  Запрос выполнен")
            try:
                print(call.message)
            except:
                print("ошибка")



"""**************************************************************************************************************"""





if __name__ == '__main__':
    bot.polling(none_stop=True)