from tkinter import *
from tkinter import ttk
import tkinter as tk
import get_data

def Home(root, max_width, max_height):
    print('This is home now')
    target = tk.StringVar()
    target.set('please entry the target')

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

    def get():
        print('Get entry')
        value = target.get()

    search_button = ttk.Button(root, command = get, text = 'search', style = 'Home.TButton')
    search_button.place(width = 60, height = 30, x = 411, y = 10)

def Settings(root, max_width, max_height):
    print('This is settings now')

def Timer(root, max_width, max_height):
    print('This is timer now')

def Choose_content(name, root, max_width, max_height):
    if name == 'Home':
        Home(root, max_width, max_height)
    elif name == 'Settings':
        Settings(root, max_width, max_height)
    elif name == 'Timer':
        Timer(root, max_width, max_height)

# Content Bar
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