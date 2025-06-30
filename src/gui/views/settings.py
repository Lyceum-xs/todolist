from tkinter import *
from tkinter import ttk
import tkinter as tk
from ..utils import clear_frame

# settings content
#-------------------------------- begin -------------------------------
def Settings(root, max_width, max_height):
    clear_frame(root)
    print('This is settings now')

    def toggle_simple_mode():
        # 这里后续可添加简洁模式切换逻辑
        pass

    switch_btn = tk.Button(
        root,
        text="切换模式",
        font=("consolas", 12),
        width=15,
        command=toggle_simple_mode
    )
    switch_btn.pack(pady=20)
#--------------------------------- End --------------------------------
