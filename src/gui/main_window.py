from tkinter import *
from tkinter import ttk
import task_item


root = Tk()
root.title('To Do List')
max_width, max_height = root.maxsize()

w = int(max_width * 0.5)
h = int(max_height * 0.5)

root.geometry(f'{w}x{h}')
root.resizable(False, False)    # ���ô��ڲ�������
root.overrideredirect(True)    # �Ƴ����д�������

# ��Ӵ����϶�����
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

# ������¼�ʵ�ִ����϶�
root.bind("<ButtonPress-1>", start_move)
root.bind("<ButtonRelease-1>", stop_move)
root.bind("<B1-Motion>", do_move)

task_item.NavigationBar(root, w, h)

def show_root():
    root.mainloop()