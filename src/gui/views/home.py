from tkinter import *
from tkinter import ttk
import tkinter as tk
from ..utils import clear_frame
from .. import get_data


# home content
#-------------------------------- begin -------------------------------
def Home(root, max_width, max_height):
    clear_frame(root)   # initialize content frame
    print('This is home now')
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight = 0)

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
    sort_basis = ['Due Date', 'Urgency', 'Importance']
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
