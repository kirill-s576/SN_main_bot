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
import idea

SHOPPASS = "7007123456789"
ADMINPASS = "80297618745"
SUPERADMINPASS = "1357908642"
SHOPPERBOSSPASS = {}
SHOPPERBOSSPASS['Green'] = "green"
SHOPPERBOSSPASS['Dana'] = "dana"
SHOPPERBOSSPASS['Siluet'] = "siluet"
SHOPPERBOSSPASS['Globo'] = "globo"
SHOPPERBOSSPASS['Malinovka'] = "malinovka"
SHOPPERBOSSPASS['Prostore'] = "prostore"
SHOPPERBOSSPASS['Partizan'] = "partizan"
SHOPPERBOSSPASS['Region'] = "1364432"


token = "760178208:AAFT7Qdk5Hfv3lwQthh6vykwGCpSxa6yT2U"
#token = "385467625:AAF8EjbdekUijHlaXlcrdkh4jwPAqatCrzs"
bot = telebot.TeleBot(token)

#ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ.

global menumessage       #Хранится словарь ChatID пользователя и MessageID. Запоминает сообщение с выведенным меню.
menumessage = {}         #Используется для того, чтобы не захламлять чат.

global operationlist     #Хранится словарь ChatID пользователя и название выполняемой операции.
operationlist = {}       #Справка:


global opendaymessage1   #Три сообщения, в котрые выводятся данные об открытой смене.
opendaymessage1 = {}     #Формат {chat_id:message_id}
global opendaymessage2
opendaymessage2 = {}
global opendaymessage3
opendaymessage3 = {}

shops = read_db_array("telegrambase", "ChatID")
for shop in shops:
    operationlist[int(shop)] = ""
print(operationlist)
operationlist[310331116] = ""

#Функция онлайн обновления пришедших на работу.
def openday_update():
    openday = read_db_array("dailycheck", "id", check_name="Открытие смены", date=str(date.today()))
    keyboard1 = types.InlineKeyboardMarkup()
    keyboard2 = types.InlineKeyboardMarkup()
    opendayids = []
    # Сортируем опоздавших и не опоздавших. Выводим двумя разными сообщениями.
    for day in openday:
        data = read_db_row("dailycheck", id=str(day))
        if len(data["result"]) <4:
            callback_button2 = types.InlineKeyboardButton(
                text=data['user_name'] + " " + str(data['result']) + " мин",
                callback_data='Почему опоздал:' + str(data['chat_id']))
            keyboard1.add(callback_button2)
            opendayids.append(data['chat_id'])
        else:
            callback_button2 = types.InlineKeyboardButton(text=data['user_name'] + " " + "Без опозданий",
                                                          callback_data='12345')
            keyboard2.add(callback_button2)
            opendayids.append(data['chat_id'])



    openids = read_db_array("telegrambase", "ChatID", UserType="Продавец")
    keyboard3 = types.InlineKeyboardMarkup()
    for openid in openids:
        print(openids)
        print(opendayids)
        if int(openid) not in opendayids:
            data = read_db_row("telegrambase", ChatID=str(openid))
            callback_button2 = types.InlineKeyboardButton(text=data['UserName'] + " " + "Не открылся",
                                                          callback_data='12345')
            keyboard3.add(callback_button2)

    for key in opendaymessage1:
        try:
            bot.edit_message_reply_markup(chat_id = str(key), message_id=str(opendaymessage1[key]), reply_markup = keyboard1)
            bot.edit_message_reply_markup(chat_id=str(key), message_id=str(opendaymessage2[key]),reply_markup=keyboard2)
            bot.edit_message_reply_markup(chat_id=str(key), message_id=str(opendaymessage3[key]),reply_markup=keyboard3)
        except:
            print("Ничего неизменилось, нечего менять.")

#Функция возвращает текст фамилия\смены\опоздал\минут
def top_opezdalov():
    arrayopezdalov = read_db_array("dailycheck", "worker")
    opendays = {}
    notdelay = {}
    delaytime = {}
    delaycounts = {}
    for opezdal in arrayopezdalov:
        delays = read_db_array("dailycheck", "result", worker = opezdal)
        opendays[opezdal] = len(delays)
        for delay in delays:
            notdelaycount = 0
            delaytimecount = 0
            delaycount = 0
            if delay == "Не опоздал":
                notdelaycount +=1
            elif len(delay)<3:
                delaytimecount += int(delay)
                delaycount += 1
            notdelay[opezdal] = notdelaycount
            delaytime[opezdal] = delaytimecount
            delaycounts[opezdal] = delaycount
    result = ""
    for key in opendays:
        result += key+"="*(14-len(key))+str(opendays[key]) + " Смен. " + str(delaycounts[key]) + " раз опоздал на " + str(delaytime[key]) + " минут.\n"
    return result


@bot.message_handler(content_types=['text'], func=lambda message: message.chat.id not in operationlist)
def operation(message):
    operationlist[message.chat.id] = ""


@bot.callback_query_handler(func=lambda call: call.message.chat.id not in operationlist)
def operation_call(call):
    operationlist[call.message.chat.id] = ""


#Команда сброса и удаления пользователя из зарегистрированных.
@bot.message_handler(commands=['reset'])
def handle_reset(message):
    pass
    deteterow_db(message.chat.id, "telegrambase")
    bot.send_message(message.chat.id, "Вы можете начать все заново!")


#Меню регистрации
#Условие вывода меню регистрации (Команда Start и Абонента нет в базе номеров)
@bot.message_handler(commands=['start'])
def main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text="Главное меню")
    keyboard.add(button1)
    bot.send_message(message.chat.id, "Это бот-помощник компании SigaretNet.by. Добро пожаловать",
                     reply_markup=keyboard)

def registry(message):

    shopids = bdfunc.read_db_array("telegrambase", "ChatID", UserType = "Продавец")
    adminids =bdfunc.read_db_array("telegrambase", "ChatID", UserType = "Администратор")
    shopperbossids = bdfunc.read_db_array("telegrambase", "ChatID", UserType = "Старший продавец")
    #Что делать если продавец
    if str(message.chat.id) in shopids:
        menu_shop(message)
    #ЧТо делать если администратор
    elif str(message.chat.id) in adminids:
        menu_admin(message)
    # ЧТо делать если старший продавец
    elif str(message.chat.id) in shopperbossids:
        print("Старший продавец")
        menu_shopperboss(message)
    # Что делать если пощльзователя нет в базе(Не зарегистрирован). Процедура регистрации.
    else:
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Магазин",
                                                      callback_data="Регистрация Магазин" + ":" + str(message.chat.id))
        callback_button2 = types.InlineKeyboardButton(text="Администратор",
                                                      callback_data="Регистрация Администратор" + ":" + str(message.chat.id))
        callback_button3 = types.InlineKeyboardButton(text="Суперадмин",
                                                      callback_data="Регистрация Суперадмин" + ":" + str(message.chat.id))

        callback_button4 = types.InlineKeyboardButton(text="Старший продавец",
                                                      callback_data="Регистрация Старший продавец" + ":" + str(
                                                          message.chat.id))
        keyboard.add(callback_button1)
        keyboard.add(callback_button2)
        keyboard.add(callback_button3)
        keyboard.add(callback_button4)
        message = bot.send_message(message.chat.id, "Выберите тип пользователя", reply_markup=keyboard)
        menumessage[message.chat.id] = message.message_id


@bot.message_handler(func = lambda message: message.text == "Главное меню")
def main_menu(message):
    #bot.delete_message(message.chat.id, message.message_id)
    try:
        bot.delete_message(message.chat.id, menumessage[message.chat.id])
    except:
        print("Ошибка главного меню")
    registry(message)


#Ввод пароля для регистрации
@bot.callback_query_handler(func=lambda call: (("Регистрация" in call.data) and (call.data.split(":")[1] == str(call.message.chat.id))))
def callback_choose_usertype(call):
    if "Регистрация Старший продавец" in call.data:
        bot.delete_message(call.message.chat.id, menumessage[call.message.chat.id])
        operationlist[call.message.chat.id] = "Ввод пароля для регистрации старшего продавца"
        bot.send_message(call.message.chat.id, "ВВведите пароль старшего продавца")

    else:
        bot.delete_message(call.message.chat.id,menumessage[call.message.chat.id])
        operationlist[call.message.chat.id] = "Ввод пароля для регистрации"
        bot.send_message(call.message.chat.id, "Введите пароль пользователя")


#Тут мы проверяем пароль и вносим нового человека в базу данных.
@bot.message_handler(func=lambda message: operationlist[message.chat.id] == "Ввод пароля для регистрации")
def enter_password(message):
    id = message.chat.id
    firstname = str(message.chat.first_name)
    lastname = str(message.chat.last_name)

    if message.text == SHOPPASS:
        print("Это продавец!")
        write_db_insert("telegrambase", ChatID=str(id), UserName=str(firstname)+" " + str(lastname), UserType="Продавец", UserID = id)
        operationlist[message.chat.id] = ""
        menu_shop(message)
    elif message.text == ADMINPASS:
        print("Это Админ!")
        write_db_insert("telegrambase", ChatID = str(id), UserName=str(firstname)+" " + str(lastname), UserType="Администратор", UserID = id)
        operationlist[message.chat.id] = ""
        menu_admin(message)
    elif message.text == SUPERADMINPASS:
        print("Это Суперадмин!")
        write_db_insert("telegrambase", ChatID=str(id), UserName=str(firstname)+" " + str(lastname), UserType="Суперадмин", UserID=id)
        operationlist[message.chat.id] = ""
    else:
        bot.send_message(message.chat.id, "Пароль введен не верно. Повторите ввод")
        print("Не верно введен пароль!")

#Тут мы проверяем пароль СТАРШЕГО ПРОДАВЦА и вносим нового человека в базу данных.
@bot.message_handler(func=lambda message: operationlist[message.chat.id] == "Ввод пароля для регистрации старшего продавца")
def enter_password_shopperboss(message):
    id = message.chat.id
    firstname = str(message.chat.first_name)
    lastname = str(message.chat.last_name)
    keylog = ""
    for password in SHOPPERBOSSPASS:
        if message.text == SHOPPERBOSSPASS[password]:
            keylog = message.text
            groups = password
            continue

    if len(keylog) > 0:
        write_db_insert("telegrambase",ChatID = str(id), UserName = str(firstname)+" " +str(lastname), UserType = "Старший продавец", Groups = str(groups), UserID = id)
        msg = bot.send_message(message.chat.id, "Регистрация прошла успешно")
        time.sleep(1)
        bot.delete_message(msg.chat.id, msg.message_id)
        operationlist[message.chat.id] = ""
        menu_shopperboss(message)
    else:
        bot.send_message(message.chat.id, "Пароль введен не верно. Повторите ввод")
        print("Не верно введен пароль!")


#Меню продавца

#****************Условие вывода меню продавца*******************
@bot.message_handler(func=lambda message: operationlist[message.chat.id]=="" and str(message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Продавец"))
#Отрисовка меню продавца.
def menu_shop(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Открытие смены", callback_data="Открытие смены"+":"+str(message.chat.id))
    callback_button2 = types.InlineKeyboardButton(text="********Дневной чек-лист********", callback_data="Дневной чек-лист")
    callback_button3 = types.InlineKeyboardButton(text="Помощь руководства", callback_data="Помощь руководства"+":"+str(message.chat.id))
    callback_button4 = types.InlineKeyboardButton(text="Шаблон для рассрочки", callback_data="Шаблон рассрочки")
    callback_button_free = types.InlineKeyboardButton(text=" ", callback_data="Пустая кнопка")
    keyboard.add(callback_button2)
    keyboard.add(callback_button1, callback_button_free)
    keyboard.add(callback_button3)
    keyboard.add(callback_button4)
    message = bot.send_message(message.chat.id, "Главное меню", reply_markup=keyboard)
    menumessage[message.chat.id] = message.message_id


        #****************Обработчик нажатия кнопок меню продавца***************************
#Обработчик кнопки "Открытие смены" !!! Добавить везде проверку пользователя.
@bot.callback_query_handler(func=lambda call: (("Открытие смены" in call.data) and (call.data.split(":")[1] == str(call.message.chat.id))
                                               and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Продавец")))
def callback_open_day(call):


    operationlist[call.message.chat.id] = "Ввод фамилии для открытия смены"
    print(call.message.chat.id)
    bot.send_message(call.message.chat.id, "Введите свою фамилию")

#Рекция на ввод фамилии при открытии смены.
@bot.message_handler(func=lambda message: operationlist[message.chat.id] == "Ввод фамилии для открытия смены" and str(message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Продавец"))
def get_last_name(message):
    #Проверка на уже открытую смену.
    print("Проверка на открытие")
    if len(read_db_row("dailycheck", chat_id = message.chat.id, date = date.today(), check_name = "Открытие смены")) >0:
        bot.send_message(message.chat.id, "Смена уже открыта. Попробуйте открыть завтра")
    else:
        #Проверка на опоздание
        now = datetime.datetime.now()
        open= read_db_row("telegrambase", ChatID = str(message.chat.id))['OpenTime']

        opentime = datetime.datetime.strptime(str(open), "%H:%M:%S").time()
        nowtime = now.time()
        delta = datetime.datetime.combine(date.today(), nowtime) - datetime.datetime.combine(date.today(), opentime)

        if delta.seconds//60 > 1000:
            delay = "Не опоздал"
        else:
            delay = delta.seconds//60

        # Здесть в базу вносятся все параметры открытия смены в базу данных.
        write_db_insert("dailycheck", chat_id=str(message.chat.id),
                        user_name=str(message.chat.first_name) + " " + str(message.chat.last_name),
                        worker=str(message.text),
                        date=str(date.today()),
                        dateoff=str(date.today()),
                        result=str(delay),
                        #status="complete",
                        check_name="Открытие смены")
        #Проверяем на опоздание.
        if nowtime > opentime:
            bot.send_message(message.chat.id, "Какова причина задержки на "+ str(delta.seconds//60) + " минут? Все причины рассматриваются в частном порядке.")
            operationlist[message.chat.id] = "Ввод причины опоздания"
        else:
            #Убираем старое меню и выводим снова, чтобы оно опять было в самом низу.
            try:

                bot.send_message(message.chat.id, "Смена открыта в " + str(strftime("%H:%M")))
                operationlist[message.chat.id] = ""
                bot.delete_message(message.chat.id,menumessage[message.chat.id])
            except:
                print("Старого меню не обнаружено")
            menu_shop(message)
            openday_update()


@bot.message_handler(func=lambda message: operationlist[message.chat.id] == "Ввод причины опоздания" and str(message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Продавец"))
def get_open_delay(message):
    #Внесение причины опоздания в БД
    try:
        write_db_update_ultimate("dailycheck", find__chat_id = message.chat.id, find__check_name = "Открытие смены", find__date = str(date.today()), comment = str(message.text))
        bot.send_message(message.chat.id, "Больше не задерживайтесь. Клиенты ждать не будут... Смена открыта в " + str(strftime("%H:%M")))
        #Отправить сообщение об опоздании Администраторам!
        shop = read_db_row("dailycheck", chat_id = message.chat.id, check_name = "Открытие смены", date = str(date.today()))
        admins = read_db_array("telegrambase","ChatID", UserType = "Администратор")
        for admin in admins:
            bot.send_message(admin, "Опоздание на "+ str(shop['result'])+" минут "+ str(shop['user_name'])+ " \nПродавец:"+ str(shop['worker'])+ " \nПричина опоздания:"+ str(message.text))
        operationlist[message.chat.id] = ""
        bot.delete_message(message.chat.id, menumessage[message.chat.id])
    except:
        print("Старого меню не обнаружено")
    menu_shop(message)
    openday_update()

#Обработчик кнопки "Помощь руководства"
@bot.callback_query_handler(func=lambda call: "Помощь руководства" in call.data and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Продавец"))
def callback_inline(call):
    print(call.data)






#Меню администратора
#Условие вывода
@bot.message_handler(commands=['admin'])
def menu_admin(message):


    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Кто открыл смену",
                                                  callback_data="Кто открыл смену" + ":" + str(message.chat.id))
    callback_button2 = types.InlineKeyboardButton(text="Отправить всем сообщение",
                                                  callback_data="Отправить всем сообщение")
    callback_button3 = types.InlineKeyboardButton(text="Старшие продавцы",
                                                  callback_data="Старшие продавцы" + ":" + str(message.chat.id))
    callback_button_free = types.InlineKeyboardButton(text=" ", callback_data="Пустая кнопка")
    keyboard.add(callback_button1)
    keyboard.add(callback_button2)
    keyboard.add(callback_button3)
    message = bot.send_message(message.chat.id, "Главное меню", reply_markup=keyboard)
    menumessage[message.chat.id] = message.message_id


#Обработчик кнопки "Кто открыл смену"
@bot.callback_query_handler(func=lambda call: "Кто открыл смену" in call.data and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Администратор"))
def get_open_day(call):
    openday = read_db_array("dailycheck", "id", check_name = "Открытие смены", date = str(date.today()))
    keyboard1 = types.InlineKeyboardMarkup()
    keyboard2 = types.InlineKeyboardMarkup()
    opendayids = []
    #Сортируем опоздавших и не опоздавших. Выводим двумя разными сообщениями.
    for day in openday:
        data = read_db_row("dailycheck", id = str(day))
        if len(data["result"]) < 4:
            callback_button2 = types.InlineKeyboardButton(text=data['user_name']+ " "+ str(data['result']) + " мин",
                                                      callback_data='Почему опоздал:'+str(data['chat_id']))
            keyboard1.add(callback_button2)
            opendayids.append(data['chat_id'])
        else:
            callback_button2 = types.InlineKeyboardButton(text=data['user_name']+" "+"Без опозданий",
                                                      callback_data='Почему опоздал:'+str(data['chat_id']))
            keyboard2.add(callback_button2)
            opendayids.append(data['chat_id'])
    #Третьим сообщением выводим еще не открытые магазины.
    openids = read_db_array("telegrambase", "ChatID", UserType="Продавец")
    keyboard3 = types.InlineKeyboardMarkup()
    for openid in openids:

        if int(openid) not in opendayids:
            data = read_db_row("telegrambase", ChatID=str(openid))
            callback_button2 = types.InlineKeyboardButton(text=data['UserName'] + " " + "Не открылся",
                                                          callback_data='12345')
            keyboard3.add(callback_button2)

    #Отправляем сформированные сообщения об открытых сменах и запоминаем номера сообщений для последующего обновления.
    msg1 = bot.send_message(call.message.chat.id, "Опоздали", reply_markup=keyboard1)
    msg3 = bot.send_message(call.message.chat.id, "Еще не открылись", reply_markup=keyboard3)
    msg2 = bot.send_message(call.message.chat.id, "Пришли вовремя", reply_markup=keyboard2)

    opendaymessage1[call.message.chat.id] = msg1.message_id
    opendaymessage2[call.message.chat.id] = msg2.message_id
    opendaymessage3[call.message.chat.id] = msg3.message_id

#Показать причину опоздания в окне Alert.
@bot.callback_query_handler(func=lambda call: "Почему опоздал" in call.data and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Администратор"))
def why_delay(call):
    chatid = call.data.split(":")[1]
    data = read_db_row("dailycheck",date = date.today(), chat_id = chatid, check_name = "Открытие смены")
    shop = data['user_name']
    comment = data['comment']
    worker = data['worker']
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Магазин: " + str(shop) + "\nПродавец: " + str(worker) + "\nПричина опоздания: " +str(comment))


#Обработка кнопки "Старшие продавцы"
@bot.callback_query_handler(func=lambda call: "Старшие продавцы" in call.data and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Администратор"))
def shopperboss_monitoring(call):
    pass
    bosses = read_db_array("openday_shopperboss", "id", stat = "open")
    text = ""
    if len(bosses)>0:
        for boss in bosses:
            info = read_db_row("openday_shopperboss",id = boss)
            text +=  info['user_name']+ " " +info['shop']+"\n"
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text = text)
    else:
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Никого нигде нет")


#Меню супер-администратора
#Условие вывода
@bot.message_handler(commands=['superadmin'])
def menu_superadmin(message):
    bot.send_message(message.chat.id, top_opezdalov())



# *********** ВСЕ, Что касается старших продавцов ***************
@bot.message_handler(func=lambda message: operationlist[message.chat.id]=="" and str(message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Старший продавец"))
#Отрисовка меню Старшего продавца продавца.
def menu_shopperboss(message):
    keyboard = types.InlineKeyboardMarkup()

    callback_button1 = types.InlineKeyboardButton(text="Начать смену", callback_data="Открытие смены старшего"+":"+str(message.chat.id))
    callback_button2 = types.InlineKeyboardButton(text="Завершить смену", callback_data="Завершение смены старшего" + ":" + str(message.chat.id))


    keyboard.add(callback_button1, callback_button2)

    if "open" in read_db_array("openday_shopperboss", "stat", chat_id=message.chat.id):
        info = read_db_row("openday_shopperboss",chat_id=message.chat.id, stat = "open")

        callback_button3 = types.InlineKeyboardButton(text="Открыта в "+ str(info['shop']), callback_data="Пустая кнопка")
        keyboard.add(callback_button3)
    else:
        callback_button3 = types.InlineKeyboardButton(text="Смена закрыта",
                                                      callback_data="Пустая кнопка")
        keyboard.add(callback_button3)

    message = bot.send_message(message.chat.id, "Главное меню", reply_markup=keyboard)
    menumessage[message.chat.id] = message.message_id


# Открытие смены старшего
@bot.callback_query_handler(func=lambda call: "Открытие смены старшего" in call.data and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Старший продавец"))
def openday_shopperboss(call):
    bot.delete_message(call.message.chat.id, menumessage[call.message.chat.id])
    group = read_db_row("telegrambase",ChatID = str(call.message.chat.id) )['Groups']
    shops = read_db_array("telegrambase", "UserName", UserType = "Продавец", Groups = group )
    keyboard = types.InlineKeyboardMarkup()
    for shop in shops:
        callback_button = types.InlineKeyboardButton(text=str(shop), callback_data="Выбор магазина"+":"+str(shop))
        keyboard.add(callback_button)
    msg = bot.send_message(call.message.chat.id, text = "Выберите магазин", reply_markup=keyboard)
    menumessage[call.message.chat.id] = msg.message_id


# Реакция на выбор магазина
@bot.callback_query_handler(func=lambda call: "Выбор магазина" in call.data and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Старший продавец"))
def openday_shopperboss_checkshop(call):

    if "open" in read_db_array("openday_shopperboss", "stat", chat_id = call.message.chat.id):
        bot.delete_message(call.message.chat.id, menumessage[call.message.chat.id])
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text = "Сначала закройте прыдыдущую смену")
        menu_shopperboss(call.message)
    else:
        shopname = call.data.split(":")[1]
        group =  read_db_row("telegrambase", ChatID = str(call.message.chat.id) )['Groups']
        username = str(call.message.chat.first_name) +" " + str(call.message.chat.last_name)

        bot.delete_message(call.message.chat.id, menumessage[call.message.chat.id])
        bot.send_message(call.message.chat.id, "Смена открыта в " + str(shopname))
        write_db_insert("openday_shopperboss", chat_id = call.message.chat.id, user_name = username, groups = group, shop = shopname, timeon = datetime.datetime.now(), stat = "open")

        menu_shopperboss(call.message)

        adminids = bdfunc.read_db_array("telegrambase", "ChatID", UserType = "Администратор")
        for id in adminids:
            bot.send_message(id, "Старший продавец" + str(username) + " прибыл в "+ str(shopname))


# Завершение смены старшего
@bot.callback_query_handler(func=lambda call: "Завершение смены старшего" in call.data and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Старший продавец"))
def closeday_shopperboss(call):

    info = read_db_row("openday_shopperboss", chat_id = call.message.chat.id, stat = "open")
    timeon = info['timeon']
    timeoff = datetime.datetime.now()
    delta = timeoff - timeon
    print(delta)
    write_db_update_ultimate("openday_shopperboss", find__id = info['id'], stat = "close", timeoff = timeoff, timedelta = delta)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Смена завершена. Длительность "+str(delta))

    bot.delete_message(call.message.chat.id, menumessage[call.message.chat.id])
    menu_shopperboss(call.message)

    adminids = bdfunc.read_db_array("telegrambase", "ChatID", UserType="Администратор")
    for id in adminids:
        bot.send_message(id, "Старший продавец" + str(info['user_name']) + " покинул " + str(info['shop'])+ ". Пробыл там "+ str(delta))

@bot.callback_query_handler(func=lambda call: "Шаблон рассрочки" in call.data and str(call.message.chat.id) in read_db_array("telegrambase", "ChatID", UserType = "Продавец"))
def get_rassrochka_list(call):

    file = open("/python_projects/sntelebot_v1/шаблон рассрочка.xlsx", 'rb')
    bot.send_document(call.message.chat.id, file, None)
    insrtuction = "Бот отпраляет пустую форму для выдачи рассрочки.\n" \
                  "Требуется заполнить необходимые поля и переслать файл обратно боту."

    bot.answer_callback_query(callback_query_id=call.id, text=insrtuction, show_alert=True)

@bot.message_handler(content_types=['document'])
def rassrochka(message):
    bd_id = write_db_insert("rassrochka", date=datetime.datetime.now())
    print("ID из базы данных" + str(bd_id))

    info = idea.send_order(message, str(bd_id))
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Проверить статус",
                                                  callback_data="Обновить:"+str(bd_id))

    keyboard.add(callback_button1)
    bot.send_message(message.chat.id, "Рассрочка " + str(info["FullNameStr"]), reply_markup=keyboard)



@bot.callback_query_handler(func = lambda call: "Обновить" in call.data)
def refresh_rassrochka(call):
    try:
        ApplicationNumber = call.data.split(":")[1]
        feedback = idea.get_status(ApplicationNumber)
        bot.answer_callback_query(callback_query_id=call.id, text=str(feedback), show_alert=True)
    except:
        bot.answer_callback_query(callback_query_id=call.id, text="Не корректно заданы параметры. Надо переделать.", show_alert=True)



if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except KeyError as e:
        operationlist[e] = ""
