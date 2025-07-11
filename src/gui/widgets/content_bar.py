from tkinter import *
from tkinter import ttk
from ..views.home import Home
from ..views.habitclockin import Habitclockin
from ..views.timer import Timer
from ..views.calendar import Calendar

# Content Bar
#-------------------------------- begin -------------------------------
def ContentBar(root, max_width, max_height):
    style = ttk.Style()

    style.configure('Con.TFrame')

    content_frame = ttk.Frame(root, style = 'Con.TFrame')
    x_place = int(max_width * 0.3)
    y_place = 20
    w = int(max_width - x_place)
    h = int(max_height - y_place)

    content_frame.place(x = x_place, y = y_place, width = w, height = h)

    return content_frame
#--------------------------------- End --------------------------------

# choose content
#-------------------------------- begin -------------------------------
def Choose_content(name, root, max_width, max_height):
    if name == 'Home':
        Home(root, max_width, max_height)
    elif name == 'Habitclockin':
        Habitclockin(root, max_width, max_height)
    elif name == 'Timer':
        Timer(root, max_width, max_height)
    elif name == 'Calendar':
        Calendar(root, max_width, max_height)
#--------------------------------- End --------------------------------