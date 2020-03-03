#Разобраться почему обновляется время апдейта в базе. Если в базе время не будет обновляться - скорость скрипта увеличится.

import asana2
import asana
import bdfunc
import sntbot
import datetime
from datetime import date
import time
from time import strftime
import telebot
client = asana.Client.access_token('0/9de808358c48f13b938aaf36112e3037')
while True:
    # Получаем массив тасков из проекта Асаны.
    tasks = client.projects.tasks("1111815872858792", {'completed': 'False'})

    for task in tasks:

        #Получаем полный объект таска(Не в краткой записи)
        fulltask = client.tasks.find_by_id(task['id'])

        print(fulltask['name'])
        #if fulltask['completed'] == False:
        #***Присвоение атрибутов таска переменным***
        #Название секции и таска
        taskid=fulltask['id']
        sectionname = fulltask['memberships'][0]['section']['name']
        taskname = fulltask['name']
        #Дата обновления таска в Асане и преобразуем в нормальный формат
        updatedate = fulltask['modified_at']
        if updatedate != None:
            updatedate = updatedate[:-5]
            updatedate = datetime.datetime.strptime(updatedate, "%Y-%m-%dT%H:%M:%S")
            delta = datetime.timedelta(hours=3)  # Добавляем 3 часа, потому что время в асане не наше
            updatedate = updatedate + delta
        else:
            updatedate = ""
        # Дата создания таска в Асане и преобразуем в нормальный формат
        createtedate = fulltask['created_at']
        createtedate = createtedate[:-5]
        createtedate = datetime.datetime.strptime(createtedate, "%Y-%m-%dT%H:%M:%S")
        delta = datetime.timedelta(hours=3)  #Добавляем 3 часа, потому что время в асане не наше
        createdate = createtedate + delta
        # Дата заверщения таска в Асане и преобразуем в нормальный формат
        completedate = fulltask['completed_at']
        if completedate !=None:
            completedate = completedate[:-5]
            completedate = datetime.datetime.strptime(completedate, "%Y-%m-%dT%H:%M:%S")
            delta = datetime.timedelta(hours=3) #Добавляем 3 часа, потому что время в асане не наше
            completedate = completedate + delta
        else:
            completedate = ""
        #Описание таска
        description = fulltask['notes']
        #Кто выполняет - IF, чтобы не вылез тип переменной NoneType
        if str(fulltask['assignee']) == "None":
            assignee = "None"
        else:
            assignee = str(fulltask['assignee']['name'])
        # Статус выполнения - True или False
        completed = fulltask['completed']
        #время обновления таска в mysql
        sqlupdatedate = bdfunc.read_db_universe("asanabase", "sql_update_date", "task_id", taskid)


        #Проверяем есть ли такой таск в БД
        if str(bdfunc.read_db_universe("asanabase", "task_id", "task_id", taskid)) != str(taskid):
            #Если нету - создаем с атрибутами, описанными, выше.
            #Не вносится дата выполнения!
            bdfunc.write_db_insert("asanabase", task_id=taskid, section_name=sectionname, task_name=taskname,
                                       create_date=createdate, update_date=updatedate, assigned_to=assignee,
                                       description=description,sql_update_date = datetime.datetime.today(), completed = completed)
            continue


        #Если есть - надо проверить, есть ли различия с БД, и обновлять только если есть, чтобы не изменилось время обновления в БД без причины.
        #Обновлять только если время изменения таска в асане больше, чем время изменения таска в БД. Обновляем в БД
        elif (str(bdfunc.read_db_universe("asanabase", "section_name", "task_id", taskid)) != str(sectionname) or
              str(bdfunc.read_db_universe("asanabase", "task_name", "task_id", taskid)) != str(taskname) or
              str(bdfunc.read_db_universe("asanabase", "assigned_to", "task_id", taskid)) != str(assignee) or
              str(bdfunc.read_db_universe("asanabase", "completed", "task_id", taskid)) != str(completed) or
              str(bdfunc.read_db_universe("asanabase", "description", "task_id", taskid)) != str(description)):
            print('Обновляем')
            if (updatedate > sqlupdatedate):
                #Проверяем на пустую дату завершения таска. Если пустая - лучше не трогать. Ячейка в БД станет 0000000000000.
                if completedate == "":
                    print('Обновление 1 ')
                    bdfunc.write_db_update("asanabase", task_id=taskid, section_name=sectionname, task_name=taskname,
                                       create_date=createdate, update_date=updatedate, assigned_to=assignee, completed=completed,
                                       description=description)
                else:
                    bdfunc.write_db_update("asanabase", task_id=taskid, section_name=sectionname, task_name=taskname,
                                           create_date=createdate, update_date=updatedate, assigned_to=assignee,
                                           completed=completed, description=description, complete_date=completedate)
                    print('Обновление 2 ')
                continue
        #Если время оьновления в асане меньше, чем время обновления в БД
            elif updatedate < sqlupdatedate:
                # Обновляем при условии, что различие есть и дата изменения в базе больше, чем дата в асане.
                asana2.update_task(taskid,
                                   complete_date=str(bdfunc.read_db_universe("asanabase", "complete_date", "task_id", taskid)),
                                   completed=bdfunc.read_db_universe("asanabase", "completed", "task_id", taskid),
                                   section_name=bdfunc.read_db_universe("asanabase", "section_name", "task_id", taskid),
                                   task_name=bdfunc.read_db_universe("asanabase", "task_name", "task_id", taskid),
                                   description=bdfunc.read_db_universe("asanabase", "description", "task_id", taskid))

    #Проверяем таски, которых еще нет в асане(Они в БД с пустым ID). Добавляем если найдем.
    notids = bdfunc.read_dailycheck("asanabase", "id", task_id = '')
    for notid in notids:
        taskname = bdfunc.read_db_universe("asanabase", "task_name", "id", notid[0])
        sectionname = bdfunc.read_db_universe("asanabase", "section_name", "id", notid[0])
        taskid = asana2.create_task(taskname, sectionname)
        bdfunc.write_db_update("asanabase", id = notid[0],task_id = taskid, completed = False)




    #Начинаем цикл заново.

