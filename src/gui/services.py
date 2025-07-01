from datetime import datetime
from ..app import services

def gettime():
    nowtime = datetime.now()
    return {'year' : nowtime.year, 'month' : nowtime.month, 'day' : nowtime.day, 'hour' : nowtime.hour, 'minute' : nowtime.minute}

def getcalendar(year, month):
    calendar = {}

    max_day = 0
    if month == 2:
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            max_day = 29
        else:
            max_day = 28
    elif month == 4 or month == 6 or month == 9 or month == 11:
        max_day = 30
    else:
        max_day = 31

    for day in range(1, max_day + 1):
        week = datetime(year, month, day).isoweekday()
        calendar.update({day : week})
    
    return calendar

def create_datetime(year, month, day):
    return datetime(year, month, day)

def gettasks():
    return services.TaskService.get_all_tasks()

def addtask(task):
    services.TaskService.create_task(task)
    print(f'add {task} successfully')

def deltask(task_id):
    services.TaskService.delete_task(task_id)
    print(f'delete {task_id} successfully')

def updatetask(task_id, up_dict):
    services.TaskService.update_task(task_id, up_dict)
    print(f'update {task_id} {up_dict} successfully')

def gettask(task_id):
    return services.TaskService.get_task(task_id)



