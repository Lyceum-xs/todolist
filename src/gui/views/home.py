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
    root.rowconfigure(5, weight = 0)

    style = ttk.Style()
    style.configure('Home.TButton', 
                   background='#FFFFFF',
                   foreground='#000000',
                   font = ('consolas', 10),
                   borderwidth=0,
                   padding=0,
                   relief='flat')

    # Search Bar
    #-------------------------- begin ------------------------------
    '''
    search_frame = ttk.Frame(root)
    search_frame.grid(row=0, column=0, sticky='w', pady=(15,0), padx=40)

    target = tk.StringVar()
    target.set('Search Task')

    search_bar = tk.Entry(search_frame, textvariable = target, width = 45, font = ('consolas', 12))
    search_bar.grid(row = 0, column = 0)

    def search():
        value = target.get()
        print(f'Get entry: {value}')

    search_button = ttk.Button(search_frame, command = search, text = 'search', style = 'Home.TButton')
    search_button.grid(row = 0, column = 1, padx = (1, 0))
    '''
    #--------------------------- End --------------------------


    # Menu bar
    #-------------------------- begin ------------------------------
    style.configure('Meau.TFrame', background = '#FFFFFF')
    menu_bar = ttk.Frame(root, style = 'Menu.TFrame')
    menu_bar.grid(row = 1, column = 0, sticky = 'ew', pady=(10, 0))


    # Sort Bar
    #-------------------------- Begin -------------------------
    sort_basis = ['Due Date', 'Urgency', 'Importance', 'Default']
    s = tk.StringVar()
    
    sort_bar = ttk.Combobox(menu_bar, width = 15, state = 'readonly', textvariable = s, values = sort_basis, font = ('consolas', 12))
    sort_bar.grid(row = 0, column = 0)

    sort_bar.set('Default')

    def select(event):
        print(f'Get sort basis: {s.get()}')
        update_treeview()

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

    
    '''
    tasks = services.TaskServices.gettasks()
    if not tasks:
        print('No task')
    else:
        print(tasks)
    '''


    def update_treeview():
        def gettasks(tasks, error):
            if error:
                print(error)
                return

            def collect_expanded(item, _dict):
                tags = tree_view.item(item, 'tags')
                if tags:
                    _dict.update({int(tags[0]) : tree_view.item(item, 'open')})
                for child in tree_view.get_children(item):
                    collect_expanded(child, _dict)

            expansion_state = {}
            for item in tree_view.get_children():
                collect_expanded(item, expansion_state)
        
            tree_view.delete(*tree_view.get_children())

            task_id_to_tree_id = {}

            parent = ''
            for task in tasks:
                if task['parent_id'] is None:
                    parent = ''
                else:
                    parent = task_id_to_tree_id[task['parent_id']]
                tree_id = tree_view.insert(parent, 'end', text = task['name'], values = (services.TimeServices.turn_datetime_strf(task['due_date']), task['urgent'], task['importance'], task['completed']), tags = (task['id'],))
                task_id_to_tree_id.update({task['id'] : tree_id})

            for task_id, is_expanded in expansion_state.items():
                if task_id in task_id_to_tree_id:
                    tree_item = task_id_to_tree_id[task_id]
                    tree_view.item(tree_item, open = is_expanded)

        services.TaskServices.gettasks(s.get(), gettasks)

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
            menu.add_command(label = 'Edit due_date', command = lambda: edit_due_date(item))
            menu.post(event.x_root, event.y_root)

    tree_view.bind('<Button-3>', show_context_menu)

    def updatetask(success, error):
        if error:
            print(error)
            return

        update_treeview()

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
        
            tags = tree_view.item(item, 'tags')
            if tags:
                task_id = int(tags[0])

                services.TaskServices.updatetask(task_id, {'name' : new_name}, updatetask)
            
            edit_entry.destroy()

        def cancel_rename(e=None):
            if edit_entry.winfo_exists(): 
                edit_entry.destroy()

    def delete_item(item):
        tags = tree_view.item(item, 'tags')
        if tags:
            task_id = int(tags[0])

            def deltask(success, error):
                if error:
                    print(error)
                    return

                update_treeview()

            services.TaskServices.deltask(task_id, deltask)
            

    def done_item(item):
        tags = tree_view.item(item, 'tags')

        services.TaskServices.updatetask(int(tags[0]), {'completed' : True}, updatetask)
        
        def gettask(task, error):
            if error:
                print(error)
                return

            if task['parent_id'] is not None:
                def getparent(parent_task, error):
                    if error:
                        print(error)
                        return

                    def getchildren(children, error):
                        if error:
                            print(error)
                            return

                        all_done = True
                        for child in children:
                            if not child['completed']:
                                all_done = False

                        if all_done:
                            services.TaskServices.updatetask(task['parent_id'], {'completed' : True}, updatetask)
                
                    services.TaskServices.getchildren(task['parent_id'], getchildren)
                
                services.TaskServices.gettask(task['parent_id'], getparent)

        services.TaskServices.gettask(int(tags[0]), gettask)     

    def newchild_item(item):
        tags = tree_view.item(item, 'tags')
        add(int(tags[0]))

    def edit_due_date(item):
        if not item:
            return
    
        tags = tree_view.item(item, 'tags')
        if not tags:
            return
        task_id = int(tags[0])
        
        def gettask(task, error):
            if error:
                print(error)
                return

            current_due_date = task.get('due_date')
            if current_due_date:
                # prase ISO formatted date and time
                import datetime
                dt = datetime.datetime.fromisoformat(current_due_date)
                year, month, day, hour, minute = dt.year, dt.month, dt.day, dt.hour, dt.minute
            else:
                # if there is no deadline, use the current time
                time = services.TimeServices.gettime()
                year, month, day, hour, minute = time['year'], time['month'], time['day'], time['hour'], time['minute']
    
            edit_window = tk.Toplevel(root)
            edit_window.title('Edit Due Date')
            edit_window.geometry(f'{400}x{200}+{max_width}+{int(max_height * 0.5)}')
            edit_window.transient(root)
            edit_window.grab_set()
    
            time_frame = ttk.Frame(edit_window)
            time_frame.pack(pady=20)
    
            labels = [
                ttk.Label(time_frame, text='Year:'),
                ttk.Label(time_frame, text='Month:'),
                ttk.Label(time_frame, text='Day:'),
                ttk.Label(time_frame, text='Hour:'),
                ttk.Label(time_frame, text='Minute:')
            ]
    
            for i, label in enumerate(labels):
                label.grid(row=0, column=i, padx=5)
    
            dl_year = tk.StringVar(value=str(year))
            dl_month = tk.StringVar(value=str(month))
            dl_day = tk.StringVar(value=str(day))
            dl_hour = tk.StringVar(value=str(hour))
            dl_minute = tk.StringVar(value=str(minute))
    
            spinboxes = [
                tk.Spinbox(time_frame, from_=2000, to=2100, textvariable=dl_year, width=5),
                tk.Spinbox(time_frame, from_=1, to=12, textvariable=dl_month, width=5),
                tk.Spinbox(time_frame, from_=1, to=31, textvariable=dl_day, width=5),
                tk.Spinbox(time_frame, from_=0, to=23, textvariable=dl_hour, width=5),
                tk.Spinbox(time_frame, from_=0, to=59, textvariable=dl_minute, width=5)
            ]
    
            for i, spinbox in enumerate(spinboxes):
                spinbox.grid(row=1, column=i, padx=5)
    
            button_frame = ttk.Frame(edit_window)
            button_frame.pack(pady=10)
    
            def save():
                try:
                    # create new due date
                    new_due_date = services.TimeServices.create_datetime(
                        int(dl_year.get()),
                        int(dl_month.get()),
                        int(dl_day.get()),
                        int(dl_hour.get()),
                        int(dl_minute.get())
                    ).isoformat()
            
                    services.TaskServices.updatetask(task_id, {'due_date': new_due_date}, updatetask)
            
                    edit_window.destroy()
                except Exception as e:
                    print(f"Error updating due date: {e}")
                    from tkinter import messagebox
                    messagebox.showerror("Error", f"Failed to update due date: {e}")
    
            def cancel():
                edit_window.destroy()
    
            # button
            save_button = ttk.Button(button_frame, text="Save", command=save)
            save_button.grid(row=0, column=0, padx=10)
    
            cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel)
            cancel_button.grid(row=0, column=1, padx=10)

        task = services.TaskServices.gettask(task_id, gettask)
    
        

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

        time = services.TimeServices.gettime()
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

        dl_year.set(str(year))
        dl_month.set(str(month))
        dl_day.set(str(day))
        dl_hour.set(str(hour))
        dl_minute.set(str(minute))

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

        def addtask(success, error):
            if error:
                print(error)
                return

            update_treeview()

        def submit():
            services.TaskServices.addtask({
                'name' : taskname.get(), 
                'description' : 'test',
                'due_date' : services.TimeServices.create_datetime(int(dl_year.get()), int(dl_month.get()), int(dl_day.get()), int(dl_hour.get()), int(dl_minute.get())).isoformat(),
                'importance' : option_i.get(),
                'urgent' : option_u.get(),
                'parent_id' : parent_id
                }, addtask)
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
