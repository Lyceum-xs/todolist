from tkinter import *
from tkinter import ttk
import tkinter as tk
from ..utils import clear_frame
from .. import get_data 

# Habitclockin content
#-------------------------------- begin -------------------------------
def Habitclockin(root, max_width, max_height):
    clear_frame(root)
    print('This is Habitclockin now')

    style = ttk.Style()
    style.configure('Hab.TButton', 
                   background='#FFFFFF',
                   foreground='#000000',
                   font = ('consolas', 10),
                   borderwidth=0,
                   padding=0,
                   relief='flat')
    style.configure('Hab.TLabel', font = ('consolas', 10))

    root.columnconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)

    # calendar frame
    #----------------------- begin -----------------------
    calendar_frame = ttk.Frame(root)
    calendar_frame.grid(row = 0, column = 0, sticky = 'ew')
    clockin_frame = ttk.Frame(root)
    clockin_frame.grid(row = 1, column = 0, sticky = 'nsew')

    clockin_frame.columnconfigure(0, weight = 1)

    nowtime = get_data.gettime()
    target_year = nowtime['year']
    target_month = nowtime['month']

    target_date = {'year' : nowtime['year'], 'month' : nowtime['month'], 'day' : nowtime['day']}

    def clear_clockin():
        for widget in clockin_frame.grid_slaves():
            row = widget.grid_info().get('row', -1)
            if row is not None:
                widget.destroy()

    def draw_clockin():
        clear_clockin()
        
        date_label = ttk.Label(clockin_frame, text = f'{target_date['year']}-{target_date['month']}-{target_date['day']}', style = 'Hab.TLabel')
        date_label.grid(row = 0, column = 0, sticky = 'w', padx = (10, 0))
        
        if target_date['year'] == nowtime['year'] and target_date['month'] == nowtime['month'] and target_date['day'] == nowtime['day']:
            null_label = ttk.Label(clockin_frame)
            null_label.grid(row = 2, column = 0, sticky = 'ew')

            clockin_content = tk.StringVar()
            clockin_content.set('Clockin content')

            clockin_bar = tk.Entry(clockin_frame, textvariable = clockin_content, width = 45, font = ('consolas', 12))
            clockin_bar.grid(row = 1, column = 0, pady = 15)

            def clo():
                value = clockin_content.get()
                print(f'{value} is clockined')

            clockin_button = ttk.Button(clockin_frame, text = 'clockin', style = 'Hab.TButton', command = clo)
            clockin_button.grid(row = 2, column = 1)
        
        elif (target_date['year'] < nowtime['year']) or (target_date['year'] == nowtime['year'] and target_date['month'] < nowtime['month']) or (target_date['year'] == nowtime['year'] and target_date['month'] == nowtime['month'] and target_date['day'] < nowtime['day']):
            content_label = ttk.Label(clockin_frame, text = 'You didn\'t clockin on this day', style = 'Hab.TLabel')
            content_label.grid(row = 1, column = 0, pady = 50)
        
        elif (target_date['year'] > nowtime['year']) or (target_date['year'] == nowtime['year'] and target_date['month'] > nowtime['month']) or (target_date['year'] == nowtime['year'] and target_date['month'] == nowtime['month'] and target_date['day'] > nowtime['day']):
            content_label = ttk.Label(clockin_frame, text = 'This day has not arrived', style = 'Hab.TLabel')
            content_label.grid(row = 1, column = 0, pady = 50)


    def clear_calendar():
        for widget in calendar_frame.grid_slaves():
            row = widget.grid_info().get('row', -1)
            if row is not None and row > 1:
                widget.destroy()

    def draw_calendar(calendar):
        r = 2
        for day, week in calendar.items():
            c = week % 7
            if week == 7:
                r += 1
            def game(target_day):
                print(f'{target_day} is now')
                nonlocal target_date
                target_date['year'] = target_year
                target_date['month'] = target_month
                target_date['day'] = target_day

                draw_clockin()
            day_button = ttk.Button(calendar_frame, text = day, style = 'Hab.TButton', width = 5, command = lambda d = day: game(d))
            day_button.grid(row = r, column = c, padx = 10, pady = 20)

    def update_calendar():
        clear_calendar()

        year_label.config(text = f'{target_year} year')
        month_label.config(text = f'{target_month} month')

        calendar = get_data.getcalendar(target_year, target_month)
        draw_calendar(calendar)

    def yl_game():
        nonlocal target_year
        target_year -= 1
        update_calendar()
    def yr_game():
        nonlocal target_year
        target_year += 1
        update_calendar()
    def ml_game():
        nonlocal target_month, target_year
        target_month -= 1
        if target_month < 1:
            target_year -= 1
            target_month = 12
        update_calendar()
    def mr_game():
        nonlocal target_month, target_year
        target_month += 1
        if target_month > 12:
            target_month = 1
            target_year += 1
        update_calendar()

    yl_button = ttk.Button(calendar_frame, text = '<', style = 'Hab.TButton',width = 3, command = yl_game)
    yr_button = ttk.Button(calendar_frame, text = '>', style = 'Hab.TButton',width = 3, command = yr_game)
    ml_button = ttk.Button(calendar_frame, text = '<', style = 'Hab.TButton',width = 3, command = ml_game)
    mr_button = ttk.Button(calendar_frame, text = '>', style = 'Hab.TButton',width = 3, command = mr_game)

    yl_button.grid(row = 0, column = 0)
    yr_button.grid(row = 0, column = 2)
    ml_button.grid(row = 0, column = 3)
    mr_button.grid(row = 0, column = 5)

    year_label = ttk.Label(calendar_frame, text = f'{target_year} year', style = 'Hab.TLabel')
    month_label = ttk.Label(calendar_frame, text = f'{target_month} month', style = 'Hab.TLabel')
    year_label.grid(row = 0, column = 1)
    month_label.grid(row = 0, column = 4)

    week_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for i, week in enumerate(week_labels):
        week_label = ttk.Label(calendar_frame, text = week, style = 'Hab.TLabel')
        week_label.grid(row = 1, column = i, padx = 30)

    calendar = get_data.getcalendar(target_year, target_month)
    draw_calendar(calendar)

    def back_to_today():
        nonlocal target_year, target_month, target_date
        target_year = nowtime['year']
        target_month = nowtime['month']

        target_date['year'] = nowtime['year']
        target_date['month'] = nowtime['month']
        target_date['day'] = nowtime['day']

        update_calendar()
        draw_clockin()

    back_to_today_button = ttk.Button(calendar_frame, text = 'back', style = 'Hab.TButton', command = back_to_today)
    back_to_today_button.grid(row = 0, column = 6)

    draw_clockin()
    #------------------------ End ------------------------


#--------------------------------- End --------------------------------