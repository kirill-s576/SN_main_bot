import requests
from http.client import HTTPSConnection
from base64 import b64encode
import base64
import datetime
import json
import ast
import telebot
import os  # библиотека для работы с файлами и каталогами
import openpyxl  # библиотека для обработки Excel-файлов

token = "760178208:AAFT7Qdk5Hfv3lwQthh6vykwGCpSxa6yT2U"
bot = telebot.TeleBot(token)


username = "sigaretnet"
password = "s535ab"

log = (username,password)

def get_status(ApplicationNumber):
    logAndPAss = base64.b64encode(b"sigaretnet:s535ab")  # Кодируем логин и пароль в base64
    host = 'https://mobile.ideabank.by/services/v2/shop/getExternalOrderStatus'
    logAndPAss = str(logAndPAss)[1:].replace("'", "")
    header = {'Content-Type': 'application/json', 'Authorization': '%s' % logAndPAss}  # Формируем header
    # Отправляем POST - запрос.
    resp = requests.post(host, data='{"ApplicationNumber": "%s"}' % ApplicationNumber, headers=header)
    print(resp.text)
    my_dict = ast.literal_eval(resp.text)
    decode = {}
    decode[1] = "Received (Получена банком)"
    decode[2] = "Identify (Закреплена за пользователем - клиент авторизовался)"
    decode[3] = "Sent (Анкета заполнена и отправлена на рассмотрение)"
    decode[4] = "Sign (Договор подписан)"
    decode[5] = "Cancel (Отменена пользователем)"
    decode[6] = "Deny (отказ банка)"
    decode[7] = "Invalid (Заявка не найдена илиистек срок действия заявки)"
    decode[8] = "Отменена банком при рассмотрении"
    decode[9] = "Отказ клиента при звонке КЦ"
    decode[10] = "Заявка одобрена Банком"

    return decode[my_dict['Status']]

def send_order(message, ApplicationNumber):
    # Получаем и сохраняем отправленный в телеграм файл.
    name = message.document.file_name
    document = message.document.file_id
    file_info = bot.get_file(document)
    downloaded_file = bot.download_file(file_info.file_path)
    new_path = "/SNtelebot/" + name
    with open(new_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Обрабатываем Excel документ
    excel = openpyxl.load_workbook(new_path)
    sheet = excel.get_sheet_by_name("Form")
    order = {}
    order["ShopName"] = "sigaretnet.by"
    order['PhoneShop'] = "+375296621313"
    #Дата в формате... Хуевом формате.
    nowdate = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S")
    order["Date"] = str(nowdate)
    order['Product'] = "1"
    order["ApplicationNumber"] = str(ApplicationNumber)
    order["FirstName"] = sheet['B3'].value
    order["LastName"] = sheet['B2'].value
    order["MiddleName"] = sheet['B4'].value
    order["FullNameStr"] = order['LastName']+" "+order['FirstName']+" "+order['MiddleName']
    order["PhoneContact"] = "+" + str(sheet['B5'].value)
    order["Term"] = str(sheet['B7'].value)
    order["TotalPrice"] = str(sheet['D23'].value)
    order["CreditAmount"] = str(sheet['D23'].value)
    goosearray = []
    for cell in range(11,21):
        if sheet['A%s' % cell].value is not None:
            goose = {}
            goose["ProductName"] = str(sheet["A%s" % cell].value)
            goose["Modification"] = str(sheet["D%s" % cell].value)
            goose["ProductPrice"] = str(sheet["B%s" % cell].value)
            goose["Quantity"] = str(sheet["C%s" % cell].value)
            goose["ShippingPrice"] = "0"
            goosearray.append(goose)

    order['ProductOrder'] = goosearray
    # Удаляем уже ненужный файл.
    os.remove(new_path)
    #Отправляем сформированную строку в банк
    logAndPAss = base64.b64encode(b"sigaretnet:s535ab")  # Кодируем логин и пароль в base64
    host = 'https://mobile.ideabank.by/services/v2/shop/setExternalOrder'
    logAndPAss = str(logAndPAss)[1:].replace("'", "")

    print(logAndPAss)

    header = {'Content-Type': 'application/json', 'Authorization': '%s' % logAndPAss}  # Формируем header
    jsonorder = json.dumps(order)
    print(jsonorder)
    resp = requests.post(host, data=jsonorder, headers=header)  # Отправляем POST - запрос.
    # Передаваемые данные с номером заявки

    my_dict = ast.literal_eval(resp.text)
    print(my_dict)
    return order
"""{
"ShopName": "sigaretnet.by",
"PhoneShop": "375296621313",
"ShopURL": "http://www.sigaretnet.by/",
"ShopLogo": "http://www.sigaretnet.by/images/logo.png",
"ApplicationNumber": "",
"Product": "1",
"Term": "",
"LastName": "",
"FirstName": "",
"MiddleName": "",
"FullNameStr": "",
"PhoneContact": "",
"ProductOrder": [
{
"ProductName": "",
"Modification": "",
"Quantity": "",
"ProductPrice": "",
"ShippingPrice": "0",
}
],
"TotalPrice": "",
}"""






"""
logAndPAss = base64.b64encode(b"sigaretnet:s535ab") # Кодируем логин и пароль в base64
host = 'https://mobile.ideabank.by/services/v2/shop/getExternalOrderStatusList'
logAndPAss = str(logAndPAss)[1:].replace("'", "")

print(logAndPAss)

header = {'Content-Type': 'application/json', 'Authorization': '%s' % logAndPAss} # Формируем header

resp = requests.post(host, data='{"DateFrom": "2019-04-01T00:00:00","DateTo": "2019-04-05T00:00:00"}', headers=header) #Отправляем POST - запрос.
                           # Передаваемые данные с номером заявки

print(resp.text) # Выводим результат POST - запроса

my_dict = ast.literal_eval(resp.text)
my_dict = my_dict['OrderList']
for element in my_dict:
    print(element)
"""
"""
# ШАБЛОН СТАНДАРТНОГО ОБРАБОТЧИКА 
def view_test_and_start(input_call, input_message):

try:
        # Блок обработки первичного инлайна
        chat_id = input_call.message.chat.id
        call = input_call
        write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="Сделать по названию теста")

    except:
        try:
            # Блок обработки вторичного инлайна
            chat_id = input_message.message.chat.id
            call = input_message

        except:
            # Блок обработки вторичного ввода текста.
            chat_id = input_message.chat.id
            message = input_message
            text = message.text

            write_db_update_ultimate("user_base", find__chat_id=chat_id, operation="mainmenu")
            main_menu_to_user(message=input_message)

"""