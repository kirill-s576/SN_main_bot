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
from excel import *
import random

token = "817361693:AAFadWYZfaDiu9YUTgvPnNvisdx7-SwYnL4"
bot = telebot.TeleBot(token)



# Функция должна полностью отображать тест у пользователя, после того, как он нажмент кнопку с названием теста.
# Входящий элемент в функцию только message. То есть она на должна из текста предыдущего сообщения сама соображать на каком этапе находится пользователь.

def view_test(message, questionid, testid):
    #Удаляем форму со старым вопросом или не вопросом....

    # Забираем из БД информацию о тесте, который проходит конкретный пользователь в данный момент.
    try:  # Прверяем есть ли...
        test_result_info = read_db_row("tests_result", test_id=testid, chat_id=message.chat.id)
    except:  # Если нету - создаем...?
        print("Нет такого теста.... Надо сздать")
        id = write_db_insert("tests_result", chat_id=message.chat.id, test_id=tetst_id)
        test_result_info = read_db_row("tests_result", id=id)
    # Вытаскиваем из БД промежуточные результаты result_previous. Формат - {question_id:[1,2,3,4,5],... }
    result_previous = test_result_info['result_previous']
    try:
        result_previous = ast.literal_eval(result_previous)
    except:
        result_previous = {}
    result_previous_local = []
    try:
        result_previous_local = list(set(result_previous[(int(questionid))]))
    except:

        print("ОШИБКА result_previous_local 1")

    # Разбираемся с временем которое отведено на прохождение теста.
    # Сначала проверяем есть ли что в ячейках и вносим исходные данные(Время начала теста)
    td = ""
    if test_result_info['time_on'] == None or "":
        now = datetime.now()
        td = timedelta(minutes=float(test_result_info['time_delta']))
        end = now + td
        # Вносим в базу время начала теста.
        write_db_update_ultimate("tests_result", find__chat_id=message.chat.id, find__test_id=testid,
                                 time_on=now, time_off=end)
        td = str(td.seconds // 60) +":" + str(td.seconds - (td.seconds // 60)*60)
    else:
        now = datetime.now()
        end = test_result_info['time_off']
        # end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        if end > now:
            td = end - now
            td = str(td.seconds // 60) +":" + str(td.seconds - (td.seconds // 60)*60)
        else:
            td = "00:00"


    # Формируем форму вопроса.
    keyboard = types.InlineKeyboardMarkup()
    callback_button_1 = types.InlineKeyboardButton(text="1️⃣ ",
                                                   callback_data="testform:1:"+str(questionid)+":"+str(testid))
    callback_button_2 = types.InlineKeyboardButton(text="2️⃣ ",
                                                   callback_data="testform:2:"+str(questionid)+":"+str(testid))
    callback_button_3 = types.InlineKeyboardButton(text="3️⃣ ",
                                                   callback_data="testform:3:"+str(questionid)+":"+str(testid))
    callback_button_4 = types.InlineKeyboardButton(text="4️⃣ ",
                                                   callback_data="testform:4:"+str(questionid)+":"+str(testid))
    callback_button_5 = types.InlineKeyboardButton(text="5️⃣ ",
                                                   callback_data="testform:5:"+str(questionid)+":"+str(testid))
    callback_button_left = types.InlineKeyboardButton(text="⬅Назад",
                                                      callback_data="testform:left:"+str(questionid)+":"+str(testid))
    callback_button_right = types.InlineKeyboardButton(text="Вперед➡",
                                                       callback_data="testform:right:"+str(questionid)+":"+str(testid))
    callback_button_confirm = types.InlineKeyboardButton(text="Ответить этот",
                                                         callback_data="testform:confirm:"+str(questionid)+":"+str(testid))
    callback_button_close = types.InlineKeyboardButton(text="Принять все ответы и завершить",
                                                       callback_data="testform:close:"+str(questionid)+":"+str(testid))

    keyboard.row(callback_button_1, callback_button_2, callback_button_3, callback_button_4, callback_button_5)
    keyboard.row(callback_button_left, callback_button_confirm, callback_button_right)
    keyboard.row(callback_button_close)

    # Генерируем номер вопроса
    generic_questions = ast.literal_eval(test_result_info["generic_questions"])
    nowid = generic_questions.index(int(questionid))
    number_question = "Вопрос: " + str(nowid+1) + "/" + str(len(generic_questions))

    # Генерируем вопрос и вставляем в него номер вопроса.
    question_info = read_db_row("tests", id=str(questionid))
    question = "♦" + number_question + "♦️Осталось 🕑 " + str(td) + "\n\n" + "❓" + question_info['question']



    answer1 = ast.literal_eval(question_info['answers'])[1]
    if 1 in result_previous_local:
        answer1 = "<b>" + "🔘 1️⃣." + str(answer1) + "</b>"
    else:
        answer1 = "<b>" + "⚪ 1️⃣." + str(answer1) + "</b>"

    answer2 = ast.literal_eval(question_info['answers'])[2]
    if 2 in result_previous_local:
        answer2 = "<b>" + "🔘 2️⃣." + str(answer2) + "</b>"
    else:
        answer2 = "<b>" + "⚪ 2️⃣." + str(answer2) + "</b>"

    answer3 = ast.literal_eval(question_info['answers'])[3]
    if 3 in result_previous_local:
        answer3 = "<b>" + "🔘 3️⃣." + str(answer3) + "</b>"
    else:
        answer3 = "<b>" + "⚪ 3️⃣." + str(answer3) + "</b>"

    answer4 = ast.literal_eval(question_info['answers'])[4]
    if 4 in result_previous_local:
        answer4 = "<b>" + "🔘 4️⃣." + str(answer4) + "</b>"
    else:
        answer4 = "<b>" + "⚪ 4️⃣." + str(answer4) + "</b>"

    answer5 = ast.literal_eval(question_info['answers'])[5]
    if 5 in result_previous_local:
        answer5 = "<b>" + "🔘 5️⃣." + str(answer5) + "</b>"
    else:
        answer5 = "<b>" + "⚪ 5️⃣." + str(answer5) + "</b>"

    # Формируем и выводим результат.
    x = (question, answer1,answer2, answer3, answer4, answer5)
    question_text = "<b>%s</b> \n\n <b></b>%s \n <b></b>%s \n <b></b>%s \n <b></b>%s \n <b></b>%s" % x

    if td == "00:00" and test_result_info['result_percent'] is None:
        result = confirm_test(test_result_info['id'])
        bot.send_message(message.chat.id, "Время истекло. Отмеченные вопросы засчитаны. ")

    if test_result_info['result_percent'] is None or test_result_info['result_percent'] == "":

        try:
            bot.edit_message_text(question_text, message.chat.id, message.message_id, parse_mode="HTML")
            bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=keyboard)
        except:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, question_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        bot.delete_message(message.chat.id, message.message_id)
        percent = test_result_info['result_percent']
        keyboard = types.InlineKeyboardMarkup()
        close_button_close = types.InlineKeyboardButton(text="❌Закрыть",
                                                       callback_data="Закрыть")
        keyboard.row(close_button_close)
        bot.send_message(message.chat.id, "Спасибо за прохождение теста. Ожидайте результат. Он вам придет после прохождения теста всеми участниками.",
                         parse_mode="HTML", reply_markup=keyboard)



# **********************Обработчик нажатия кнопок на форме теста*****************************.

def testform_buttons_click(message, data, call):
    #Вытаскиваем данные из call.data.
    button = data.split(':')[1]
    question_id = data.split(':')[2]
    test_id = data.split(':')[3]
    #Забираем из БД всю инфрмацию о созданном тесте (Шаблоне).
    test_info = read_db_row("tests", id=test_id)
    #Забираем из БД информацию о тесте, который проходит конкретный пользователь в данный момент.
    try: # Прверяем есть ли...
        test_result_info = read_db_row("tests_result", test_id=test_id, chat_id=message.chat.id)
    except: #Если нету - создаем...?
        id = write_db_insert("tests_result", chat_id=message.chat.id, test_id=tetst_id)
        test_result_info = read_db_row("tests_result", id=id)
        print("Нет такого теста.... Надо сздать")


    # Вытаскиваем из БД промежуточные результаты result_previous. Формат - {question_id:[1,2,3,4,5],... }
    # Сюда вносятся все промежуточные результаты.
    # Промежуточные результаты отмечаются в тексте вопроса. Для того, чтобы юзер видел, что он навибирал.
    result_previous = test_result_info['result_previous']
    try:
        result_previous = ast.literal_eval(result_previous)
    except:
        result_previous = {}
    result_previous_local = []
    try:
        result_previous_local = list(set(result_previous[(int(question_id))]))
    except:

        print("ОШИБКА result_previous_local 2")


    #Если кнока от 1 до 5.
    for key in range(1,6):
        if button == str(key):
            if key not in result_previous_local:
                result_previous_local.append(key)
                print(result_previous_local)
            else:
                result_previous_local.remove(key)


    generic_questions = ast.literal_eval(test_result_info["generic_questions"])
    nowid = generic_questions.index(int(question_id))

    if button == "left":
        print(nowid)
        if nowid > 0:
            nowid = nowid - 1
        else:
            pass
    elif button == "right":
        idscount = len(generic_questions)-1
        if nowid < idscount:
            nowid = nowid + 1
        else:
            pass
    elif button == "confirm":
        # Сделать проверку на последний вопрос. Если последний - завершить тест.
        if len(generic_questions) > 1:
            #Сделать, чтобы вопрос убирался из списка выдачи(Убрать его из БД из столбца Generic questions).
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Ответ принят. Вопрос убран из списка.")
            generic_questions.pop(nowid)
            nowid = random.randint(0, len(generic_questions))

            #nowid = nowid - 1
        else:
            result = confirm_test(test_result_info['id'])
    # Требуется завершать тест, если проклацаны все ответы.
    elif button == "close":
        result = confirm_test(test_result_info['id'])

    #### Дописать, чтобы при нажатии на кнопку бот сворачивал окно прохождения теста. и переносил данные из временной ячейки в постоянную в БД.
    # Считал результаты теста, выдавал их на экран и благодарил за успешное прохождение!

    result_previous[int(question_id)] = result_previous_local
    write_db_update_ultimate("tests_result", find__chat_id=message.chat.id, find__test_id=test_id,
                             result_previous=result_previous, generic_questions=generic_questions)
    view_test(message, generic_questions[nowid], test_id)


def confirm_test(test_id):
    print("RESULT TEST ID" + str(test_id))
    test_info = read_db_row("tests_result", id=test_id)
    result_previous = ast.literal_eval(test_info['result_previous'])
    test_example_id = test_info['test_id']
    test_example_info = read_db_row("tests_created", id=test_example_id)
    question_numbers = ast.literal_eval(test_example_info['question_ids'])
    trueanswers = {}
    for question in question_numbers:
        question_info = read_db_row("tests", id=question)
        true_answer = ast.literal_eval(question_info['truenumbers'])
        trueanswers[question] = true_answer
    print(trueanswers)
    print(result_previous)
    if result_previous == trueanswers:
        print("ВСе верно!")
    trueanswercount = 0
    for item in trueanswers.keys():
        if trueanswers[item] == result_previous[item]:
            trueanswercount += 1
    answercount = len(trueanswers)
    percent = int(trueanswercount/answercount*100)
    print(percent)
    time=datetime.now()
    write_db_update_ultimate("tests_result", find__id=test_id,
                             result_percent=percent, result_full=result_previous, time_off=time)
    return percent
"""
Пример использования
@bot.message_handler(commands=['12345'])
def test(message):
    pass
    view_test(message, '22', '1')

@bot.callback_query_handler(func=lambda call: "testform" in call.data)
def testform(call):
    testform_buttons_click(call.message, call.data, call)
"""


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ТЕСТИРОВАНИЕ\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# СОЗДАТЬ ТЕСТ ПО НАЗВАНИЮ ТЕСТА

def create_test_on_name(input_call, input_message):
    # Проверяем что из этого настоящий мессэдж, а что обычный текст.
    # try - обработчик первичного коллбэка
    # except - обработчик вторичного ввода (И коллбэки и простые вводы текста)
    try:
        chat_id = input_call.message.chat.id
        # Информация о пользователе, который создает тест.
        user_info = read_db_row("user_base", chat_id=chat_id)
        # Меняем статус в operation.

        write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="Сделать по названию теста")

        # 1.Надо вывести перечень названий тестов, доступных для создания.
        test_names = list(set(read_db_array("tests", "test_name")))
        keyboard = types.InlineKeyboardMarkup()
        for test_name in test_names:
            test_name_button = types.InlineKeyboardButton(text=test_name, callback_data=test_name)
            keyboard.add(test_name_button)
        test_name_button = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
        keyboard.add(test_name_button)
        bot.send_message(chat_id, "Список тестов на выбор", reply_markup=keyboard)

    except:
        # Пихаем еще 1 обработчик ошибок, чтобы разделить вторичный месседж на коллбэк и просто ввод.
        try:
            chat_id = input_message.message.chat.id
            bot.delete_message(chat_id,input_message.message.message_id)
            # Обрабатываем название теста.
            if input_message.data in read_db_array("tests", "test_name"):
                # !Вносим название теста в базу данных(Надо создать новую строку). И массив номеров вопросов тоже!
                question_array = read_db_array("tests", "id", test_name=input_message.data)
                write_db_insert("tests_created", question_ids=question_array, test_name=input_message.data,
                                create_status="Создаётся")

                user_types = list(set(read_db_array("user_base", "user_type")))
                keyboard = types.InlineKeyboardMarkup()
                for user_type in user_types:
                    user_type_button = types.InlineKeyboardButton(text=user_type, callback_data=user_type)
                    keyboard.add(user_type_button)
                close_button = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
                keyboard.add(close_button)
                bot.send_message(chat_id, "Для кого делаем тест?", reply_markup=keyboard)
            # Обрабатываем тип пользователя и просим ввести время на прохождение теста.
            elif input_message.data in read_db_array("user_base", "user_type"):
                # !Вносим ID всех пользователей, для которых хотим провести тест.
                user_ids = read_db_array("user_base", "chat_id", user_type=input_message.data)
                write_db_update_ultimate("tests_created", find__create_status="Создаётся", user_ids=user_ids,
                                         open_status="close", user_type=str(input_message.data))
                bot.send_message(chat_id, "Введите количество минут, за которые надо пройти тест в формате ** минут")


            else:
                pass
        except:
            chat_id = input_message.chat.id
            text = input_message.text
            if "минут" in text:
                delta = int(text.split(" ")[0])
                # delta = datetime.strptime(str(delta), "%M").time()
                # Тут вносим время на проведение теста, переведя в формат времени.
                write_db_update_ultimate("tests_created", find__create_status="Создаётся", time_delta=delta)
                bot.send_message(chat_id, "Сколько дней дается на выполнение? Внесите в формате ** дней")
            elif "дней" in text:
                days = int(text.split(" ")[0])
                # Ну и тут вносим крайний срок выполнения теста(Посчитать ручками)
                now = datetime.now()
                daydelta = timedelta(days=days)
                dateoff = now + daydelta
                # Делаем рассылку юзерам, на которых проведен тест.
                test_info = read_db_row("tests_created", create_status="Создаётся")
                user_ids = test_info['user_ids']
                user_ids = ast.literal_eval(user_ids)
                test_name = test_info['test_name']
                for user_id in user_ids:
                    bot.send_message(user_id, "Появился новый тест, доступный к прохождению!\n"
                                              "Называется " + test_name)

                write_db_update_ultimate("tests_created", find__create_status="Создаётся", time_off=dateoff, time_on=now,
                                         creator_id=chat_id, create_status="Создан")
                # Вывести форму предварительного просмотра с кнопками "Отправить" и "Отменить".

                write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="mainmenu")
                bot.send_message(chat_id, "Тест создан!")


                main_menu_to_user(message=input_message)
            elif len(text)<15:
                bot.send_message(chat_id, "Че-то вынеправильно ввели... Пробуйте еще раз.")
                write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="mainmenu")
                main_menu_to_user(message=input_message)


# ТЕСТЫ ДЛЯ ПРОХОЖДЕНИЯ+ВЫВОД ТЕСТА(ВЗАИМОДЕЙСТВИЕ С МОДУЛЕМ test_func)
def view_test_and_start(input_call, input_message):
    try:
        # Блок обработки первичного инлайна
        print("Выводим перечень тестов для прохождения")
        chat_id = input_call.message.chat.id
        call = input_call
        write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="Надо пройти")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        # 1.Надо показать список тестов, актуальных для прохождения.
        now = datetime.now()
        user_type = read_db_row("user_base", chat_id=chat_id)['user_type']
        try:
            tests_array = read_db_array_universe("tests_created", "id", time_off=">"+str(now), open_status="=close", user_type="="+user_type)
        except:
            tests_array = []

        try:
            complete_array = read_db_array("tests_result", "id", chat_id=call.message.chat.id)
        except:
            complete_array = []

        tests_array = list(set(tests_array) - set(complete_array))
        keyboard = types.InlineKeyboardMarkup()
        for test in tests_array:
            test_info = read_db_row("tests_created", id=test)
            test_button = types.InlineKeyboardButton(text=test_info['test_name'], callback_data="Номер:" + str(test))

            date = test_info['time_off']
            datestring = date.strftime("%d/%m/%Y %H:%M")
            date_button = types.InlineKeyboardButton(text="До "+str(datestring), callback_data="12345")
            keyboard.add(test_button, date_button)
        close_button = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
        keyboard.add(close_button)
        message_text = ""
        if len(tests_array)>0:
            message_text = "Вот список актуальных тестов для Вас:"
        else:
            message_text = "Пока ничего нет."
        bot.send_message(call.message.chat.id, message_text, reply_markup=keyboard)
    except:
        try:
            # Блок обработки вторичного инлайна
            chat_id = input_message.message.chat.id
            call = input_message
            if "Номер" in call.data:
                # Вывод окна предварительного просмотра теста
                test_id = call.data.split(":")[1]
                keyboard = types.InlineKeyboardMarkup()
                test_button_start = types.InlineKeyboardButton(text="Начать", callback_data="Начать:"+str(test_id))
                test_button_close = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
                keyboard.row(test_button_start, test_button_close)
                test_info = read_db_row("tests_created", id=test_id)
                x = (test_info['test_name'], str(test_info['question_ids'].count(",")+1), test_info['time_off'], test_info['time_delta'])
                test_detail = "Название теста: %s \nКоличество вопросов: %s \nПройти до: %s \nВремя на прохождение %s минут." % x
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, test_detail, reply_markup=keyboard)

            if "Начать" in call.data:
                test_id = call.data.split(":")[1]
                test_info = read_db_row("tests_created", id=test_id)
                question_ids = ast.literal_eval(test_info['question_ids'])
                test_name = test_info['test_name']
                time_delta = test_info['time_delta']
                id = write_db_insert("tests_result", chat_id=call.message.chat.id, test_id=test_id,
                                     generic_questions=question_ids, test_name=test_name, time_delta=time_delta)
                view_test(call.message, str(question_ids[0]), str(test_id))
            else:
                pass

            if "testform" in call.data:
                testform_buttons_click(call.message, call.data, call)

        except:
            # Блок обработки вторичного ввода текста.
            chat_id = input_message.chat.id
            message = input_message
            text = message.text
            if text == "Главное меню":
                bot.send_message(message.chat.id,
                                 "Выйти из теста нельзя. Вы можете завершить тест, при этом все разультаты будут зафиксированы.")
                # Находим какой тест выполняет Жора и еще раз закидываем ему это окно.
                # Это надо выцепить на каком вопросе он находится и какой test_id у выполняемого теста в БД test_result
                #
                # test_info = read_db_row("tests_result", chat_id=message.chat.id, status="Проходится")
                # question_ids = ast.literal_eval(test_info['generic_questions'])
                # test_id = test_info['test_id']
                # view_test(message, str(question_ids[0]), str(test_id))
            else:
                bot.send_message(message.chat.id, "Писать бессмысленно... Нажимайте лучше кнопки. Или нажмите Главное меню, если закончили...")


# Добавление новых вопросов для тестов через документ.
def add_new_questions(input_call, input_message):
    try:
        # Блок обработки первичного инлайна
        chat_id = input_call.message.chat.id
        call = input_call
        write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="Добавить вопросы")
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Теперь можно добавлять вопросы тестов.\nПеретяните Excel документ в чат.\n",
                                  show_alert=True)
    except:
        try:
            # Блок обработки вторичного инлайна
            chat_id = input_message.message.chat.id
            call = input_message
            if "Добавить" in call.data:
                print("Добавляем вопрос")
                confirm_question(call)
            elif "Удалить вопрос" in call.data:
                remove_question(call)
        except:
            # Блок обработки вторичного ввода текста.
            chat_id = input_message.chat.id
            message = input_message

            try:
                input_document_question(message)
            except:
                if message.text == "Главное меню":
                    write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="mainmenu")
                    main_menu_to_user(message=input_message)
                else:
                    bot.send_message(message.chat.id,
                                     "Нече писать. Документ скинь...")



# РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ для администратора!!!!!!

def admin_tests_result(input_call, input_message):
    try:
        # Блок обработки первичного инлайна
        chat_id = input_call.message.chat.id
        call = input_call
        write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="Итоги тестов")
        # Первично выводим 4 временных промежутка. Актуальные, За месяц, за 2, за 3.

        # Формируем массив из периодов
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = periods_keyboard(call)
        bot.send_message(call.message.chat.id, "Выберите временной промежуток", reply_markup=keyboard)

    except:
        try:
            # Блок обработки вторичного инлайна
            chat_id = input_message.message.chat.id
            call = input_message
            # Обработка при нажатии на временной промежуток.
            print("Выполнение вторичного инлайна! " + call.data)
            if "cal:" in call.data:
                periods_keyboard_onclick(call)
            # Обработка при нажатии на наименование теста во временном промежутке.
            if "test_id" in call.data:
                open_test_info(call)
            # Обработка кнопки "Вскрыть результаты"
            if "Отправить результаты" in call.data:
                send_result(call)
            # Обработка кнопки "Напомнить о тесте"
            if "Напомнить:" in call.data:
                print("Напоминаем!")
                remember_test(call)
            # Обработка кнопки "Скачать отчет"

            # Обработка кнопки "Свернуть"
            if "Свернуть" in call.data:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            # Обработка кнопки "Добавить польщователей"
            if "Добавить пользователей" in call.data:
                add_users_to_test(call)

        except:
            # Блок обработки вторичного ввода текста.
            chat_id = input_message.chat.id
            message = input_message
            text = message.text
            # Обработка ввода сопровод. текста при вскрытии результатов.Добавить в test_created колонку open_text

            write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="mainmenu")
            main_menu_to_user(message=input_message)

# Функция формирует клавиатуру - календарь с возможностью выбрать период.
def periods_keyboard(call):
    # Забиваем словарь с месяцами и номерами.
    months = {
        1: "Январь",
        2: "Февраль",
        3: "Март",
        4: "Апрель",
        5: "Май",
        6: "Июнь",
        7: "Июль",
        8: "Август",
        9: "Сентябрь",
        10: "Октябрь",
        11: "Ноябрь",
        12: "Декабрь"
    }
    if "cal:year" in call.data:
        now_year = call.data.split(":")[2]
        next_year = int(now_year) + 1
        prev_year = int(now_year) - 1
    else:
        now = datetime.now()
        now_year = now.year
        next_year = int(now_year) + 1
        prev_year = int(now_year) - 1

    keyboard = types.InlineKeyboardMarkup()

    year = types.InlineKeyboardButton(text=str(now_year), callback_data="12345")
    left_year = types.InlineKeyboardButton(text="<=", callback_data="cal:year:" + str(prev_year))
    right_year = types.InlineKeyboardButton(text="=>", callback_data="cal:year:" + str(next_year))
    keyboard.row(left_year, year, right_year)

    tests_count = {}
    for i in range(1,13):
        month = str(i)
        year = str(now_year)
        if len(month) < 2:
            month = "0" + month
        datefrom = (year, month)
        datefrom_info = "%s-%s" % datefrom
        try:
            ids = read_db_array_like("tests_created", "id", time_off=datefrom_info)
        except:
            ids = []
        tests_count[i] = len(ids)

    for i in range(1, 12, 3):


        btn1 = types.InlineKeyboardButton(text=months[i] + "(" + str(tests_count[i])+ ")",
                                          callback_data="cal:month:" + str(i) + ":" + str(now_year))
        btn2 = types.InlineKeyboardButton(text=months[i+1] + "(" + str(tests_count[i+1])+ ")",
                                          callback_data="cal:month:" + str(i+1) + ":" + str(now_year))
        btn3 = types.InlineKeyboardButton(text=months[i+2] + "(" + str(tests_count[i+2])+ ")",
                                          callback_data="cal:month:" + str(i+2) + ":" + str(now_year))
        keyboard.row(btn1, btn2, btn3)


    close = types.InlineKeyboardButton(text="Закрыть", callback_data="Закрыть")
    keyboard.row(close)

    return keyboard

def periods_keyboard_onclick(call):
    if "cal:year" in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = periods_keyboard(call)
        bot.send_message(call.message.chat.id, "Выберите временной промежуток", reply_markup=keyboard)
    elif "cal:month" in call.data:
        month = call.data.split(":")[2]
        year = call.data.split(":")[3]
        if len(month) < 2:
            month = "0" + month
        datefrom = (year, month)
        datefrom_info = "%s-%s" % datefrom
        try:
            tests_ids = read_db_array_like("tests_created", "id", time_off=datefrom_info)
        except:
            tests_ids = []
        if len(tests_ids) > 0:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for test_id in tests_ids:
                test_info = read_db_row("tests_created", id=test_id)
                if test_info['open_status'] == "close":
                    status_icon = ""
                else:
                    status_icon = ""
                if test_info['time_off'] < datetime.now() and test_info['open_status'] == "close":
                    date_icon = "🆘"
                elif test_info['time_off'] > datetime.now() and test_info['open_status'] == "close":
                    date_icon = "✳️"
                else:
                    date_icon = "🆗"
                name_button = types.InlineKeyboardButton(text=status_icon + date_icon + "До " + str(test_info['time_off'])[:-9] + " 🔳" + test_info['test_name'], callback_data="test_id:"+str(test_id))
                # date_button = types.InlineKeyboardButton(text="До " + str(test_info['time_off'])[:-16], callback_data="12345")
                # status_button = types.InlineKeyboardButton(text=test_info['open_status'], callback_data="12345")
                keyboard.row(name_button)
                # keyboard.row(date_button, status_button)
            hide_button = types.InlineKeyboardButton(text="Свернуть", callback_data="Свернуть")
            keyboard.row(hide_button)
            bot.send_message(call.message.chat.id, "Перечень тестов за выбранный месяц", reply_markup=keyboard)
    else:
        pass

def open_test_info(call):
    test_id = call.data.split(":")[1]
    test_info = read_db_row("tests_created", id=test_id)
    user_ids = ast.literal_eval(test_info['user_ids'])

    test_name = str(test_info['test_name'])
    creator = str(test_info['creator_id'])
    open_status = str(test_info['open_status'])
    time_on = str(test_info['time_on'])[:-7]
    time_off = str(test_info['time_off'])[:-16]
    user_info_text = ""
    for user_id in user_ids:
        user_info = read_db_row("user_base", chat_id=user_id)
        try:
            user_test_info = read_db_row("tests_result", chat_id=user_id, test_id=test_id)
            result = str(user_test_info['result_percent'])
        except:
            result = "Еще не прошел"
        user_info_text += str(str(user_info['full_name']) + " " + str(result) + "% \n")


    output_text = "<b>Название теста: </b>" + str(test_name) + "\n\n " \
                  "<b>Создан пользователем: </b> " + str(creator) + " \n " \
                  "<b>Открыты ли результаты: </b> " + str(open_status) + " \n " \
                  "<b>Создан: </b> " + str(time_on) + " \n " \
                  "<b>Пройти до: </b> " + str(time_off) + " \n " \
                  "<b>Результаты:</b> \n " + str(user_info_text) + " "

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    send_button = types.InlineKeyboardButton(text="Отправить результаты", callback_data="Отправить результаты:"+str(test_id))
    keyboard.row(send_button)
    remember_button = types.InlineKeyboardButton(text="Напомнить", callback_data="Напомнить:" + str(test_id))
    keyboard.row(remember_button)
    add_button = types.InlineKeyboardButton(text="Добавить пользователей", callback_data="Добавить пользователей:" + str(test_id))
    keyboard.row(add_button)
    hide_button = types.InlineKeyboardButton(text="Свернуть", callback_data="Свернуть")
    keyboard.row(hide_button)

    bot.send_message(call.message.chat.id, output_text, parse_mode="HTML", reply_markup=keyboard)

def send_result(call):
    test_id = call.data.split(":")[1]
    test_info = read_db_row("tests_created", id=test_id)
    time_on = str(test_info['time_on'])[:-16]
    time_off = str(test_info['time_off'])[:-16]
    test_name = str(test_info['test_name'])
    user_ids = ast.literal_eval(test_info['user_ids'])
    for user_id in user_ids:
        user_info = read_db_row("user_base", chat_id=user_id)
        try:
            user_test_info = read_db_row("tests_result", chat_id=user_id, test_id=test_id)
            result = str(user_test_info['result_percent']) + " %"
        except:
            result = "отсутствует. Тест не был пройден в отведенные сроки."

        text = ("‼️\nC " + time_on + " по " + time_off + " проводился тест с названием <b>" + test_name + "</b>" +
                "\nНа данный момент тест завершен. \nВаш результат : " + result)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        hide_button = types.InlineKeyboardButton(text="Свернуть", callback_data="Свернуть")
        keyboard.row(hide_button)
        bot.send_message(user_id, text, parse_mode="HTML")
    # Меняем статус теста на "Open", что значит "Результаты показывать" а сам тест не показывать.
    write_db_update_ultimate("tests_created", find__id=test_id, open_status="open")


def remember_test(call):
    test_id = call.data.split(":")[1]
    test_info = read_db_row("tests_created", id=test_id)
    user_ids = ast.literal_eval(test_info['user_ids'])
    complete_user_ids = read_db_array("tests_result", "chat_id", test_id=test_id)
    uncomplete_user_ids = list(set(user_ids) - set(complete_user_ids))
    test_name = str(test_info['test_name'])
    time_off = str(test_info['time_off'])[:-16]
    text = "‼️Внимание! Сейчас проходит тест с названием <b>" + test_name + "</b>.\nЕго требуется пройти до " + time_off
    for user_id in uncomplete_user_ids:
        bot.send_message(user_id, text, parse_mode="HTML")


def add_users_to_test(call):
    pass
    test_id = call.data.split(":")[1]
    # Выкатить вариант: по категории и по пользователям.
    # По нажатии на категорию выскакивают кнопки "Добавить всех" или Посмотреть всех.
    # Посмотреть список -   выкатывается список участников категории, которых нет в этом тесте.
    # Можно добавлять по нажатии на человека нового участника к тесту.


# Обработка показа товара в базе знаний.
def view_goose_menu(input_call, input_message):
    print("Выводим перечень производителей товара")
    try:
        # Блок обработки первичного инлайна
        chat_id = input_call.message.chat.id
        call = input_call
        write_db_update_ultimate("user_base", find__chat_id=chat_id, operation=call.data)

        bot.delete_message(call.message.chat.id, call.message.message_id)
        brands = read_db_array('goose', "brand", category=str(call.data))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for brand in set(brands):
            callback_button = types.InlineKeyboardButton(text=brand, callback_data=str(brand))
            keyboard.row(callback_button)
        # Добавляем к списку меню кнопку "Назад"
        callback_button = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        keyboard.row(callback_button)
        bot.send_message(call.message.chat.id, "<b>" + call.data + "</b>", reply_markup=keyboard, parse_mode="HTML")
    except:
        try:
            # Блок обработки вторичного инлайна
            chat_id = input_message.message.chat.id
            call = input_message


            # Вывод перечня производителей.
            if call.data in read_db_array("goose", "brand"):
                # bot.delete_message(call.message.chat.id, call.message.message_id)
                gooses = read_db_array('goose', "name", brand=str(call.data))
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                for goose in set(gooses):
                    callback_button = types.InlineKeyboardButton(text=goose, callback_data=str(goose))
                    keyboard.row(callback_button)
                # Добавляем к списку меню кнопку "Назад"
                callback_button = types.InlineKeyboardButton(text="Свернуть", callback_data="Свернуть")
                keyboard.row(callback_button)
                bot.send_message(call.message.chat.id, "<b>" + call.data + "</b>", reply_markup=keyboard, parse_mode="HTML")

            # Вывод информации о товаре.
            elif call.data in read_db_array("goose", "name"):

                goose_info = read_db_row("goose", name=call.data)
                goose_message = ""
                item1 = ""
                goose_id = goose_info['id']
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
                    goose_message +="⚠️" + "<b>" + str(item1) + "</b>" + "\n" + str(goose_info[item]) + "\n"

                # +Добавляем кнопку "Закрыть и Добавить примечание"
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Свернуть", callback_data="Свернуть")
                callback_button1 = types.InlineKeyboardButton(text="Примечание",
                                                              callback_data="Добавить примечание:Юзер:" + str(goose_id))
                keyboard.add(callback_button)
                keyboard.add(callback_button1)
                # Cообщение вывода информации о товаре.
                bot.send_message(call.message.chat.id, goose_message, parse_mode="HTML", disable_web_page_preview=False,
                                 reply_markup=keyboard)

            # Обработка кнопки "Свернуть"
            elif "Свернуть" in call.data:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            # Обработка кнопки "Назад"
            elif "Назад" in call.data:
                write_db_update_ultimate("user_base", find__chat_id=call.message.chat.id, operation="mainmenu")
                main_menu_to_user(call=call)
                bot.answer_callback_query(call.id, "Нажмите еще раз")
            elif "примечание" in call.data:
                edit_comment(call)


        except:
            # Блок обработки вторичного ввода текста.
            chat_id = input_message.chat.id
            message = input_message
            text = message.text
            if text == "Главное меню":
                write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="mainmenu")
                main_menu_to_user(message=input_message)
            else:
                edit_comment_confirm(message)

def edit_comment(call):
    # Разбиваем коллбэк на данные
    user_type = call.data.split(":")[1]
    goose_id = call.data.split(":")[2]
    write_db_insert("utility", chat_id=call.message.chat.id, operand="goose_id", value=goose_id)
    if user_type == "Юзер":
        bot.send_message(call.message.chat.id, "Введите Ваш комментарий формате Фамилия:Примечание ")
    else:
        pass  # !!!!Добавление комментария для администратора. В перспективе возможность добавления модерации.

def edit_comment_confirm(message):
    #Разбиваем на данные
    goose_id = read_db_row("utility", chat_id=message.chat.id, operand="goose_id")['value']
    goose_comment = read_db_row("goose", id=goose_id)['comments']
    if "None" in str(goose_comment):
        goose_comment = ""
    goose_comment = str(goose_comment) + "\n"+message.text
    write_db_update_ultimate("goose", find__id=goose_id, comments=goose_comment)
    msg = bot.send_message(message.chat.id, "Комментарий добавлен")
    time.sleep(1)
    deteterow_db_universe("utility", "chat_id", message.chat.id)
    bot.delete_message(message.chat.id, msg.message_id)
