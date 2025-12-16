import tkinter as tk

from functions.pages import main_page
from functions.gui import create_scrollable_frame
from config import WINDOW_SIZE

#Initiates and sets the frames
root = tk.Tk()
root.title("DnD Planner")
root.geometry(WINDOW_SIZE)
root.resizable(True, True)

container = tk.Frame(root)
container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = tk.Frame(container, bg="lightgray")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
left_scroll_frame = create_scrollable_frame(left_frame)

right_frame = tk.Frame(container, width=400, bg="lightgray")
right_frame.pack(side=tk.RIGHT, fill=tk.Y)
right_frame.pack_propagate(False)
right_scroll_frame = create_scrollable_frame(right_frame)

#Starts the program on the main page, and keeps it running
main_page(root, left_scroll_frame, right_scroll_frame)

root.mainloop()