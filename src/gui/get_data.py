from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.app import services

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

def gettasks():
    return services.get_tasks()


