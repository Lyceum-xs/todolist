from datetime import datetime

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


