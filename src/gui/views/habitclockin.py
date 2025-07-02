from tkinter import *
from tkinter import ttk
import tkinter as tk
from ..utils import clear_frame

# settings content
#-------------------------------- begin -------------------------------
def Habitclockin(root, max_width, max_height):
    clear_frame(root)
    print('This is Habitclockin now')

    root.columnconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 0)
    root.rowconfigure(2, weight = 0)

    style = ttk.Style()

    style.configure('Hab.TLabel', font = ('consolas', 14))
    style.configure('Hab.TButton', 
                   background='#FFFFFF',
                   foreground='#000000',
                   font = ('consolas', 10),
                   borderwidth=0,
                   padding=0,
                   relief='flat')

    ttk.Label(root, text = 'Form new habits', style = 'Hab.TLabel').grid(row = 0, column = 0, sticky = 'ew')
    ttk.Label(root, text = 'My habits', style = 'Hab.TLabel').grid(row = 4, column = 0, sticky = 'ew')

    habit_name = tk.StringVar()
    habit_description = tk.StringVar()

    habit_name.set('Name your habit')
    habit_description.set('Describe your habit')

    name_entry = tk.Entry(root, textvariable = habit_name, width = 50, font = ('consolas', 12))
    description_entry = tk.Entry(root, textvariable = habit_description, width = 50, font = ('consolas', 12))
    name_entry.grid(row = 1, column = 0, sticky = 'ew', pady = 5)
    description_entry.grid(row = 2, column = 0, sticky = 'ew', pady = 5)

    def create_habit():
        print(f'{habit_name.get()} is created: {habit_description.get()}')

    create_button = ttk.Button(root, text = 'create', style = 'Hab.TButton', command = create_habit)
    create_button.grid(row = 3, column = 0, sticky = 'ew')

    habit_frame = ttk.Frame(root)
    habit_frame.grid(row = 5, column = 0, sticky = 'ew')
#--------------------------------- End --------------------------------
