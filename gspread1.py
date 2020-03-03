import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('snproject-3043198-d1e8f2c87291.json', scope)
client = gspread.authorize(credentials)

sheet = client.open('Прозвон клиентов').sheet1

all = sheet.get_all_records()
for a in all:

    print(a)