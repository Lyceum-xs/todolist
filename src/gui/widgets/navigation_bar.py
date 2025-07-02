from tkinter import *
from tkinter import ttk
from .content_bar import Choose_content, ContentBar
from ..views.home import Home

# navigation bar
#-------------------------------- begin -------------------------------
def NavigationBar(root, max_width, max_height):
    
    # create a style object
    style = ttk.Style()
    style.configure('Nav.TFrame', background='#FFFFFF')

    nb = ttk.Frame(root, style='Nav.TFrame')
    w = int(max_width * 0.3)
    h = max_height
    nb.place(x=0, y=0, width=w, height=h)

    style.configure('Text.TLabel', 
                   background='#FFFFFF',
                   foreground='#000000',
                   font = ('consolas', 28))

    # configure button style
    style.configure('Nav.TButton', 
                   background='#FFFFFF',
                   foreground='#000000',
                   font = ('consolas', 14),
                   borderwidth=0,         # borderless
                   padding=0,             # no inner padding
                   relief='flat')         # flat style

    title = ttk.Label(nb, text = 'To Do List', style = 'Text.TLabel').grid(row = 0, column = 0, sticky='ew',padx = (20, 0), pady = (30, 30))

    # set up the content bar
    con_bar = ContentBar(root, max_width, max_height)

    nb.columnconfigure(0, weight = 1)

    home_button = ttk.Button(nb, text = 'Home', style = 'Nav.TButton')
    home_button.grid(row = 1, column = 0, sticky='ew', pady = (0, 5))
    home_button.bind('<Button-1>', lambda e: Choose_content('Home', con_bar, max_width - w, max_height - 20))
    
    settings_button = ttk.Button(nb, text = 'Habitclockin', style = 'Nav.TButton')
    settings_button.grid(row = 2, column = 0, sticky='ew', pady = (0, 5))
    settings_button.bind('<Button-1>', lambda e: Choose_content('Habitclockin', con_bar, max_width - w, max_height - 20))
    
    timer_button = ttk.Button(nb, text = 'Timer', style = 'Nav.TButton')
    timer_button.grid(row = 3, column = 0, sticky='ew', pady = (0, 5))
    timer_button.bind('<Button-1>', lambda e: Choose_content('Timer', con_bar, max_width - w, max_height - 20))

    habitclockin_button = ttk.Button(nb, text = 'Calendar', style = 'Nav.TButton')
    habitclockin_button.grid(row = 4, column = 0, sticky = 'ew', pady = (0, 5))
    habitclockin_button.bind('<Button-1>', lambda e: Choose_content('Calendar', con_bar, max_width - w, max_height - 20))

    # set default content bar
    Home(con_bar, max_width - w, max_height - 20)

    return nb
#--------------------------------- End --------------------------------

