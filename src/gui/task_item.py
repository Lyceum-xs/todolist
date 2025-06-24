from tkinter import *
from tkinter import ttk
import tkinter

# ������--�ڸ�������һֱ����
def NavigationBar(root, max_width, max_height):
    
    # ������ʽ����
    style = ttk.Style()
    style.configure('Nav.TFrame', background='#FFFFFF')

    nb = ttk.Frame(root, style='Nav.TFrame')
    w = int(max_width * 0.3)
    h = max_height
    nb.place(x=0, y=0, width=w, height=h)

    style.configure('Text.TLabel', 
                   background='#FFFFFF',  # ����͸��
                   foreground='#000000',    # ������ɫ
                   font = ('consolas', 28))

    # ���ð�ť��ʽ
    style.configure('Nav.TButton', 
                   background='#FFFFFF',  # ����͸��
                   foreground='#000000',    # ������ɫ
                   font = ('consolas', 14),
                   borderwidth=0,         # �ޱ߿�
                   padding=0,             # ���ڱ߾�
                   relief='flat')         # ƽ����ʽ
   

    title = ttk.Label(nb, text = 'To Do List', style = 'Text.TLabel').place(x = 20, y = 30, width = w)

    home_button = ttk.Button(nb, text = 'Home', style = 'Nav.TButton').place(x = 0, y = h / 15 * 3, width = w)
    settings_button = ttk.Button(nb, text = 'Settings', style = 'Nav.TButton').place(x = 0, y = h / 15 * 4, width = w)
    timer_button = ttk.Button(nb, text = 'Timer', style = 'Nav.TButton').place(x = 0, y = h / 15 * 5, width = w)

    return nb

# �Զ��������
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
    
    # �󶨹رչ���
    close_button.bind("<Button-1>", lambda e: root.destroy())

    return title_frame