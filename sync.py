import asana2
import asana
import bdfunc
import sntbot
import datetime
from datetime import date
import time
from time import strftime
import telebot
client= asana.Client.access_token('0/9de808358c48f13b938aaf36112e3037')


"""Выводим список НЕВЫПОЛНЕННЫХ тасков из БАЗЫ - нам нужны CHATID, ИМЯ ТАСКА, НАЗВАНИЕ СЕКЦИИ(ИМЯ ЧЕКА), Дескрипшн - в БД RESULT - туда записывается ответ, если нужен.  """
"""Циклом проверяем каждый таск Базы на предмет совпадения с асаной. Цикл ищет совпадение в списке из БД, сверяет таск на предмет различий; если есть - перезаписывает туда, где дата изменения раньше"""
"""Различия: статус(выполнено или нет). Ассигнед - если ни на кого - то задача не принята, если ассигнет хот на кого-то - задача выполняется. """
"""Если есть изменения - отправляет сообщение в нужные ChatId, Например продавцам об изменении статуса(Принята к исполнению - Исполнителем, готова."""
"""Далее надо добавить в асану новые таски, которые появились в БД, если таски появились в Асане - их в БД добавлять не надо. Они не будут иметь отношения к продавцам..."""
"""Примечание. Таски надо добавлять в нужную секцию(Имя чека)"""

""" Коли уж на то пошло - добавить сюда напоминалки - типа Время капает, а задача не выполнена!!!! - будет круто"""

"""Скрипт выполняется раз в минуту. Думаю, что на первое время будет достаточно"""


#Перевод времени Асаны в нормальный формат
def asana_date_to_ok(asanadate):

    asanadate = asanadate[:-5]
    asanadate = asanadate.replace('T', ' ')
    asanadate = asanadate.replace('-', ' ')
    asanadate = asanadate.replace(':', ' ')
    date1 = asanadate.split(' ')
    date = {"h":date1[3], "m":date1[4],"s":date1[5],"Y":date1[0],"M":date1[1],"D":date1[2] }
    return(date)

#Перевод дата-времени формата Y-M-D h:m:s в формат асаны
def ok_date_to_asana(okdate):
    okdate = str(okdate)
    okdate = okdate.replace('-', ' ')
    okdate = okdate.replace(':', ' ')
    okdate = okdate.split(' ')
    asanadate =okdate[0]+"-"+okdate[1]+"-"+okdate[2]+"T"+okdate[3]+":"+okdate[4]+":"+okdate[5]+".015Z"
    print(asanadate)
    return str(asanadate)




"""Синхронизация асаны с БД"""
def sincr_bd_to_asana(TaskId):


    #users = asana2.client.users.find_by_id('mr.mcdi.576@gmail.com')
    #id = users['id']
    y = asana2.get_task(TaskId)
    asanaupdatedate = y['modified_at']
    asanaupdatedate = asanaupdatedate[:-5]
    asanaupdatedate = datetime.datetime.strptime(asanaupdatedate, "%Y-%m-%dT%H:%M:%S")
    delta = datetime.timedelta(hours=3)
    asanaupdatedate = asanaupdatedate + delta

    sqlupdatedate = bdfunc.read_db_universe("asanabase", "sql_update_date", "task_id", TaskId)

    if asanaupdatedate<sqlupdatedate:
        asana2.update_task(TaskId,  complete_date = str(bdfunc.read_db_universe("asanabase","complete_date","task_id",TaskId)),
                                    completed = bdfunc.read_db_universe("asanabase","completed","task_id",TaskId),
                                    section_name = bdfunc.read_db_universe("asanabase","section_name","task_id",TaskId),
                                    task_name=bdfunc.read_db_universe("asanabase", "task_name", "task_id", TaskId),
                                    description = bdfunc.read_db_universe("asanabase", "description", "task_id", TaskId))




"""Синхронизация БД с асаной"""
def sincr_asana_to_bd(TaskId):


    y=asana2.get_task(TaskId)

    sectionname = y['memberships'][0]['section']['name']
    taskname = y['name']

    updatedate = y['modified_at']
    updatedate = updatedate[:-5]
    updatedate = datetime.datetime.strptime(updatedate, "%Y-%m-%dT%H:%M:%S")
    delta = datetime.timedelta(hours=3)
    updatedate = updatedate + delta

    createtedate = y['created_at']
    createtedate = createtedate[:-5]
    createtedate = datetime.datetime.strptime(createtedate, "%Y-%m-%dT%H:%M:%S")
    delta = datetime.timedelta(hours=3)
    createdate = createtedate + delta

    completedate = y['completed_at']
    if completedate!= None:
        completedate = completedate[:-5]
        completedate = datetime.datetime.strptime(completedate, "%Y-%m-%dT%H:%M:%S")
        delta = datetime.timedelta(hours=3)
        completedate = completedate + delta
    else:
        completedate = datetime.datetime.strptime("2001-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")

    descript = y['notes']

    asanaupdatedate = y['modified_at']
    asanaupdatedate = asanaupdatedate[:-5]
    asanaupdatedate = datetime.datetime.strptime(asanaupdatedate, "%Y-%m-%dT%H:%M:%S")
    delta = datetime.timedelta(hours=3)
    asanaupdatedate = asanaupdatedate + delta

    sqlupdatedate = bdfunc.read_db_universe("asanabase", "sql_update_date", "task_id", TaskId)

    if str(y['assignee']) == "None":
        assignee = "None"
    else:
        assignee = str(y['assignee']['name'])
    status = str(y['completed'])

    #Если таск существует в БД - обновляем, если нет такого - записываем в БД новый таск.
    if str(bdfunc.read_db_universe("asanabase","task_id","task_id",TaskId)) == str(TaskId) and asanaupdatedate > sqlupdatedate:
        bdfunc.write_db_update("asanabase", task_id=TaskId, section_name=sectionname, task_name=taskname,create_date=createdate,
                               update_date=updatedate, assigned_to=assignee, completed = status, complete_date = completedate, description = descript)
    else:
        bdfunc.write_db_insert("asanabase", task_id = TaskId, section_name = sectionname, task_name = taskname,
                               create_date = createdate, update_date = updatedate, assigned_to = assignee, complete_date = completedate,  description = descript)

def sincr_all():
    #Прогоняем все таски в асане

    tasks = client.tasks.find_by_project('1111815872858792',{"completed":"False"})
    for task in tasks:
        if str(bdfunc.read_db_universe("asanabase", "task_id", "task_id", task['id'])) != str(task['id']):
            sincr_asana_to_bd(task['id'])


        y = asana2.get_task(task['id'])

        asanaupdatedate = y['modified_at']
        asanaupdatedate =asanaupdatedate[:-5]
        asanaupdatedate = datetime.datetime.strptime(asanaupdatedate, "%Y-%m-%dT%H:%M:%S")
        delta = datetime.timedelta(hours = 3)
        asanaupdatedate = asanaupdatedate + delta



        sqlupdatedate = bdfunc.read_db_universe("asanabase", "sql_update_date","task_id",task['id'])


        #Если время обновления в асане больше,чем в базе
        if asanaupdatedate and sqlupdatedate != None:

            if asanaupdatedate > sqlupdatedate:
                print("Асану в базу "+ str(y['name']) + str(asanaupdatedate)+ str(sqlupdatedate))
                sincr_asana_to_bd(task['id'])
            else:
                print("Базу в асану "+ str(y['name']) + str(asanaupdatedate)+ str(sqlupdatedate))
                sincr_bd_to_asana(task['id'])
        else:
            print("Асану в базу")
            sincr_asana_to_bd(task['id'])



    #Проверка и добавление в асану созданных в БД тасков.
    tasks = bdfunc.read_dailycheck("asanabase","task_name", task_id= "")
    for task in tasks:
        print(task[0])
        taskname = task[0]
        print(taskname)
        sectionname = bdfunc.read_db_universe("asanabase","section_name", "task_name", task[0])

        print(sectionname)
        asana2.create_task(taskname, sectionname)

    bdfunc.deteterow_db_universe("asanabase", "task_id","")

