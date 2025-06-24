from tkinter import *
from tkinter import ttk

# 导航栏--在根窗口中一直存在
def NavigationBar(root, max_width, max_height):
    # 创建样式对象
    style = ttk.Style()
    style.configure('Nav.TFrame', background='#FFFFFF')
    
    nb = ttk.Frame(root, style='Nav.TFrame')
    w = int(max_width * 0.3)
    h = max_height
    nb.place(x=0, y=0, width=w, height=h)

    # 配置纯文字按钮样式
    style.configure('TextOnly.TButton', 
                   background='#FFFFFF',  # 背景透明
                   foreground='#000000',    # 文字颜色
                   font = ('consolas', 14),
                   borderwidth=0,         # 无边框
                   padding=0,             # 无内边距
                   relief='flat')         # 平面样式
    
    # 禁用按钮的所有视觉反馈
    style.map('TextOnly.TButton',
              background=[],
              relief=[],
              bordercolor=[])

    home_button = ttk.Button(nb, text = 'Home', style = 'TextOnly.TButton').place(x = 0, y = 0, width = w)
    settings_button = ttk.Button(nb, text = 'Settings', style = 'TextOnly.TButton').place(x = 0, y = h / 15, width = w)