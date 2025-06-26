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

    timer_frame = tk.Frame(root, bg='#f5f5f5')
    timer_frame.pack(fill=tk.BOTH, expand=True)

    # 状态变量
    hour_var = tk.StringVar(value='0')
    min_var = tk.StringVar(value='25')
    sec_var = tk.StringVar(value='0')
    running = tk.BooleanVar(value=False)
    paused = tk.BooleanVar(value=False)
    remaining_sec = [0]
    timer_id = [None]
    error_occurred = [False]
    current_mode = tk.StringVar(value="work")

    # 模式与设置时间（默认值，用户调整后覆盖）
    mode_settings = {
        "work": {"hour": 0, "min": 25, "sec": 0},
        "break": {"hour": 0, "min": 5, "sec": 0}
    }

    mode_display = tk.Label(timer_frame, text="工作模式", font=('consolas', 12), bg='#f5f5f5', fg="#007ACC")
    mode_display.pack(pady=5)

    # 时间选择区
    time_frame = tk.Frame(timer_frame, bg='#f5f5f5')
    time_frame.pack(pady=50)
    center_frame = tk.Frame(time_frame, bg='#f5f5f5')
    center_frame.pack()

    def validate_number(new_value, min_val, max_val, var, error_label):
        if not new_value: return True
        if not new_value.isdigit():
            error_label.config(text="请输入数字", fg="red")
            error_occurred[0] = True
            return False
        num = int(new_value)
        if num < min_val or num > max_val:
            error_label.config(text=f"请输入{min_val}-{max_val}之间的数字", fg="red")
            error_occurred[0] = True
            var.set(min_val if num < min_val else max_val)
            return False
        error_label.config(text="", fg="black")
        error_occurred[0] = False
        return True

    error_labels = []
    for i in range(3):
        error_label = tk.Label(center_frame, text="", bg='#f5f5f5', font=('consolas', 10))
        error_label.grid(row=2, column=i, pady=2)
        error_labels.append(error_label)

    def validate_hour(new_value): return validate_number(new_value, 0, 23, hour_var, error_labels[0])
    def validate_minute(new_value): return validate_number(new_value, 0, 59, min_var, error_labels[1])
    def validate_second(new_value): return validate_number(new_value, 0, 59, sec_var, error_labels[2])

    tk.Label(center_frame, text='Hour', font=('consolas', 14), bg='#f5f5f5').grid(row=0, column=0, pady=(0, 10))
    hour_spin = tk.Spinbox(center_frame, from_=0, to=23, width=4, font=('consolas', 18),
                          textvariable=hour_var, validate="key",
                          validatecommand=(root.register(validate_hour), '%P'))
    hour_spin.grid(row=1, column=0, padx=5)
    tk.Label(center_frame, text='Minute', font=('consolas', 14), bg='#f5f5f5').grid(row=0, column=1, pady=(0, 10))
    min_spin = tk.Spinbox(center_frame, from_=0, to=59, width=4, font=('consolas', 18),
                          textvariable=min_var, validate="key",
                          validatecommand=(root.register(validate_minute), '%P'))
    min_spin.grid(row=1, column=1, padx=5)
    tk.Label(center_frame, text='Second', font=('consolas', 14), bg='#f5f5f5').grid(row=0, column=2, pady=(0, 10))
    sec_spin = tk.Spinbox(center_frame, from_=0, to=59, width=4, font=('consolas', 18),
                          textvariable=sec_var, validate="key",
                          validatecommand=(root.register(validate_second), '%P'))
    sec_spin.grid(row=1, column=2, padx=5)

    def format_time(secs):
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    timer_label = tk.Label(timer_frame, text="00:25:00", font=('consolas', 36), bg='#f5f5f5', fg="black")
    timer_label.pack(pady=20)

    def update_display(secs=None):
        if error_occurred[0]: return
        if secs is not None:
            timer_label.config(text=format_time(secs))
        else:
            total = int(hour_var.get())*3600 + int(min_var.get())*60 + int(sec_var.get())
            timer_label.config(text=format_time(total))
        if running.get():
            timer_label.config(fg="red")
        else:
            timer_label.config(fg="black")

    hour_var.trace_add('write', lambda *args: update_display())
    min_var.trace_add('write', lambda *args: update_display())
    sec_var.trace_add('write', lambda *args: update_display())

    def save_current_settings():
        """保存当前模式的时间设置"""
        current = current_mode.get()
        mode_settings[current] = {
            "hour": int(hour_var.get()),
            "min": int(min_var.get()),
            "sec": int(sec_var.get())
        }

    def load_mode_settings(mode):
        """加载模式设置时间"""
        settings = mode_settings[mode]
        hour_var.set(settings["hour"])
        min_var.set(settings["min"])
        sec_var.set(settings["sec"])
        update_display()

    btn_frame1 = tk.Frame(timer_frame, bg='#f5f5f5')
    btn_frame1.pack(pady=10)

    def set_work():
        """切换到工作模式并加载设置"""
        current_mode.set("work")
        load_mode_settings("work")
        mode_display.config(text="工作模式", fg="#007ACC")

    def set_break():
        """切换到休息模式并加载设置"""
        current_mode.set("break")
        load_mode_settings("break")
        mode_display.config(text="休息模式", fg="#E64A19")

    def countdown():
        if not running.get() or paused.get(): return
        if remaining_sec[0] <= 0:
            timer_label.config(text="Time's up!", fg="green")
            running.set(False)
            hour_spin.config(state='normal')
            min_spin.config(state='normal')
            sec_spin.config(state='normal')
            return
        remaining_sec[0] -= 1
        update_display(remaining_sec[0])
        timer_id[0] = root.after(1000, countdown)

    def start_timer():
        """开始计时并保存当前模式设置"""
        if running.get(): return
        validate_hour(hour_var.get())
        validate_minute(min_var.get())
        validate_second(sec_var.get())
        if error_occurred[0]: return
        total = int(hour_var.get())*3600 + int(min_var.get())*60 + int(sec_var.get())
        if total == 0: return
        save_current_settings()  # 关键：开始计时时保存当前设置
        remaining_sec[0] = total
        running.set(True)
        paused.set(False)
        hour_spin.config(state='disabled')
        min_spin.config(state='disabled')
        sec_spin.config(state='disabled')
        update_display(remaining_sec[0])
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
        """重置为当前模式的保存设置"""
        running.set(False)
        paused.set(False)
        if timer_id[0]:
            root.after_cancel(timer_id[0])
        hour_spin.config(state='normal')
        min_spin.config(state='normal')
        sec_spin.config(state='normal')
        current = current_mode.get()
        load_mode_settings(current)
        timer_label.config(fg="black")

    ttk.Button(btn_frame1, text='工作', command=set_work).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame1, text='休息', command=set_break).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame1, text='开始', command=start_timer).pack(side=tk.LEFT, padx=5)

    btn_frame2 = tk.Frame(timer_frame, bg='#f5f5f5')
    btn_frame2.pack(pady=10)
    ttk.Button(btn_frame2, text='暂停/继续', command=pause_timer).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame2, text='重置', command=reset_timer).pack(side=tk.LEFT, padx=5)
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