from tkinter import *
from tkinter import ttk

# ������--�ڸ�������һֱ����
def NavigationBar(root, max_width, max_height):
    # ������ʽ����
    style = ttk.Style()
    style.configure('Nav.TFrame', background='#FFFFFF')
    
    nb = ttk.Frame(root, style='Nav.TFrame')
    w = int(max_width * 0.3)
    h = max_height
    nb.place(x=0, y=0, width=w, height=h)

    # ���ô����ְ�ť��ʽ
    style.configure('TextOnly.TButton', 
                   background='#FFFFFF',  # ����͸��
                   foreground='#000000',    # ������ɫ
                   font = ('consolas', 14),
                   borderwidth=0,         # �ޱ߿�
                   padding=0,             # ���ڱ߾�
                   relief='flat')         # ƽ����ʽ
    
    # ���ð�ť�������Ӿ�����
    style.map('TextOnly.TButton',
              background=[],
              relief=[],
              bordercolor=[])

    home_button = ttk.Button(nb, text = 'Home', style = 'TextOnly.TButton').place(x = 0, y = 0, width = w)
    settings_button = ttk.Button(nb, text = 'Settings', style = 'TextOnly.TButton').place(x = 0, y = h / 15, width = w)