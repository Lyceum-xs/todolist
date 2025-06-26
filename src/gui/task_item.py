from tkinter import *
from tkinter import ttk
import content_view

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
    con_bar = content_view.ContentBar(root, max_width, max_height)

    home_button = ttk.Button(nb, text = 'Home', style = 'Nav.TButton')
    nb.columnconfigure(0, weight = 1)
    home_button.grid(row = 1, column = 0, sticky='ew', pady = (0, 5))
    home_button.bind('<Button-1>', lambda e: content_view.Choose_content('Home', con_bar, max_width - w, max_height - 20))
    
    settings_button = ttk.Button(nb, text = 'Settings', style = 'Nav.TButton')
    settings_button.grid(row = 2, column = 0, sticky='ew', pady = (0, 5))
    settings_button.bind('<Button-1>', lambda e: content_view.Choose_content('Settings', con_bar, max_width - w, max_height - 20))
    
    timer_button = ttk.Button(nb, text = 'Timer', style = 'Nav.TButton')
    timer_button.grid(row = 3, column = 0, sticky='ew', pady = (0, 5))
    timer_button.bind('<Button-1>', lambda e: content_view.Choose_content('Timer', con_bar, max_width - w, max_height - 20))

    return nb
#--------------------------------- End --------------------------------


# customize the title bar
#-------------------------------- begin -------------------------------
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
    
    title_frame.columnconfigure(0, weight = 1)
    close_button = ttk.Button(title_frame, text = 'X', width = 5, style = 'Tit.TButton')
    close_button.grid(row = 0, column = 1)
    
    # bind the close function
    close_button.bind("<Button-1>", lambda e: root.destroy())

    return title_frame
#--------------------------------- End --------------------------------

