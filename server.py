#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import telebot
import bdfunc
import datetime

liq = {}
liq['segments/10'] = "CASHBACK 20%"
liq['segments/11'] = "Podarok"
liq['segments/12'] = "CASHBACK 20%"
liq['segments/1'] = "CASHBACK 30%"
liq['segments/2'] = "Podarok"
liq['segments/3'] = "CASHBACK 25%"
liq['segments/4'] = "Podarok"
liq['segments/5'] = "CASHBACK 50%"
liq['segments/6'] = "Podarok"
liq['segments/7'] = "CASHBACK 20%"
liq['segments/8'] = "CASHBACK 40%"
liq['segments/9'] = "Podarok"

staff = [
    "CASHBACK 20%",
    "CASHBACK 25%",
    "CASHBACK 30%",
    "CASHBACK 40%",
    "CASHBACK 50%",
    "Podarok"
]
token = "760178208:AAFT7Qdk5Hfv3lwQthh6vykwGCpSxa6yT2U"
bot = telebot.TeleBot(token)
token1 = "817361693:AAFadWYZfaDiu9YUTgvPnNvisdx7-SwYnL4"
bot1 = telebot.TeleBot(token1)

def sendSpeen(message, header):
# Требуется обработать результат вращения спина.
# Если это нужный нам пользвоатель - то обрабатываем. Если нет - нахуй его.

    # Вот сюда записываем актуальную подпись браузера, которую надо будет обрабатывать.
    user = "Mozilla/5.0 (Linux; Android 5.1.1; Lenovo YT3-X50M Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.90 Safari/537.36 OPR/52.4.2517.140781"
    
    speen = ""

    if header['User-Agent'] == user:
        if len(message) == 14:
            speen = liq[message[0:10]]
        else:
            speen = liq[message[0:11]]

        print(speen)
    else:
        pass
        # Обработка ложных срабатываний спина. Можно нихуя не делать.
        print("Подпись браузера не прокатывает")

    if speen != "":
        # Записываем спин в базу данных.
        nowdate = str(datetime.datetime.today())[0:10]

        bdfunc.write_db_insert("wheel_speen", speen_name = speen, date_time = str(nowdate))
        
        # Выводим список спинов за сегодня.
        
        allSpeens = bdfunc.read_db_array_like("wheel_speen", "speen_name", date_time = nowdate)
        newMessage = "**" + speen +  "**" + "\n\n"
        for s in staff:
            k = allSpeens.count(s)
            newMessage += str(s) + "--" + str(k) + "раз" + "\n"

        # Отправляем полученное сообщение
        bot.send_message("356080087", newMessage)
        bot1.send_message("387568054", newMessage)
        bot.send_message("376324171", newMessage)
        bot1.send_message("313237556", newMessage)
    else:
        pass


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        print(post_data.decode('utf-8'))
        param = str(post_data.decode('utf-8'))
        
        sendSpeen(param, self.headers)    
            
        
            
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

def run(server_class=HTTPServer, handler_class=S, port=8084):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()



