from calendar import Day
from tkinter import *
from tkinter import ttk
import tkinter as tk
from token import COMMA
from tokenize import String
import get_data

# home content
#-------------------------------- begin -------------------------------
def Home(root, max_width, max_height):
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
    print('This is settings now')
#--------------------------------- End --------------------------------


# timer content
#-------------------------------- begin -------------------------------
def Timer(root, max_width, max_height):
    print('This is timer now')
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