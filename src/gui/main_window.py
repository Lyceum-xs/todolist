from tkinter import *
from tkinter import ttk
import task_item


root = Tk()
root.title('To Do List')
max_width, max_height = root.maxsize()

w = int(max_width * 0.5)
h = int(max_height * 0.5)

root.geometry(f'{w}x{h}+{int(w * 0.5)}+{int(h * 0.5)}')
root.resizable(False, False)    # 设置窗口不可拉伸
root.overrideredirect(True)    # 移除所有窗口修饰

# 添加窗口拖动功能
def start_move(event):
    root.x = event.x
    root.y = event.y
    
def stop_move(event):
    root.x = None
    root.y = None
    
def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

# 创建导航栏，标题栏和内容栏
nav_bar = task_item.NavigationBar(root, w, h)
title_bar = task_item.TitleBar(root, w, h)

# 启用标题栏拖动
def enable_drag_for_frame(frame):
    frame.bind("<ButtonPress-1>", start_move)
    frame.bind("<ButtonRelease-1>", stop_move)
    frame.bind("<B1-Motion>", do_move)

enable_drag_for_frame(title_bar)

def show_root():
    root.mainloop()