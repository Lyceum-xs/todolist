from tkinter import *
from tkinter import ttk
import tkinter as tk
from ..utils import clear_frame
from .. import services 

# Habitclockin content
#-------------------------------- begin -------------------------------
def Calendar(root, max_width, max_height):
    clear_frame(root)
    print('This is Calendar now')

    root.rowconfigure(5, weight = 0)

    style = ttk.Style()
    style.configure('Cal.TButton', 
                   background='#FFFFFF',
                   foreground='#000000',
                   font = ('consolas', 10),
                   borderwidth=0,
                   padding=0,
                   relief='flat')
    style.configure('Cal.TLabel', font = ('consolas', 10))

    root.columnconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)

    # calendar frame
    #----------------------- begin -----------------------
    calendar_frame = ttk.Frame(root)
    calendar_frame.grid(row = 0, column = 0, sticky = 'ew')
    clockin_frame = ttk.Frame(root)
    clockin_frame.grid(row = 1, column = 0, sticky = 'nsew')

    clockin_frame.columnconfigure(0, weight = 1)
    clockin_frame.rowconfigure(1, weight = 1)

    nowtime = services.TimeServices.gettime()
    target_year = nowtime['year']
    target_month = nowtime['month']

    target_date = {'year' : nowtime['year'], 'month' : nowtime['month'], 'day' : nowtime['day']}

    def clear_cavans():
        clear_frame(clockin_frame)

    def draw_cavans():
        date_label = ttk.Label(clockin_frame, text = f'{target_date['year']}-{target_date['month']}-{target_date['day']}', style = 'Cal.TLabel')
        date_label.grid(row = 0, column = 0, sticky = 'w', padx = (10, 0))
        
        canvas = Canvas(clockin_frame, borderwidth = 0, highlightthickness = 0)
        vsb = ttk.Scrollbar(clockin_frame, orient="vertical", command=canvas.yview)
        hsb = ttk.Scrollbar(clockin_frame, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")
        hsb.grid(row=2, column=0, sticky="ew")

        frame = ttk.Frame(canvas)
        canvas_frame = canvas.create_window((0, 0), window = frame, anchor="nw")

        def configure_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_frame, width = event.width)
    
        frame.bind("<Configure>", configure_scrollregion)
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_frame, width=event.width))

        frame.columnconfigure(0, weight = 1)
        frame.columnconfigure(1, weight = 1)

        ttk.Label(frame, text = 'Overdue tasks', font = ('consolas', 10)).grid(row = 0, column = 0, sticky = 'ew')
        ttk.Label(frame, text = 'Clockin habits', font = ('consolas', 10)).grid(row = 0, column = 1, sticky = 'ew')


        def gettasks(tasks, error):
            if error:
                print(error)
                return

            r = 1
            for task in tasks:
                due_date = services.TimeServices.turn_datetime_strp(task['due_date'])

                if due_date.year == target_date['year'] and due_date.month == target_date['month'] and due_date.day == target_date['day']:
                    ttk.Label(frame, text = task['name'], font = ('consolas', 10)).grid(row = r, column = 0, sticky = 'w')

                    r += 1

        tasks = services.TaskServices.gettasks('id', gettasks)


        def get_habits(habits, error):
            if error:
                print(error)
                return
 
            r = 1
            for habit in habits:
                logs = habit['logs']
                for log in logs:
                    clockin_date = services.TimeServices.turn_datetime_strp(log['date'])
                    if clockin_date.year == target_date['year'] and clockin_date.month == target_date['month'] and clockin_date.day == target_date['day']:
                        ttk.Label(frame, text = habit['name'], font = ('consolas', 10)).grid(row = r, column = 1, sticky = 'w')
            
                        r += 1

        habits = services.HabitServices.get_habits(get_habits)

    def update_cavans():
        clear_cavans()
        draw_cavans()

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

                draw_cavans()
            day_button = ttk.Button(calendar_frame, text = day, style = 'Cal.TButton', width = 5, command = lambda d = day: game(d))
            day_button.grid(row = r, column = c, padx = 10, pady = 20)

    def update_calendar():
        clear_calendar()

        year_label.config(text = f'{target_year} year')
        month_label.config(text = f'{target_month} month')

        calendar = services.TimeServices.getcalendar(target_year, target_month)
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

    yl_button = ttk.Button(calendar_frame, text = '<', style = 'Cal.TButton',width = 3, command = yl_game)
    yr_button = ttk.Button(calendar_frame, text = '>', style = 'Cal.TButton',width = 3, command = yr_game)
    ml_button = ttk.Button(calendar_frame, text = '<', style = 'Cal.TButton',width = 3, command = ml_game)
    mr_button = ttk.Button(calendar_frame, text = '>', style = 'Cal.TButton',width = 3, command = mr_game)

    yl_button.grid(row = 0, column = 0)
    yr_button.grid(row = 0, column = 2)
    ml_button.grid(row = 0, column = 3)
    mr_button.grid(row = 0, column = 5)

    year_label = ttk.Label(calendar_frame, text = f'{target_year} year', style = 'Cal.TLabel')
    month_label = ttk.Label(calendar_frame, text = f'{target_month} month', style = 'Cal.TLabel')
    year_label.grid(row = 0, column = 1)
    month_label.grid(row = 0, column = 4)

    week_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for i, week in enumerate(week_labels):
        week_label = ttk.Label(calendar_frame, text = week, style = 'Cal.TLabel')
        week_label.grid(row = 1, column = i, padx = 30)

    calendar = services.TimeServices.getcalendar(target_year, target_month)
    draw_calendar(calendar)

    def back_to_today():
        nonlocal target_year, target_month, target_date
        target_year = nowtime['year']
        target_month = nowtime['month']

        target_date['year'] = nowtime['year']
        target_date['month'] = nowtime['month']
        target_date['day'] = nowtime['day']

        update_calendar()
        update_cavans()

    back_to_today_button = ttk.Button(calendar_frame, text = 'back', style = 'Cal.TButton', command = back_to_today)
    back_to_today_button.grid(row = 0, column = 6)

    update_cavans()
    #------------------------ End ------------------------


#--------------------------------- End --------------------------------