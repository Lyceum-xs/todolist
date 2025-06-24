from tkinter import *
from tkinter import ttk
import task_item


root = Tk()
root.title('To Do List')
max_width, max_height = root.maxsize()

w = int(max_width * 0.5)
h = int(max_height * 0.5)

root.geometry(f'{w}x{h}')
root.resizable(False, False)

task_item.NavigationBar(root, w, h)

def show_root():
    root.mainloop()