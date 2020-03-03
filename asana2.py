import asana
import sys, os
import json
from six import print_
import bdfunc
import time
import datetime


client= asana.Client.access_token('0/9de808358c48f13b938aaf36112e3037')

WORKSPACE_ID="829874196257517"
WORKSPACE_NAME="sigaretnet.by"
LOGISTIKA_ID='1105325346493274'
ShopsChecklist_ID = '1111815872858792'

def user_select_option(message, options):
    option_lst = list(options)
    print_(message)
    for i, val in enumerate(option_lst):
        print_(i, ': ' + str(val['id']) + str(val['name']))
    index = int(input("Enter choice (default 0): ") or 0)
    return option_lst[index]


users = client.users.find_by_id('sigaretnetbymail@gmail.com')
id = users['id']


def get_section(ProjectID,SectionName):
    tasks = client.tasks.find_by_project(ProjectID, {"opt_expand":"id,name,complete,parent"})
    for task in tasks:

            print_(json.dumps(task, indent=2, ensure_ascii=False))
            if task['parent'] is not None:
                assignee = task['parent']['memberships']
                print_(json.dumps(assignee, indent=2, ensure_ascii=False))
                for i in assignee:
                    j = i['section']
                    print(str(j['name']))
                    if SectionName == j['name']:
                        return task['id']
                    else:
                        return None
            else:
                print(task['name']+str(task['id']))



def get_sections_ids(ProjectID):
    """Возвращает массив ID секций в проекте по ID самого проекта"""
    sections = client.sections.find_by_project(ProjectID)
    s=[]
    for section in sections:
        s.append(section['id'])
    return s


def get_tasks_of_section_ids(SectionID):
    """Возвращает массив ID таксков, которые есть в данной секции по ID секции"""
    tasks = client.tasks.find_all(section=SectionID)
    t=[]
    for task in tasks:
        t.append(task['id'])
    return t

def get_section_name(ProjectID,SectionID):

    sections = client.sections.find_by_project(ProjectID)
    for section in sections:
        if str(SectionID) == str(section['id']):
            return section['name']

def get_section_id(ProjectID,SectionName):

    sections = client.sections.find_by_project(ProjectID)
    for section in sections:
        if str(SectionName) == str(section['name']):
            return section['id']

def create_task(TaskNote,SectionName):

    task = client.tasks.create_in_workspace(WORKSPACE_ID, {
                                                            'name': str(TaskNote),
                                                            'projects': ShopsChecklist_ID,
                                                            }
                                            )
    client.tasks.add_project(task['id'], {'project': ShopsChecklist_ID,
                                          'section': str(get_section_id(ShopsChecklist_ID,SectionName))
                                          }
                             )

    print("Задача создана")
    return task['id']


def delete_task(TaskId):
    client.tasks.delete(TaskId)



def update_task(TaskId, **data):
    updatequery = {}
    if len(data.items())>0:
        for key, value in data.items():
            if str(key) == "completed":
                updatequery["completed"]=str(value)
            if str(key) == "task_name":
                updatequery["name"]=str(value)
            if str(key) == "section_name":
                client.tasks.add_project(TaskId, {'project': ShopsChecklist_ID,
                                                      'section': str(get_section_id(ShopsChecklist_ID, str(value)))})
            if str(key) == "assigned_to":
                updatequery["assignee"]=str(value)
            if str(key) == "due_date":
                updatequery["due_on"]=str(value)
            if str(key) == "description":
                updatequery["notes"]=str(value)
    else:
        print("Ошибка обновления таска")

    client.tasks.update(TaskId, updatequery)

def get_task(TaskId):

    m= client.tasks.find_by_id(TaskId)
    return m

ta = client.tasks.find_all({"workspace":"829874196257517","assignee":"mr.mcdi.576@gmail.com","completed_since":"now"})
for t in ta:
    print(t)