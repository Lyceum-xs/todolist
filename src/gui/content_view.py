import calendar
import collections
from logging import root
from re import A
from tkinter import *
from tkinter import ttk
import tkinter as tk
from turtle import back
import get_data

# clear all widgets in a frame
#-------------------------------- Begin -------------------------------
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
#--------------------------------- End --------------------------------


# home content
#-------------------------------- begin -------------------------------
def Home(root, max_width, max_height):
    clear_frame(root)   # initialize content frame
    print('This is home now')
    
    root.columnconfigure(0, weight=1)

    # Search Bar
    #-------------------------- begin ------------------------------
    search_frame = ttk.Frame(root)
    search_frame.grid(row=0, column=0, sticky='w', pady=(15,0), padx=40)

    target = tk.StringVar()
    target.set('Search Task')

    search_bar = tk.Entry(search_frame, textvariable = target, width = 45, font = ('consolas', 12))
    search_bar.grid(row = 0, column = 0)

    style = ttk.Style()
    style.configure('Home.TButton', 
                   background='#FFFFFF',
                   foreground='#000000',
                   font = ('consolas', 10),
                   borderwidth=0,
                   padding=0,
                   relief='flat')

    def search():
        value = target.get()
        print(f'Get entry: {value}')

    search_button = ttk.Button(search_frame, command = search, text = 'search', style = 'Home.TButton')
    search_button.grid(row = 0, column = 1, padx = (1, 0))
    #--------------------------- End --------------------------


    # Menu bar
    #-------------------------- begin ------------------------------
    style.configure('Meau.TFrame', background = '#FFFFFF')
    menu_bar = ttk.Frame(root, style = 'Menu.TFrame')
    menu_bar.grid(row = 1, column = 0, sticky = 'ew', pady=(10, 0))


        # Sort Bar
        #-------------------------- Begin -------------------------
    sort_basis = ['Due Date', 'Urgency', 'Importance']
    s = tk.StringVar()
    
    sort_bar = ttk.Combobox(menu_bar, width = 15, state = 'readonly', textvariable = s, values = sort_basis, font = ('consolas', 12))
    sort_bar.grid(row = 0, column = 0, padx = (5, 0))

    sort_bar.set('Sort Basis')

    def select(event):
        print(f'Get sort basis: {s.get()}')

    sort_bar.bind('<<ComboboxSelected>>', select)
        #--------------------------- End --------------------------


        # add none
    menu_bar.columnconfigure(1, weight=1)


        # Add Button
        #-------------------------- Begin -------------------------
    def add():
        print(f'task is adding...')

        window = tk.Toplevel(root)
        window.title('Add New Task')
        window.geometry(f'{max_width}x{int(max_height * 0.5)}+{max_width}+{int(max_height * 0.5)}')

        input_frame = ttk.Frame(window)
        input_frame.grid(row=0, column=0, columnspan=2, pady=40, sticky='nsew')

        ttk.Label(input_frame, text = 'Task Name:', font = ('consolas', 14)).grid(row = 0, column = 0, padx = (120, 0))

        taskname = tk.StringVar()
        input_name = tk.Entry(input_frame, textvariable = taskname, font = ('consolas', 14))
        input_name.grid(row = 0, column = 1, sticky = 'w')
        
        style.configure('Window.TLabel', font = ('consolas', 12))

        time_frame = ttk.Frame(window)
        time_frame.grid(row = 1, column = 0, columnspan = 2, padx = 80)

        for i in range(5):
            time_frame.columnconfigure(i, weight = 1, uniform = 'time_col')

        style.configure('Window.TLabel', width = 6, font = ('consolas', 12))

        labels = [
        ttk.Label(time_frame, text = 'Year', style = 'Window.TLabel'),
        ttk.Label(time_frame, text = 'Month', style = 'Window.TLabel'),
        ttk.Label(time_frame, text = 'Day', style = 'Window.TLabel'),
        ttk.Label(time_frame, text = 'Hour', style = 'Window.TLabel'),
        ttk.Label(time_frame, text = 'Minute', style = 'Window.TLabel')
        ]
    
        for i, label in enumerate(labels):
            label.grid(row=1, column=i, sticky='ew', padx = (20, 0))

        time = get_data.gettime()
        year = time['year']
        month = time['month']
        day = time['day']
        hour = time['hour']
        minute = time['minute']

        dl_year = tk.StringVar()
        dl_month = tk.StringVar()
        dl_day = tk.StringVar()
        dl_hour = tk.StringVar()
        dl_minute = tk.StringVar()

        spinboxes = [
        tk.Spinbox(time_frame, from_ = year, to=year + 100, textvariable = dl_year, width=5),
        tk.Spinbox(time_frame, from_ = 1, to = 12, textvariable = dl_month, width=5),
        tk.Spinbox(time_frame, from_ = 1, to = 31, textvariable = dl_day, width=5),
        tk.Spinbox(time_frame, from_ = 0, to = 23, textvariable = dl_hour, width=5),
        tk.Spinbox(time_frame, from_ = 0, to = 59, textvariable = dl_minute, width=5)
        ]
    
        for i, spinbox in enumerate(spinboxes):
            spinbox.grid(row=2, column=i, padx=(20, 0), pady=5, sticky='ew')


        def close():
            window.destroy()

        def cancel():
            print('Addition is canceled, no submission')
            close()

        def submit():
            print(f'Submit succeed:[taskname:{taskname.get()},submit time:{year}/{month}/{day} {hour}:{minute},due time:{dl_year.get()}/{dl_month.get()}/{dl_day.get()} {dl_hour.get()}:{dl_minute.get()}]')
            close()
        
        cancel_button = ttk.Button(window, command = cancel, text = 'cancel', style = 'Home.TButton')
        cancel_button.place(width = 80, height = 25, x = max_width - 180, y = int(max_height * 0.5 - 30))

        submit_button = ttk.Button(window, command = submit, text = 'submit', style = 'Home.TButton')
        submit_button.place(width = 80, height = 25, x = max_width - 90, y = int(max_height * 0.5 - 30))

    add_button = ttk.Button(menu_bar, command = add, text = '+ Add', width = 6, style = 'Home.TButton')
    add_button.grid(row = 0, column = 2, padx = (0, 5))
        #--------------------------- End --------------------------
    #--------------------------- End --------------------------

    #task list
    


#--------------------------------- End --------------------------------


# settings content
#-------------------------------- begin -------------------------------
def Settings(root, max_width, max_height):
    clear_frame(root)
    print('This is settings now')

    def toggle_simple_mode():
        # 这里后续可添加简洁模式切换逻辑
        pass

    switch_btn = tk.Button(
        root,
        text="切换模式",
        font=("consolas", 12),
        width=15,
        command=toggle_simple_mode
    )
    switch_btn.pack(pady=20)
#--------------------------------- End --------------------------------

# timer content
#-------------------------------- begin -------------------------------
def Timer(root, max_width, max_height):
    clear_frame(root)
    print('This is timer now')

    timer_frame = ttk.Frame(root)
    timer_frame.pack(fill=tk.BOTH, expand=True)

    # 状态变量
    hour_var = tk.StringVar(value='0')
    min_var = tk.StringVar(value='25')
    sec_var = tk.StringVar(value='0')
    running = tk.BooleanVar(value=False)
    paused = tk.BooleanVar(value=False)
    remaining_sec = [0]
    timer_id = [None]
    current_mode = tk.StringVar(value="work")
    work_content_var = tk.StringVar()

    # 模式与设置时间
    mode_settings = {
        "work": {"hour": 0, "min": 25, "sec": 0},
        "break": {"hour": 0, "min": 5, "sec": 0}
    }

    # ----------- 工作内容输入栏目始终在顶部 -----------
    work_content_frame = ttk.Frame(timer_frame)
    work_content_label = ttk.Label(work_content_frame, text="当前工作内容：", font=('consolas', 12, 'bold'))
    work_content_label.pack(side=tk.LEFT, padx=(5, 5))
    work_content_entry = ttk.Entry(work_content_frame, textvariable=work_content_var, font=('consolas', 12), width=30)
    work_content_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    work_content_frame.pack(side=tk.TOP, pady=(15, 5), fill=tk.X)

    # 状态栏
    mode_display = ttk.Label(timer_frame, text="工作模式", font=('consolas', 12), foreground="#007ACC")
    mode_display.pack(pady=5)
    
    def update_work_content_state():
        """根据模式更新工作内容输入栏状态"""
        if current_mode.get() == "work":
            work_content_entry.config(state='normal')
        else:
            work_content_entry.config(state='disabled')

    # 时间选择区
    time_container = ttk.Frame(timer_frame)
    time_container.pack(pady=20)
    
    center_frame = ttk.Frame(time_container)
    center_frame.pack()

    # 时间标签
    label_frame = ttk.Frame(center_frame)
    label_frame.pack()
    ttk.Label(label_frame, text='Hour', font=('consolas', 14)).pack(side=tk.LEFT, padx=20)
    ttk.Label(label_frame, text='Minute', font=('consolas', 14)).pack(side=tk.LEFT, padx=20)
    ttk.Label(label_frame, text='Second', font=('consolas', 14)).pack(side=tk.LEFT, padx=20)

    # 输入验证函数
    def validate_hour(value):
        if value == "": return True
        try:
            num = int(value)
            return 0 <= num <= 23
        except ValueError:
            return False

    def validate_minute(value):
        if value == "": return True
        try:
            num = int(value)
            return 0 <= num <= 59
        except ValueError:
            return False

    def validate_second(value):
        if value == "": return True
        try:
            num = int(value)
            return 0 <= num <= 59
        except ValueError:
            return False

    # 注册验证函数
    vcmd_hour = (root.register(validate_hour), '%P')
    vcmd_minute = (root.register(validate_minute), '%P')
    vcmd_second = (root.register(validate_second), '%P')

    # 时间输入框
    spinbox_frame = ttk.Frame(center_frame)
    spinbox_frame.pack(pady=10)
    
    hour_spin = tk.Spinbox(spinbox_frame, from_=0, to=23, width=4, font=('consolas', 18),
                          textvariable=hour_var, validate="key", validatecommand=vcmd_hour)
    hour_spin.pack(side=tk.LEFT, padx=20)
    
    min_spin = tk.Spinbox(spinbox_frame, from_=0, to=59, width=4, font=('consolas', 18),
                          textvariable=min_var, validate="key", validatecommand=vcmd_minute)
    min_spin.pack(side=tk.LEFT, padx=20)
    
    sec_spin = tk.Spinbox(spinbox_frame, from_=0, to=59, width=4, font=('consolas', 18),
                          textvariable=sec_var, validate="key", validatecommand=vcmd_second)
    sec_spin.pack(side=tk.LEFT, padx=20)

    def format_time(secs):
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    timer_label = ttk.Label(timer_frame, text="00:25:00", font=('consolas', 36))
    timer_label.pack(pady=20)

    def update_display(secs=None):
        try:
            if secs is not None:
                timer_label.config(text=format_time(secs))
            else:
                h = int(hour_var.get() or 0)
                m = int(min_var.get() or 0)
                s = int(sec_var.get() or 0)
                total = h * 3600 + m * 60 + s
                timer_label.config(text=format_time(total))
            
            if running.get():
                timer_label.config(foreground="red")
            else:
                timer_label.config(foreground="black")
        except ValueError:
            pass  # 忽略无效输入

    # 绑定变量变化事件
    hour_var.trace_add('write', lambda *args: update_display())
    min_var.trace_add('write', lambda *args: update_display())
    sec_var.trace_add('write', lambda *args: update_display())

    def save_current_settings():
        try:
            current = current_mode.get()
            mode_settings[current] = {
                "hour": int(hour_var.get() or 0),
                "min": int(min_var.get() or 0),
                "sec": int(sec_var.get() or 0)
            }
        except ValueError:
            pass

    def load_mode_settings(mode):
        settings = mode_settings[mode]
        hour_var.set(str(settings["hour"]))
        min_var.set(str(settings["min"]))
        sec_var.set(str(settings["sec"]))
        update_display()

    def set_work():
        """切换到工作模式"""
        if running.get():
            mode_display.config(text="计时中，无法切换模式", foreground="red")
            return
        current_mode.set("work")
        load_mode_settings("work")
        mode_display.config(text="工作模式", foreground="#007ACC")
        update_work_content_state()
        work_content_entry.focus()

    def set_break():
        """切换到休息模式"""
        if running.get():
            mode_display.config(text="计时中，无法切换模式", foreground="red")
            return
        current_mode.set("break")
        load_mode_settings("break")
        mode_display.config(text="休息模式", foreground="#E64A19")
        update_work_content_state()

    def start_timer():
        if running.get():
            return
        
        try:
            h = int(hour_var.get() or 0)
            m = int(min_var.get() or 0)
            s = int(sec_var.get() or 0)
            total = h * 3600 + m * 60 + s
            
            if total == 0:
                mode_display.config(text="请设置时间", foreground="red")
                return
                
            save_current_settings()
            remaining_sec[0] = total
            running.set(True)
            paused.set(False)
            
            hour_spin.config(state='disabled')
            min_spin.config(state='disabled')
            sec_spin.config(state='disabled')
            
            update_display(remaining_sec[0])
            countdown()
            
        except ValueError:
            mode_display.config(text="请输入有效时间", foreground="red")

    def pause_timer():
        if running.get():
            if not paused.get():
                paused.set(True)
                if timer_id[0]:
                    root.after_cancel(timer_id[0])
                mode_display.config(text="已暂停", foreground="orange")
            else:
                paused.set(False)
                countdown()
                current = current_mode.get()
                if current == "work":
                    mode_display.config(text="工作模式", foreground="#007ACC")
                else:
                    mode_display.config(text="休息模式", foreground="#E64A19")

    def reset_timer():
        running.set(False)
        paused.set(False)
        
        if timer_id[0]:
            root.after_cancel(timer_id[0])
            
        hour_spin.config(state='normal')
        min_spin.config(state='normal')
        sec_spin.config(state='normal')
        
        current = current_mode.get()
        load_mode_settings(current)
        
        if current == "work":
            mode_display.config(text="工作模式", foreground="#007ACC")
        else:
            mode_display.config(text="休息模式", foreground="#E64A19")
        
        update_work_content_state()

    def countdown():
        if not running.get() or paused.get():
            return
            
        if remaining_sec[0] <= 0:
            timer_label.config(text="Time's up!", foreground="green")
            running.set(False)
            hour_spin.config(state='normal')
            min_spin.config(state='normal')
            sec_spin.config(state='normal')
            mode_display.config(text="时间到！", foreground="green")
            return
            
        remaining_sec[0] -= 1
        update_display(remaining_sec[0])
        timer_id[0] = root.after(1000, countdown)

    # 按钮布局
    btn_frame1 = ttk.Frame(timer_frame)
    btn_frame1.pack(fill=tk.X, padx=20, pady=10)
    
    ttk.Button(btn_frame1, text='工作', command=set_work).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
    ttk.Button(btn_frame1, text='休息', command=set_break).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,5))
    ttk.Button(btn_frame1, text='开始', command=start_timer).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))

    btn_frame2 = ttk.Frame(timer_frame)
    btn_frame2.pack(fill=tk.X, padx=20, pady=10)
    
    ttk.Button(btn_frame2, text='暂停/继续', command=pause_timer).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
    ttk.Button(btn_frame2, text='重置', command=reset_timer).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))

    # 初始化
    update_work_content_state()
    update_display()
#--------------------------------- End --------------------------------


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
            clockin_bar.grid(row = 1, column = 0, pady = 45)

            def clo():
                value = clockin_content.get()
                print(f'{value} is clockined')

            clockin_button = ttk.Button(clockin_frame, text = 'clockin', style = 'Hab.TButton', command = clo)
            clockin_button.grid(row = 2, column = 1)
        
        elif target_date['year'] < nowtime['year'] or target_date['month'] < nowtime['month'] or target_date['day'] < nowtime['day']:
            content_label = ttk.Label(clockin_frame, text = 'You didn\'t clockin on this day', style = 'Hab.TLabel')
            content_label.grid(row = 1, column = 0, pady = 50)
        
        else:
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


# choose content
#-------------------------------- begin -------------------------------
def Choose_content(name, root, max_width, max_height):
    if name == 'Home':
        Home(root, max_width, max_height)
    elif name == 'Settings':
        Settings(root, max_width, max_height)
    elif name == 'Timer':
        Timer(root, max_width, max_height)
    elif name == 'Habitclockin':
        Habitclockin(root, max_width, max_height)
#--------------------------------- End --------------------------------


# Content Bar
#-------------------------------- begin -------------------------------
def ContentBar(root, max_width, max_height):
    style = ttk.Style()

    style.configure('Con.TFrame', background = '#C0C0C0')

    content_frame = ttk.Frame(root, style = 'Con.TFrame')
    x_place = int(max_width * 0.3)
    y_place = 20
    w = int(max_width - x_place)
    h = int(max_height - y_place)

    content_frame.place(x = x_place, y = y_place, width = w, height = h)

    return content_frame
#--------------------------------- End --------------------------------
