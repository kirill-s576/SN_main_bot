import telebot
from telebot import types
import bdfunc
from bdfunc import *
import datetime
from datetime import *

token = "760178208:AAFT7Qdk5Hfv3lwQthh6vykwGCpSxa6yT2U"
bot = telebot.TeleBot(token)

openshops = read_db_array("dailycheck", "user_name", check_name="Открытие смены", date=str(date.today()))

regionshops = read_db_array("telegrambase", "UserName", UserType = "Продавец", Groups="Region")

for shop in regionshops:
	if shop in openshops:
		bot.send_message ("356080087", str(shop)+ " открыт.")
		bot.send_message ("390901374", str(shop)+ " открыт.")
	else:
		bot.send_message ("356080087", str(shop)+ " закрыт.")
		bot.send_message ("390901374", str(shop)+ " закрыт.")




siluetshops = read_db_array("telegrambase", "UserName", UserType = "Продавец", Groups="Siluet")


for shop in siluetshops:
	if shop in openshops:
		bot.send_message ("481707377", str(shop)+ " открыт.")
	else:
		bot.send_message ("481707377", str(shop)+ " закрыт.")



