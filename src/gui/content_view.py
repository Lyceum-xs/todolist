from tkinter import *
from tkinter import ttk
import tkinter as tk
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
    

    # Search Bar
    #-------------------------- begin ------------------------------
    target = tk.StringVar()
    target.set('Search Task')

    search_bar = tk.Entry(root, textvariable = target, font = ('consolas', 12))
    search_bar.place(width = 400, height = 30, x = 10, y = 10)

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

    search_button = ttk.Button(root, command = search, text = 'search', style = 'Home.TButton')
    search_button.place(width = 60, height = 30, x = 411, y = 10)

    style.configure('Meau.TFrame', background = '#FFFFFF')
    menu_bar = ttk.Frame(root, style = 'Menu.TFrame')
    menu_bar.place(x = 0, y = 50, width = max_width, height = 25)
    #--------------------------- End --------------------------


    # Sort Bar
    #-------------------------- Begin -------------------------
    sort_basis = ['Submission Date', 'Due Date', 'Urgency']
    s = tk.StringVar()
    
    sort_bar = ttk.Combobox(menu_bar, width = 15, state = 'readonly', textvariable = s, values = sort_basis, font = ('consolas', 12))
    sort_bar.grid(row = 0, column = 0)

    sort_bar.set('Sort Basis')

    def select(event):
        print(f'Get sort basis: {s.get()}')

    sort_bar.bind('<<ComboboxSelected>>', select)
    #--------------------------- End --------------------------


    # Add Button
    #-------------------------- Begin -------------------------
    def add():
        print(f'task is adding...')

        window = tk.Toplevel(root)
        window.title('Add New Task')
        window.geometry(f'{max_width}x{int(max_height * 0.5)}+{max_width}+{int(max_height * 0.5)}')

        taskname = tk.StringVar()

        ttk.Label(window, text = 'Task Name:', font = ('consolas', 14)).place(x = int(max_width * 0.25 - 80), y = int(max_height * 0.10),
                                                                             width = 160, height = 35)
        input_name = tk.Entry(window, textvariable = taskname, font = ('consolas', 14))
        input_name.place(x = int(max_width * 0.25 + 40), y = int(max_height * 0.10), width = int(max_width * 0.5), height = 35)

        style.configure('Window.TLabel', font = ('consolas', 12))

        year_label = ttk.Label(window, text = 'Year', style = 'Window.TLabel')
        year_label.place(width = 60, height = 25, x = 60, y = int(max_height * 0.10 + 35 + 25))

        month_label = ttk.Label(window, text = 'Month', style = 'Window.TLabel')
        month_label.place(width = 60, height = 25, x = 160, y = int(max_height * 0.10 + 35 + 25))

        day_label = ttk.Label(window, text = 'Day', style = 'Window.TLabel')
        day_label.place(width = 60, height = 25, x = 260, y = int(max_height * 0.10 + 35 + 25))

        hour_label = ttk.Label(window, text = 'Hour', style = 'Window.TLabel')
        hour_label.place(width = 60, height = 25, x = 360, y = int(max_height * 0.10 + 35 + 25))

        mintue_label = ttk.Label(window, text = 'Mintue', style = 'Window.TLabel')
        mintue_label.place(width = 60, height = 25, x = 460, y = int(max_height * 0.10 + 35 + 25))

        time = get_data.gettime()
        year = time['year']
        month = time['month']
        day = time['day']
        hour = time['hour']
        mintue = time['mintue']

        dl_year = tk.StringVar()
        dl_month = tk.StringVar()
        dl_day = tk.StringVar()
        dl_hour = tk.StringVar()
        dl_mintue = tk.StringVar()

        year_spinbox = tk.Spinbox(window, from_ = year, to = 3000, textvariable = dl_year)
        year_spinbox.place(width = 60, height = 40, x = 60, y = int(max_height * 0.10 + 35 + 55))

        month_spinbox = tk.Spinbox(window, from_ = 1, to = 12, textvariable = dl_month)
        month_spinbox.place(width = 60, height = 40, x = 160, y = int(max_height * 0.10 + 35 + 55))

        day_spinbox = tk.Spinbox(window, from_ = 1, to = 31, textvariable = dl_day)
        day_spinbox.place(width = 60, height = 40, x = 260, y = int(max_height * 0.10 + 35 + 55))

        hour_spinbox = tk.Spinbox(window, from_ = 0, to = 23, textvariable = dl_hour)
        hour_spinbox.place(width = 60, height = 40, x = 360, y = int(max_height * 0.10 + 35 + 55))

        mintue_spinbox = tk.Spinbox(window, from_ = 0, to = 59, textvariable = dl_mintue)
        mintue_spinbox.place(width = 60, height = 40, x = 460, y = int(max_height * 0.10 + 35 + 55))


        def close():
            window.destroy()

        def cancel():
            print('Addition is canceled, no submission')
            close()

        def submit():
            print(f'Submit succeed:[taskname:{taskname.get()},submit time:{year}/{month}/{day}/{hour}/{mintue},due time:{dl_year.get()}/{dl_month.get()}/{dl_day.get()}/{dl_hour.get()}/{dl_mintue.get()}]')
            close()
        
        cancel_button = ttk.Button(window, command = cancel, text = 'cancel', style = 'Home.TButton')
        cancel_button.place(width = 80, height = 25, x = max_width - 180, y = int(max_height * 0.5 - 30))

        submit_button = ttk.Button(window, command = submit, text = 'submit', style = 'Home.TButton')
        submit_button.place(width = 80, height = 25, x = max_width - 90, y = int(max_height * 0.5 - 30))

    add_button = ttk.Button(menu_bar, command = add, text = '+ Add', style = 'Home.TButton')
    add_button.place(x = max_width - 50, y = 0, width = 50, height = 25)
    #--------------------------- End --------------------------
#--------------------------------- End --------------------------------


# settings content
#-------------------------------- begin -------------------------------
def Settings(root, max_width, max_height):
    clear_frame(root)
    print('This is settings now')
#--------------------------------- End --------------------------------


# timer content
#-------------------------------- begin -------------------------------
def Timer(root, max_width, max_height):
    clear_frame(root)
    print('This is timer now')

    style = ttk.Style()
    style.configure('Timer.TLabel', font=('consolas', 28))
    style.configure('Timer.TButton', font=('consolas', 12), padding=6)
    style.configure('Timer.TFrame', background='#f5f5f5')

    timer_frame = ttk.Frame(root, style='Timer.TFrame')
    timer_frame.place(relx=0.5, rely=0.5, anchor='center', width=350, height=300)

    # 状态变量
    hour_var = tk.StringVar(value='0')
    min_var = tk.StringVar(value='25')
    sec_var = tk.StringVar(value='0')
    running = tk.BooleanVar(value=False)
    paused = tk.BooleanVar(value=False)
    remaining_sec = [0]  # 用列表包裹以便内部修改

    # 时间选择区
    tk.Label(timer_frame, text='Hour', font=('consolas', 12), bg='#f5f5f5').place(x=20, y=20)
    hour_spin = tk.Spinbox(timer_frame, from_=0, to=23, width=4, textvariable=hour_var, font=('consolas', 14), state='normal')
    hour_spin.place(x=20, y=50)

    tk.Label(timer_frame, text='Minute', font=('consolas', 12), bg='#f5f5f5').place(x=110, y=20)
    min_spin = tk.Spinbox(timer_frame, from_=0, to=59, width=4, textvariable=min_var, font=('consolas', 14), state='normal')
    min_spin.place(x=110, y=50)

    tk.Label(timer_frame, text='Second', font=('consolas', 12), bg='#f5f5f5').place(x=200, y=20)
    sec_spin = tk.Spinbox(timer_frame, from_=0, to=59, width=4, textvariable=sec_var, font=('consolas', 14), state='normal')
    sec_spin.place(x=200, y=50)

    # 时间显示
    def format_time(h, m, s):
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

    timer_label = ttk.Label(timer_frame, text=format_time(hour_var.get(), min_var.get(), sec_var.get()), style='Timer.TLabel')
    timer_label.place(x=60, y=110, width=220, height=50)

    # 更新显示
    def update_display():
        timer_label.config(text=format_time(hour_var.get(), min_var.get(), sec_var.get()))

    # 切换工作/休息
    def set_work():
        hour_var.set('0')
        min_var.set('25')
        sec_var.set('0')
        update_display()

    def set_break():
        hour_var.set('0')
        min_var.set('5')
        sec_var.set('0')
        update_display()

    # 倒计时逻辑
    timer_id = [None]  # 用于取消 after

    def countdown():
        if not running.get() or paused.get():
            return
        if remaining_sec[0] <= 0:
            timer_label.config(text="Time's up!")
            running.set(False)
            return
        h = remaining_sec[0] // 3600
        m = (remaining_sec[0] % 3600) // 60
        s = remaining_sec[0] % 60
        timer_label.config(text=format_time(h, m, s))
        remaining_sec[0] -= 1
        timer_id[0] = root.after(1000, countdown)

    def start_timer():
        if running.get():
            return
        total_sec = int(hour_var.get()) * 3600 + int(min_var.get()) * 60 + int(sec_var.get())
        if total_sec == 0:
            return
        remaining_sec[0] = total_sec
        running.set(True)
        paused.set(False)
        hour_spin.config(state='disabled')
        min_spin.config(state='disabled')
        sec_spin.config(state='disabled')
        countdown()

    def pause_timer():
        if running.get() and not paused.get():
            paused.set(True)
            if timer_id[0]:
                root.after_cancel(timer_id[0])
        elif running.get() and paused.get():
            paused.set(False)
            countdown()

    def reset_timer():
        running.set(False)
        paused.set(False)
        if timer_id[0]:
            root.after_cancel(timer_id[0])
        hour_spin.config(state='normal')
        min_spin.config(state='normal')
        sec_spin.config(state='normal')
        update_display()
        timer_label.config(text=format_time(hour_var.get(), min_var.get(), sec_var.get()))

    # 按钮区
    ttk.Button(timer_frame, text='工作', style='Timer.TButton', command=set_work).place(x=30, y=180, width=70)
    ttk.Button(timer_frame, text='休息', style='Timer.TButton', command=set_break).place(x=110, y=180, width=70)
    ttk.Button(timer_frame, text='开始', style='Timer.TButton', command=start_timer).place(x=190, y=180, width=70)
    ttk.Button(timer_frame, text='暂停/继续', style='Timer.TButton', command=pause_timer).place(x=30, y=230, width=110)
    ttk.Button(timer_frame, text='重置', style='Timer.TButton', command=reset_timer).place(x=160, y=230, width=100)

    # 监听时间变化自动更新显示
    hour_var.trace_add('write', lambda *args: update_display())
    min_var.trace_add('write', lambda *args: update_display())
    sec_var.trace_add('write', lambda *args: update_display())
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