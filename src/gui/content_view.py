from re import A
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
    sort_basis = ['Submission Date', 'Due Date', 'Urgency']
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
    work_content_var = tk.StringVar()  # 工作内容变量

    # 模式与设置时间
    mode_settings = {
        "work": {"hour": 0, "min": 25, "sec": 0},
        "break": {"hour": 0, "min": 5, "sec": 0}
    }

    # ----------- 工作内容输入栏目始终在顶部 -----------
    work_content_frame = tk.Frame(timer_frame, bg='#f5f5f5')
    work_content_label = tk.Label(work_content_frame, text="当前工作内容：", font=('consolas', 12, 'bold'), bg='#f5f5f5')
    work_content_label.pack(side=tk.LEFT, padx=(5, 5))
    work_content_entry = tk.Entry(work_content_frame, textvariable=work_content_var, font=('consolas', 12), width=30)
    work_content_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    work_content_frame.pack(side=tk.TOP, anchor='n', pady=(15, 5), fill=tk.X)  # 固定在顶部

    # 状态栏
    mode_display = tk.Label(timer_frame, text="工作模式", font=('consolas', 12), bg='#f5f5f5', fg="#007ACC")
    mode_display.pack(pady=5)

    def update_work_content_state():
        """根据模式更新工作内容输入栏状态（不改变布局顺序）"""
        if current_mode.get() == "work":
            work_content_entry.config(state='normal')
            # 始终保持在顶部，不 pack_forget
        else:
            work_content_entry.config(state='disabled')
            # 休息模式下禁用输入，但不隐藏，且可选：清空内容
            # work_content_var.set('')  # 如需切换时清空内容可取消注释

    # 时间选择区
    time_frame = tk.Frame(timer_frame, bg='#f5f5f5')
    time_frame.pack(pady=50, anchor='center')
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
    timer_label.pack(pady=20, anchor='center')  # 居中显示

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
        current = current_mode.get()
        mode_settings[current] = {
            "hour": int(hour_var.get()),
            "min": int(min_var.get()),
            "sec": int(sec_var.get())
        }

    def load_mode_settings(mode):
        settings = mode_settings[mode]
        hour_var.set(settings["hour"])
        min_var.set(settings["min"])
        sec_var.set(settings["sec"])
        update_display()

    btn_frame1 = tk.Frame(timer_frame, bg='#f5f5f5')
    btn_frame1.pack(pady=10, anchor='center')  # 按钮居中

    def set_work():
        """切换到工作模式并显示输入栏"""
        if running.get():
            mode_display.config(text="计时中，无法切换模式", fg="red")
            # 不再恢复原提示，让提示一直显示
            return
        current_mode.set("work")
        load_mode_settings("work")
        mode_display.config(text="工作模式", fg="#007ACC")
        update_work_content_state()
        work_content_entry.focus()

    def set_break():
        """切换到休息模式并禁用输入栏"""
        if running.get():
            mode_display.config(text="计时中，无法切换模式", fg="red")
            # 不再恢复原提示，让提示一直显示
            return
        current_mode.set("break")
        load_mode_settings("break")
        mode_display.config(text="休息模式", fg="#E64A19")
        update_work_content_state()

    def start_timer():
        if running.get(): return
        validate_hour(hour_var.get())
        validate_minute(min_var.get())
        validate_second(sec_var.get())
        if error_occurred[0]: return
        total = int(hour_var.get())*3600 + int(min_var.get())*60 + int(sec_var.get())
        if total == 0: return
        save_current_settings()
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
        # 重置时恢复模式提示
        if current == "work":
            mode_display.config(text="工作模式", fg="#007ACC")
            update_work_content_state()
        else:
            mode_display.config(text="休息模式", fg="#E64A19")
            update_work_content_state()

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

    ttk.Button(btn_frame1, text='工作', command=set_work).pack(side=tk.LEFT, padx=10)
    ttk.Button(btn_frame1, text='休息', command=set_break).pack(side=tk.LEFT, padx=10)
    ttk.Button(btn_frame1, text='开始', command=start_timer).pack(side=tk.LEFT, padx=10)

    btn_frame2 = tk.Frame(timer_frame, bg='#f5f5f5')
    btn_frame2.pack(pady=10, anchor='center')
    ttk.Button(btn_frame2, text='暂停/继续', command=pause_timer).pack(side=tk.LEFT, padx=10)
    ttk.Button(btn_frame2, text='重置', command=reset_timer).pack(side=tk.LEFT, padx=10)

    # 初始化显示状态
    update_work_content_state()
#--------------------------------- End --------------------------------


# Habbitclockin content
#-------------------------------- begin -------------------------------
def Habbitclockin(root, max_width, max_height):
    clear_frame(root)
    print('This is Habbitclockin now')

    # 存放栏目名称的列表
    columns = []

    # 创建样式对象
    style = ttk.Style()
    style.configure('TEntry', font=('consolas', 12))
    style.configure('TButton', font=('consolas', 12))
    style.configure('Listbox.TLabel', font=('consolas', 12))

    # 输入框
    entry_var = tk.StringVar()
    entry = ttk.Entry(root, textvariable=entry_var, style='TEntry')
    entry.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky='ew')

    # 添加栏目功能
    def add_column():
        name = entry_var.get().strip()
        if name:
            columns.append(name)
            listbox.insert(tk.END, name)
            entry_var.set("")

    add_btn = ttk.Button(root, text="添加栏目", command=add_column, style='TButton')
    add_btn.grid(row=1, column=0, columnspan=2, pady=5, padx=20, sticky='ew')

    # 显示栏目列表的Listbox
    listbox = tk.Listbox(root, font=('consolas', 12), height=20)
    listbox.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky='nsew')

    # 设置列和行的权重
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)

    # 绑定双击事件
    def on_double_click(event):
        selected_item = listbox.curselection()
        if selected_item:
            index = selected_item[0]
            column_name = columns[index]
            print(f"编辑栏目: {column_name}")
            edit_column(index, column_name)

    listbox.bind("<Double-1>", on_double_click)

    # 编辑栏目功能
    def edit_column(index, old_name):
        def save_edit():
            new_name = entry_var.get().strip()
            if new_name and new_name != old_name:
                columns[index] = new_name
                listbox.delete(index)
                listbox.insert(index, new_name)
                entry_var.set("")
            edit_window.destroy()

        edit_window = tk.Toplevel(root)
        edit_window.title("编辑栏目")
        edit_window.geometry("300x150")

        label = tk.Label(edit_window, text="修改栏目名称:", font=('consolas', 12))
        label.pack(pady=10)

        entry_edit = tk.Entry(edit_window, textvariable=entry_var, font=('consolas', 12))
        entry_edit.pack(pady=10)

        save_btn = tk.Button(edit_window, text="保存", command=save_edit, font=('consolas', 12))
        save_btn.pack(pady=10)

        entry_edit.insert(0, old_name)
        entry_edit.focus()
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
    elif name == 'Habbitclockin':
        Habbitclockin(root, max_width, max_height)
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
