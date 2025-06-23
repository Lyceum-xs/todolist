import tkinter as tk
from tkinter import *
from tkinter import ttk



#init
root = tk.Tk()
root.title('To Do List')
max_size = root.maxsize()   #get your windows' resolution 
width, heigth = max_size
root.geometry(f'{int(width*0.25)}x{int(heigth*0.5)}')   #calculation the width and height

root.resizable(False, False)    #set can't be sized

#root.iconbitmap('')    #set logo

root.configure(bg = '#E6E6E6')  #set background color

root.attributes('-topmost', True)   #set top

root.mainloop() #begin main
