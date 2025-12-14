import tkinter as tk
import config

from models.region import *
from config import (
    BUTTON_PACK_OPTIONS,
    REGIONS_BUTTON_LABELS,
    SPECIFIC_REGION_BUTTON_LABELS
)
from functions.general import (
    load_json,
    line_break,
    find_category
)

def clear_widgets(parent):
    for w in parent.winfo_children():
        w.destroy()

def create_scrollable_frame(parent):
    container = tk.Frame(parent)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scroll_frame = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", update_scroll_region)

    def match_width(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", match_width)

    return scroll_frame

def initiate_page(root, left_scroll_frame, header_text, placeholder_text):
    clear_widgets(left_scroll_frame)

    header_label = tk.Label(left_scroll_frame, text=header_text, font=("Arial", 12, "bold"))
    header_label.pack(pady=10)

    placeholder_label = tk.Label(left_scroll_frame, text=placeholder_text, anchor="nw", justify="left")
    placeholder_label.pack(fill=tk.BOTH, expand=True)

    line_break(left_scroll_frame)
    return left_scroll_frame

def initiate_buttons(root, left_scroll_frame, right_scroll_frame, labels):
    from functions.onclick import on_button_click

    clear_widgets(right_scroll_frame)

    for label in labels:
        btn = tk.Button(right_scroll_frame, text=label,
                        command=lambda l=label: on_button_click(l, root, left_scroll_frame, right_scroll_frame))
        btn.pack(**BUTTON_PACK_OPTIONS)
    line_break(right_scroll_frame)
    return right_scroll_frame

def generate_buttons(root, left_scroll_frame, right_scroll_frame):
    from functions.onclick import on_button_click

    data = load_json("regions.json")
    items_to_list = []
    current = config.button_flag

    if config.nav_stack [-1] == "Regions" or config.nav_stack[-2] == "Regions":
        region_data = data[current]
        items_to_list = [c["City"] for c in region_data["Cities"]]
        items_to_list += [p["Point of Interest"] for p in region_data["POI"]]
    elif config.nav_stack[-3] == "Regions":
        item_type = find_category(current, data)
        region_name = config.nav_stack[-2]
        if item_type == "City":
            region_data = next(c for c in data[region_name]["Cities"] if c["City"] == name)
        elif item_type == "POI":
            region_data = next(p for p in data[region_name]["POI"] if p["Point of Interest"] == name)
    elif config.nav_stack[-4] == "Regions":
        pass

        items_to_list = [c["City"] for c in region_data["Cities"]]
        items_to_list += [p["Point of Interest"] for p in region_data["POI"]]

        for city in region_data["Cities"]:
            if city["City"] == current:
                items_to_list = [p["Point of Interest"] for p in city["POI"]]
                break
    elif config.nav_stack[-3] == "Regions":
        pass

    for label in items_to_list:
        btn = tk.Button(right_scroll_frame, text=label,
                        command=lambda l=label: on_button_click(l, root, left_scroll_frame, right_scroll_frame))
        btn.pack(fill=tk.X, padx=5, pady=5)

def submit_buttons(root, popup, text, function):
    btn_frame = tk.Frame(popup)
    btn_frame.pack(fill="x", pady=10, padx=10)
    tk.Button(btn_frame, text=text, command=function).pack(side="left", padx=(30, 0))
    tk.Button(btn_frame, text="Cancel", command=popup.destroy).pack(side="right", padx=(0, 30))
    popup.grab_set()
    root.wait_window(popup)

def close_popup_and_refresh(popup, root, left_frame, right_frame, refresh_fn):
    popup.destroy()
    if left_frame and right_frame:
        refresh_fn(root, left_frame, right_frame)


def initiate_popup(root, title, label, fields):
    popup = tk.Toplevel(root)
    popup.title(title)

    instr_label = tk.Label(popup, text=label)
    instr_label.pack()

    entries = {}

    if not fields:
        return popup, entries

    for field in fields:
        key = field["key"]
        label = field["label"]
        field_type = field["type"]

        tk.Label(popup, text=label).pack()

        if field_type == "entry":
            entry = tk.Entry(popup)
            entry.pack()
            entries[key] = entry
        elif field_type == "radio":
            frame = tk.Frame(popup)
            frame.pack()
        elif field_type == "text":
            entry = tk.Text(popup, height=8, width=50)
            entry.pack(pady=10)
            entries[key] = entry

            default = field.get("default", "")
            var = tk.StringVar(popup, value=default)

            for option in field["options"]:
                tk.Radiobutton(
                    frame,
                    text=option.title(),
                    variable=var,
                    value=option
                ).pack(anchor="w")
            entries[key] = var
    return popup, entries