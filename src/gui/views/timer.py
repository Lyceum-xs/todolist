import collections
from logging import root
from re import A
from tkinter import *
from tkinter import ttk
import tkinter as tk
from turtle import back
from ..utils import clear_frame
import pygame  # 用于播放mp3铃声

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
            try:
                pygame.mixer.init()
                pygame.mixer.music.load('docs/assets/preview.mp3')  
                pygame.mixer.music.play()
            except Exception as e:
                print(f"铃声播放失败: {e}")
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
