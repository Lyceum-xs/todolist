from tkinter import *
from tkinter import ttk
import tkinter as tk
from .. import services
from ..utils import clear_frame

# settings content
#-------------------------------- begin -------------------------------
def Habitclockin(root, max_width, max_height):
    clear_frame(root)
    print('This is Habitclockin now')

    root.columnconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 0)
    root.rowconfigure(2, weight = 0)
    root.rowconfigure(5, weight = 1)

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
    ttk.Label(root, text = 'My habits', style = 'Hab.TLabel').grid(row = 4, column = 0, sticky = 'ew', pady = 5)

    habit_name = tk.StringVar()
    habit_description = tk.StringVar()

    habit_name.set('Name your habit')
    habit_description.set('Describe your habit')

    name_entry = tk.Entry(root, textvariable = habit_name, width = 50, font = ('consolas', 12))
    description_entry = tk.Entry(root, textvariable = habit_description, width = 50, font = ('consolas', 12))
    name_entry.grid(row = 1, column = 0, sticky = 'ew', pady = 5)
    description_entry.grid(row = 2, column = 0, sticky = 'ew', pady = 5)

    def create_habit():
        habit = {'name' : habit_name.get(), 'description' : habit_description.get(), 'duration' : 0}
        services.HabitServices.create_habit(habit)
        update_habits()
        

    create_button = ttk.Button(root, text = 'create', style = 'Hab.TButton', command = create_habit)
    create_button.grid(row = 3, column = 0, sticky = 'ew')

    habits_container = ttk.Frame(root)
    habits_container.grid(row=5, column=0, sticky='nsew')
    habits_container.columnconfigure(0, weight=1)
    habits_container.rowconfigure(0, weight=1)

    canvas = Canvas(habits_container, borderwidth = 0, highlightthickness = 0)
    vsb = ttk.Scrollbar(habits_container, orient="vertical", command=canvas.yview)
    hsb = ttk.Scrollbar(habits_container, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    habits_frame = ttk.Frame(canvas)
    canvas_frame = canvas.create_window((0, 0), window = habits_frame, anchor="nw")

    def configure_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_frame, width = event.width)
    
    habits_frame.bind("<Configure>", configure_scrollregion)
    canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_frame, width=event.width))

    habits_frame.columnconfigure(0, weight = 1)

    def update_habits():
        for widget in habits_frame.winfo_children():
            widget.destroy()

        habits = services.HabitServices.get_habits()

        r = 0
        for habit in habits:
            habit_frame = ttk.Frame(habits_frame)
            habit_frame.grid(row = r, column = 0, padx = 10, sticky = 'ew')
            habit_frame.columnconfigure(0, weight = 1)
            
            def getdays(habit_id):
                return services.HabitServices.get_consecutive_clockin_days(habit_id)

            name_label = ttk.Label(habit_frame, text = habit['name'], font = ('consolas', 12))
            description_label = ttk.Label(habit_frame, text = habit['description'], font = ('consolas', 10))
            duration_label = ttk.Label(habit_frame, text = f'Consecutive clockin days:{getdays(habit['id'])}', font = ('consolas', 12))
            name_label.grid(row = 0, column = 0, pady = 5, sticky = 'w')
            description_label.grid(row = 1, column = 0, sticky = 'w')
            duration_label.grid(row = 0, column = 1, sticky = 'e', padx = 5)
            


            delete_button = ttk.Button(habit_frame, text = 'delete', style = 'Hab.TButton', command = lambda habit_id = habit['id']: delhabit(habit_id))
            delete_button.grid(row = 0, column = 2, sticky = 'e')
            clockin_button = ttk.Button(habit_frame, text = 'clockin', style = 'Hab.TButton', command = lambda habit_id = habit['id']: clohabit(habit_id))
            clockin_button.grid(row = 1, column = 2, sticky = 'e')
        
            def delhabit(habit_id):
                services.HabitServices.delete_habit(habit_id)
                update_habits()

            def clohabit(habit_id):
                services.HabitServices.clockin_habit(habit_id)
                update_habits()
            r += 1

    update_habits()
#--------------------------------- End --------------------------------
