from tkinter import *
from tkinter import ttk
import tkinter

# 导航栏--在根窗口中一直存在
def NavigationBar(root, max_width, max_height):
    
    # 创建样式对象
    style = ttk.Style()
    style.configure('Nav.TFrame', background='#FFFFFF')

    nb = ttk.Frame(root, style='Nav.TFrame')
    w = int(max_width * 0.3)
    h = max_height
    nb.place(x=0, y=0, width=w, height=h)

    style.configure('Text.TLabel', 
                   background='#FFFFFF',  # 背景透明
                   foreground='#000000',    # 文字颜色
                   font = ('consolas', 28))

    # 配置按钮样式
    style.configure('Nav.TButton', 
                   background='#FFFFFF',  # 背景透明
                   foreground='#000000',    # 文字颜色
                   font = ('consolas', 14),
                   borderwidth=0,         # 无边框
                   padding=0,             # 无内边距
                   relief='flat')         # 平面样式
   

    title = ttk.Label(nb, text = 'To Do List', style = 'Text.TLabel').place(x = 20, y = 30, width = w)

    home_button = ttk.Button(nb, text = 'Home', style = 'Nav.TButton').place(x = 0, y = h / 15 * 3, width = w)
    settings_button = ttk.Button(nb, text = 'Settings', style = 'Nav.TButton').place(x = 0, y = h / 15 * 4, width = w)
    timer_button = ttk.Button(nb, text = 'Timer', style = 'Nav.TButton').place(x = 0, y = h / 15 * 5, width = w)

    return nb

# 自定义标题栏
def TitleBar(root, max_width, max_height):
    style = ttk.Style()
    
    style.configure('Tit.TFrame', background = '#FFFFFF')

    title_frame = ttk.Frame(root, style = 'Tit.TFrame')
    w = int(max_width - max_width * 0.3)
    x_place = int(max_width * 0.3)
    h = 20

    title_frame.place(x = x_place, y = 0, width = w, height = h)

    style.configure('Tit.TButton', 
                   background='#FFFFFF',
                   foreground='#000000',
                   font = ('consolas', 10),
                   borderwidth=0,
                   padding=0,
                   relief='flat')
    
    close_button = ttk.Button(title_frame, text = 'X', style = 'Tit.TButton')
    close_button.place(x = 570, y = 0, width = 25, height = h)
    
    # 绑定关闭功能
    close_button.bind("<Button-1>", lambda e: root.destroy())

    return title_frame