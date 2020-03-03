import pymysql
import pymysql.cursors

def connect_db():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1357908642',
                                 db='phpmyadmin',
                                 )

    return connection


"""**************************************************************************************************************"""


"""Функции для работы с базой данных telegrambase. Ну их нахуй..."""

"""*******************************************************************"""
def read_db(ID, Param, DB):
    #Функция возвращает значение ячейки по  UserID и указанному столбцу.
    connection = connect_db()
    cursor = connection.cursor()
    x=(Param,DB,ID)
    mySQLQuery = "SELECT %s FROM %s WHERE UserID = '%s'" % x
    cursor.execute(mySQLQuery)
    result = cursor.fetchone()
    connection.close()
    if result == None:
        return None
    else:
        return result[0]

def read_db_simple(ID, Param, DB):
    #Функция возвращает значение ячейки по  UserID и указанному столбцу.
    connection = connect_db()
    cursor = connection.cursor()
    x=(Param,DB,ID)
    mySQLQuery = "SELECT %s FROM %s WHERE UserID = '%s'" % x
    cursor.execute(mySQLQuery)
    result = cursor.fetchone()
    connection.close()
    if result == None:
        return None
    else:
        return result[0]


"""***************************************************************"""

def deteterow_db(ID,DB):
    #Функция Удаляет строку БД по ID
    connection = connect_db()
    cursor = connection.cursor()
    x=(DB,ID)
    mySQLQuery = "DELETE FROM %s WHERE UserID = '%s'" % x
    cursor.execute(mySQLQuery)
    connection.commit()
    connection.close()

def deteterow_db_universe(DB, Param, Value):
    #Функция Удаляет строку БД по ID
    connection = connect_db()
    cursor = connection.cursor()
    x=(DB,Param,Value)
    mySQLQuery = "DELETE FROM %s WHERE %s = '%s'" % x
    cursor.execute(mySQLQuery)
    connection.commit()
    connection.close()

"""***************************************************************"""

def write_db(ID, Param, DB, Value):
#Функция записывает в ячейку таблицы указанное значение. Исходные значения UserID, какую колонку заполняем, значение.

    connection = connect_db()
    cursor = connection.cursor()
    if read_db(ID, "UserID",DB) == ID:
          #Функция замены.
        x = (DB, Param, Value, ID)
        mySQLQuery = "UPDATE %s SET %s='%s' WHERE UserID='%s'" % x
    else: #Функция добавления записи в конец списка.
        x = (DB, Param, ID, Value)
        mySQLQuery = "INSERT INTO %s (UserID,%s) VALUES('%s','%s')" % x
    cursor.execute(mySQLQuery)
    connection.commit()
    connection.close()



"""***************************************************************"""

def read_db_universe(DB, Param1, Param2, Value):
    #Функция возвращает значение ячейки по  UserID и указанному столбцу.
    connection = connect_db()
    cursor = connection.cursor()
    x=(Param1,DB,Param2, Value)
    mySQLQuery = "SELECT %s FROM %s WHERE %s = '%s'" % x
    cursor.execute(mySQLQuery)
    result = cursor.fetchone()
    connection.close()
    if result == None:
        return None
    else:
        return result[0]


"""База данных/ перечень параметов, которые надо записать в строку"""
def write_db_insert(DB, **data):

    if "dictionary" not in data.keys():
        keytext = " "
        valuetext = " "
        if len(data.items()) > 0:

            for key, value in data.items():
                keytext = keytext + str(key) + ","
                valuetext = valuetext  + '"' +  str(value) + '"' + ","
            try:
                keytext = keytext[:-1]
                valuetext = valuetext[:-1]
                connection = connect_db()
                cursor = connection.cursor()
                x = (DB, keytext, valuetext)
                mySQLQuery = "INSERT INTO %s (%s) VALUES (%s)" % x
                print(mySQLQuery)
                cursor.execute(mySQLQuery)
                id = cursor.lastrowid
                connection.commit()
                connection.close()
                return id
            except:
                print("ОШИБКА" + str(mySQLQuery))
        else:
            print("Ошибка write_db_insert" + str(data))
    else:
        keytext = " "
        valuetext = " "

        for k, v in data.items():
            dictionary = v
            for key in dictionary:
                keytext = keytext + str(key) + ","
                valuetext = valuetext + '"' + str(dictionary[key]) + '"' + ","
            try:
                keytext = keytext[:-1]
                valuetext = valuetext[:-1]
                connection = connect_db()
                cursor = connection.cursor()
                x = (DB, keytext, valuetext)
                mySQLQuery = "INSERT INTO %s (%s) VALUES (%s)" % x
                cursor.execute(mySQLQuery)
                id = cursor.lastrowid
                connection.commit()
                connection.close()
                return id
            except:
                print("2"+str(mySQLQuery))


"""База данных/1! Условие/Перечень параметров, которые меняем"""
def write_db_update(DB, **data):
    try:
        num = " "
        if len(data.items()) > 0:
            subquery = "SET"
            subquery1 = ""
        else:
            subquery = " "
        i=1
        for key, value in data.items():
            if i== 1:
                subquery1 = "WHERE " + str(key) + " = '" + str(value) + "'"
                i = i+1
            else:
                id = num + str(key) + " = '" + str(value) + "' "
                subquery = subquery + id
                num = " , "



        connection = connect_db()
        cursor = connection.cursor()
        x = (DB,subquery, subquery1)
        mySQLQuery = "UPDATE %s %s %s" % x
        cursor.execute(mySQLQuery)
        connection.commit()
        connection.close()
    except:
        print("Ошибка write_db_update"+ str(data))




"""Полное обновление строки. Ищем строку по нескольким параметрам. К параметам условвия добавляем find__, которые надо перезаписать - просто пишем."""
def write_db_update_ultimate(DB, **data):
    try:
        num = " "
        if len(data.items()) > 0:
            subquery = "SET"
            subquery1 = ""
        else:
            subquery = " "
        where = "WHERE"
        andy = ""
        for key, value in data.items():

            if "find" in str(key):
                key = key.split("__")[1]

                subquery1 = subquery1 + " " + str(andy)+ " " +str(where)+ " " + str(key) + " = '" + str(value) + "'"
                where = ""
                andy = "AND"

            else:
                id = num + str(key) + " = '" + str(value) + "' "
                subquery = subquery + id
                num = " , "



        connection = connect_db()
        cursor = connection.cursor()
        x = (DB,subquery, subquery1)
        mySQLQuery = "UPDATE %s %s %s" % x
        print(mySQLQuery)
        cursor.execute(mySQLQuery)
        connection.commit()
        connection.close()
    except:
        print("Ошибка write_db_update"+ str(data))
"""**************************************************************************************************************"""



"""Блок фунций для работы с БД dailycheck"""
"""id      chat_id   user_name   worker      check_name   status            result                    date       time_off   """
"""ясно    ясно      назв маг    фамилия     назв чека    вып или не        возвращенное значение     дата       время вып  """


""" Короче функция выводит массив значений столбца по фильтру. В фильтр можно вставлять любое количество значений"""
def read_dailycheck(DB, Param, **data):
    num = " "

    if len(data.items())>0:
        subquery = "WHERE"

    else:
        subquery = " "

    for key, value in data.items():

        id = num + str(key) + " = '" + str(value) + "'"
        subquery = subquery + id
        num = " AND "
    connection = connect_db()
    cursor = connection.cursor()
    x = (Param, DB, subquery)
    mySQLQuery = "SELECT %s FROM %s %s " % x
    print(mySQLQuery)
    cursor.execute(mySQLQuery)
    param1 = cursor.fetchall()
    connection.close()
    return param1

def read_db_array(DB, Param, **data):
    num = " "

    if len(data.items())>0:
        subquery = "WHERE"

    else:
        subquery = " "

    for key, value in data.items():

        id = num + str(key) + " = '" + str(value) + "'"
        subquery = subquery + id
        num = " AND "
    connection = connect_db()
    cursor = connection.cursor()
    x = (Param, DB, subquery)
    mySQLQuery = "SELECT %s FROM %s %s " % x
    print(mySQLQuery)
    cursor.execute(mySQLQuery)
    param1 = cursor.fetchall()
    connection.close()
    k=[]
    for i in param1:
        k.append(i[0])

    return k

def read_db_array_like(DB, Param, **data):
    num = " "

    if len(data.items())>0:
        subquery = "WHERE"

    else:
        subquery = " "

    for key, value in data.items():

        id = num + str(key) + " LIKE '%" + str(value) + "%'"
        subquery = subquery + id
        num = " AND "
    connection = connect_db()
    cursor = connection.cursor()
    x = (Param, DB, subquery)
    mySQLQuery = "SELECT %s FROM %s %s " % x
    print(mySQLQuery)
    cursor.execute(mySQLQuery)
    param1 = cursor.fetchall()
    connection.close()
    k=[]
    for i in param1:
        k.append(i[0])

    return k

def read_db_array_universe(DB, Param, **data):
    num = " "

    if len(data.items())>0:
        subquery = "WHERE"

    else:
        subquery = " "

    for key, value in data.items():

        id = num + str(key) + str(value)[0]+"'" + str(value)[1:] + "'"
        subquery = subquery + id
        num = " AND "
    connection = connect_db()
    cursor = connection.cursor()
    x = (Param, DB, subquery)
    mySQLQuery = "SELECT %s FROM %s %s " % x
    print(mySQLQuery)
    cursor.execute(mySQLQuery)
    param1 = cursor.fetchall()
    connection.close()
    k=[]
    for i in param1:
        k.append(i[0])

    return k



def read_array_with_not(DB, Param, array):
    subquery = "WHERE NOT ("
    num = False
    for ids in array:
        if num==False:
            subquery = subquery + str(ids)
            num = True
        else:
            subquery = subquery +", AND"+ str(ids)

    connection = connect_db()
    cursor = connection.cursor()
    x = (Param, DB, subquery)
    mySQLQuery = "SELECT %s FROM %s %s " % x

    cursor.execute(mySQLQuery)
    param1 = cursor.fetchall()
    connection.close()
    return param1


#Функция читает всю строку сразу по нескольким параметрам и возвращает словарь Description:value
def read_db_row(DB, **data):
    array={}
    connection = connect_db()
    cursor = connection.cursor()
    subquery = ""
    ifand = ""
    for key, value in data.items():
        subquery += " " + str(ifand) + " " + str(key) + " = '" + str(value)+ "'"
        ifand = "AND"
    x = (DB, subquery)
    mySQLQuery = "SELECT * FROM %s WHERE %s" %x
    print(mySQLQuery)
    cursor.execute(mySQLQuery)
    result = cursor.fetchone()
    field_names = [i[0] for i in cursor.description]
    for j in range(0,len(field_names)):
        try:
            array[field_names[j]] = result[j]
        except:
            print("Ошибка")
    connection.close()
    print(array)
    return array