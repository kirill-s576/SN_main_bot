import pymysql
import pymysql.cursors


def connect_db():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='telegramusers',
                                 )

    return connection

def read_db(ID, Param):
    #Функция возвращает значение ячейки по  UserID и указанному столбцу.

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='telegramusers',
                                 )
    cursor = connection.cursor()

    x=(Param,ID)
    mySQLQuery = "SELECT %s FROM TelegramBase WHERE UserID = '%s'" % x

    cursor.execute(mySQLQuery)
    result = cursor.fetchone()
    if result == None :
        connection.close()
        return "Null"
    else:
        connection.close()
        return result[0]

def write_db(ID, Param, Value):
#Функция записывает в ячейку таблицы указанное значение. Исходные значения UserID, какую колонку заполняем, значение.

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='telegramusers',
                               )
    cursor = connection.cursor()
    if read_db(ID, "UserID") == ID:
          #Функция замены.
        x = (Param, Value, ID)
        mySQLQuery = "UPDATE TelegramBase SET %s='%s' WHERE UserID='%s'" % x

    else: #Функция добавления записи в конец списка.
        print("вапвапа")
        x = (Param, ID, Value)
        mySQLQuery = "INSERT INTO TelegramBase (UserID,%s) VALUES('%s','%s')" % x


    cursor.execute(mySQLQuery)
    connection.commit()
    connection.close()