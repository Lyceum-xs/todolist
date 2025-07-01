from os import name
from tkinter import *
from tkinter import ttk
import tkinter as tk
from ..utils import clear_frame
from .. import services


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
    sort_bar.grid(row = 0, column = 0)

    sort_bar.set('Sort Basis')

    def select(event):
        print(f'Get sort basis: {s.get()}')

    sort_bar.bind('<<ComboboxSelected>>', select)
    #--------------------------- End --------------------------


    # add none
    menu_bar.columnconfigure(1, weight=1)
    
    add_button = ttk.Button(menu_bar, command = lambda: add(None), text = '+ Add', width = 6, style = 'Home.TButton')
    add_button.grid(row = 0, column = 3, padx = 5)

    #--------------------------- End --------------------------


    #task tree view
    #-------------------------- Begin -------------------------
    root.rowconfigure(2, weight = 1)
    task_frame = ttk.Frame(root)
    task_frame.grid(row = 2, column = 0, sticky = 'nsew')
    
    task_frame.columnconfigure(0, weight = 1)
    task_frame.rowconfigure(0, weight = 1)
    
    vsb = ttk.Scrollbar(task_frame, orient="vertical")
    hsb = ttk.Scrollbar(task_frame, orient="horizontal")

    tree_view = ttk.Treeview(
        task_frame, 
        columns = ('due_date', 'urgency', 'importance', 'completed'), 
        yscrollcommand=vsb.set, 
        xscrollcommand=hsb.set,
        show = 'tree headings',
        selectmode = 'extended'
        )
    tree_view.grid(row = 0, column = 0, sticky = 'nsew')

    vsb.config(command = tree_view.yview)
    hsb.config(command = tree_view.xview)
    vsb.grid(row = 0, column = 1, sticky = 'ns')
    hsb.grid(row = 1, column = 0, sticky = 'ew')

    tree_view.heading('#0', text = 'name', anchor = tk.W)
    tree_view.column('#0', width=150, minwidth=100, anchor = tk.W)

    columns = {
        'due_date' : {'width' : 150, 'anchor' : tk.W},
        'urgency' : {'width' : 70, 'anchor' : tk.W},
        'importance' : {'width' : 70, 'anchor' : tk.W},
        'completed' : {'width' : 70, 'anchor' : tk.W}
        }
    for col, settings in columns.items():
            tree_view.heading(col, text = col)
            tree_view.column(col, **settings)

    
    tasks = services.gettasks()
    if not tasks:
        print('No task')
    else:
        print(tasks)

    def update_treeview():
        tree_view.delete(*tree_view.get_children())

        tasks = services.gettasks()

        task_id_to_tree_id = {}

        parent = ''
        for task in tasks:
            if task.parent_id is None:
                parent = ''
            else:
                parent = task_id_to_tree_id[task.parent_id]
            tree_id = tree_view.insert(parent, 'end', text = task.name, values = (task.due_date, task.urgent, task.importance, task.completed), tags = (task.id,))
            task_id_to_tree_id.update({task.id : tree_id})

    update_treeview()

    def show_context_menu(event):
        item = tree_view.identify_row(event.y)
        if item:
            tree_view.selection_set(item)

            menu = tk.Menu(root, tearoff = 0)

            menu.add_command(label = 'Rename', command = lambda: rename_item(item))
            menu.add_command(label = 'Delete', command = lambda: delete_item(item))
            menu.add_command(label = 'Done', command = lambda: done_item(item))
            menu.add_command(label = 'New child', command = lambda: newchild_item(item))
            menu.post(event.x_root, event.y_root)

    tree_view.bind('<Button-3>', show_context_menu)

    def rename_item(item):
        if not item:
            return
        # get now position
        x, y, width, height = tree_view.bbox(item, column="#0")
        
        # get now text
        current_text = tree_view.item(item, "text")
        
        # create edit
        edit_entry = ttk.Entry(tree_view)
        edit_entry.insert(0, current_text)
        edit_entry.select_range(0, tk.END)
        edit_entry.focus()
        
        # locate edit
        edit_entry.place(x=x, y=y, width=width, height=height)
        
        edit_entry.bind("<Return>", lambda e: save_rename(item))
        edit_entry.bind("<Escape>", lambda e: cancel_rename())
        edit_entry.bind("<FocusOut>", lambda e: save_rename(item))
    
        def save_rename(item):
            new_name = edit_entry.get()
            tree_view.item(item, text=new_name)
        
            edit_entry.destroy()
    
        def cancel_rename(e=None):
            if edit_entry.winfo_exists(): 
                edit_entry.destroy()

    def delete_item(item_id):
        tags = tree_view.item(item_id, 'tags')
        if tags:
            task_id = tags[0]
            services.deltask(task_id)
            update_treeview()

    def done_item(item):
        tags = tree_view.item(item, 'tags')
        services.updatetask(tags[0], {'completed' : True})
        '''
        task = services.gettask(tags[0])
        if task.parent_id is not None:
            parent_task = services.gettask(task.parent_id)
            children = services.getchildren(task.parent_id)

            print(parent_task)
            print(children)

            all_done = True
            for child in children:
                if not child.completed:
                    all_done = False

            if all_done:
                services.updatetask(task.parent_id, {'completed' : True})
        '''
        update_treeview()

    def newchild_item(item):
        tags = tree_view.item(item, 'tags')
        add(tags[0])


    # Add
    #-------------------------- Begin -------------------------
    def add(parent_id):
        print(f'task is adding...')

        window = tk.Toplevel(root)
        window.title('Add New Task')
        window.geometry(f'{max_width}x{int(max_height * 0.5)}+{max_width}+{int(max_height * 0.5)}')

        window.transient(root)
        window.grab_set()

        input_frame = ttk.Frame(window)
        input_frame.grid(row=0, column=0, columnspan=2, pady=25, sticky='nsew')

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

        time = services.gettime()
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

        Radio_frame = ttk.Frame(window)
        Radio_frame.grid(row = 3, column = 0)

        u_label = ttk.Label(Radio_frame, text = 'Urgency:', style = 'Home.TLabel')
        i_label = ttk.Label(Radio_frame, text = 'Importance:', style = 'Home.TLabel')
        u_label.grid(row = 0, column = 0, pady = 10)
        i_label.grid(row = 1, column = 0)

        option_u = tk.StringVar()
        u_radiobutton_1 = tk.Radiobutton(Radio_frame, text = 'True', variable = option_u, value = True)
        u_radiobutton_2 = tk.Radiobutton(Radio_frame, text = 'False', variable = option_u, value = False)
        u_radiobutton_2.select()
        u_radiobutton_1.grid(row = 0, column = 1)
        u_radiobutton_2.grid(row = 0, column = 2)
        option_i = tk.StringVar()
        i_radiobutton_1 = tk.Radiobutton(Radio_frame, text = 'True', variable = option_i, value = True)
        i_radiobutton_2 = tk.Radiobutton(Radio_frame, text = 'False', variable = option_i, value = False)
        i_radiobutton_2.select()
        i_radiobutton_1.grid(row = 1, column = 1)
        i_radiobutton_2.grid(row = 1, column = 2)
        

        def close():
            window.destroy()

        def cancel():
            print('Addition is canceled, no submission')
            close()

        def submit():
            services.addtask({
                'name' : taskname.get(), 
                'description' : 'test',
                'due_date' : services.create_datetime(int(dl_year.get()), int(dl_month.get()), int(dl_day.get())),
                'importance' : option_i.get(),
                'urgent' : option_u.get(),
                'parent_id' : parent_id
                })
            update_treeview()
            close()
        
        cancel_button = ttk.Button(window, command = cancel, text = 'cancel', style = 'Home.TButton')
        cancel_button.place(width = 80, height = 25, x = max_width - 180, y = int(max_height * 0.5 - 30))

        submit_button = ttk.Button(window, command = submit, text = 'submit', style = 'Home.TButton')
        submit_button.place(width = 80, height = 25, x = max_width - 90, y = int(max_height * 0.5 - 30))
    #--------------------------- End --------------------------

    is_expanded = False
    def exp_col():
        nonlocal is_expanded
        def expand_all():
            def expand(item):
                tree_view.item(item, open = True)
                for child in tree_view.get_children(item):
                    expand(child)

            for item in tree_view.get_children():
                expand(item)
            
        def collapse_all():
            def collapse(item):
                tree_view.item(item, open = False)
                for child in tree_view.get_children(item):
                    collapse(child)

            for item in tree_view.get_children():
                collapse(item)

        if not is_expanded:
            exp_col_button.config(text = 'Collapse all')
            expand_all()
            is_expanded = True
        else:
            exp_col_button.config(text = 'Expand all')
            collapse_all()
            is_expanded = False

    exp_col_button = ttk.Button(menu_bar, command = exp_col, text = 'Expand all', style = 'Home.TButton')
    exp_col_button.grid(row = 0, column = 2)
    #--------------------------- End --------------------------
#--------------------------------- End --------------------------------
