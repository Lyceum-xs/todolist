from tkinter import *
from tkinter import ttk

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
