# clear all widgets in a frame
#-------------------------------- Begin -------------------------------
def clear_frame(frame):
    for widget in frame.winfo_children():
        if widget.winfo_children():
            clear_frame(widget)
        widget.destroy()
#--------------------------------- End --------------------------------


