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

class SafeEntry:
    def __init__(self, entry_widget):
        self.entry = entry_widget
    def get(self):
        value = self.entry.get().strip()
        if value.startswith("__CMD__:"):
            value = value.removeprefix("__CMD__:")

        words = value.split()
        result = []
        for word in words:
            if word.lower().endswith("'s"):
                result.append(word[:-2].capitalize() + "'s")
            else:
                result.append(word.capitalize())
        return " ".join(result)

    def insert(self, value):
        self.entry.insert(0, value)

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
        scroll_frame.wrap_width = event.width - 20

    canvas.bind("<Configure>", match_width)

    scroll_frame.wrap_width = 500
    return scroll_frame

def initiate_page(root, left_scroll_frame, header_text, placeholder_text=None):
    clear_widgets(left_scroll_frame)

    header_label = tk.Label(left_scroll_frame, text=header_text, font=("Arial", 22, "bold"))
    header_label.pack(pady=10)

    line_break(left_scroll_frame)
    return left_scroll_frame

def initiate_buttons(root, left_scroll_frame, right_scroll_frame, labels):
    from functions.onclick import on_button_click

    clear_widgets(right_scroll_frame)

    for label in labels:
        if label != "Line Break":
            if label.startswith("Label:"):
                text = label[len("Label:"):].strip()
                # Header labels can be title-cased for UI only
                lbl = tk.Label(
                    right_scroll_frame,
                    text=text.title(),
                    anchor="center",
                    justify="center",
                    font=("Arial", 12, "bold")
                )
                lbl.pack(fill="x", pady=2)
            else:
                display_name = label      # What the user sees
                actual_name = f"__CMD__:{label}"       # Exact string from JSON, preserves case
                btn = tk.Button(
                    right_scroll_frame,
                    text=display_name,
                    command=lambda n=actual_name: on_button_click(n, root, left_scroll_frame, right_scroll_frame)
                )
                btn.pack(**BUTTON_PACK_OPTIONS)
        else:
            line_break(right_scroll_frame)
    line_break(right_scroll_frame)
    return right_scroll_frame


def generate_buttons(root, left_scroll_frame, right_scroll_frame):
    from functions.onclick import on_button_click
    data = load_json("regions.json")
    items_to_list = []

    current_name = config.nav_stack[-1]

    # ---------- Regions ----------
    if current_name == "Regions" and data:
        items_to_list.append("Label: Regions")
        items_to_list += list(data.keys())

    # ---------- Cities and POIs ----------
    elif len(config.nav_stack) >= 2 and config.nav_stack[-2] == "Regions":
        current = data.get(current_name)
        if not current:
            return  # No data

        cities = current.get("Cities", [])
        if cities:
            items_to_list.append("Label: Cities")
            items_to_list += [c["City"] for c in cities]
            items_to_list.append("Line Break")

        pois = current.get("Points Of Interest", [])
        if pois:
            items_to_list.append("Label: Points of Interest")
            items_to_list += [p["POI"] for p in pois]
            items_to_list.append("Line Break")

    # ---------- Places and Shops ----------
    elif len(config.nav_stack) >= 3 and config.nav_stack[-3] == "Regions":
        region_name = config.regions_flag
        region = data.get(region_name)
        if not region:
            return

        result = find_category(current_name, {region_name: region})
        item_type = result[0]
        if item_type == "City":
            current = next((c for c in region.get("Cities", []) if c["City"] == current_name), None)
            if not current:
                return

            places = current.get("Places", [])
            if places:
                items_to_list.append("Label: Places")
                items_to_list += [p["Name"] for p in places]
                items_to_list.append("Line Break")

            shops = current.get("Shops", [])
            if shops:
                items_to_list.append("Label: Shops")
                items_to_list += [s["Name"] for s in shops]
                items_to_list.append("Line Break")

    # ---------- Create buttons ----------
    for label in items_to_list:
        if label != "Line Break":
            if label.startswith("Label:"):
                text = label[len("Label:"):].strip()
                lbl = tk.Label(
                    right_scroll_frame,
                    text=text.title(),  # UI-only title
                    anchor="center",
                    justify="center",
                    font=("Arial", 12, "bold")
                )
                lbl.pack(fill="x", pady=2)
            else:
                display_name = label  # UI shows exactly what user entered
                actual_name = label   # preserve casing for logic
                btn = tk.Button(
                    right_scroll_frame,
                    text=display_name,
                    command=lambda n=actual_name: on_button_click(n, root, left_scroll_frame, right_scroll_frame)
                )
                btn.pack(fill=tk.X, padx=5, pady=5)
        else:
            line_break(right_scroll_frame)

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
            entries[key] = SafeEntry(entry)
        elif field_type == "radio":
            frame = tk.Frame(popup)
            frame.pack()
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
        elif field_type == "radionum":
            frame = tk.Frame(popup)
            frame.pack()
            var = tk.IntVar(popup, value=field.get("default"))

            for option in field["options"]:
                tk.Radiobutton(
                    frame,
                    text=str(option),
                    variable=var,
                    value=option
                ).pack(anchor="w")
            entries[key] = var
        elif field_type == "text":
            entry = tk.Text(popup, height=8, width=50)
            entry.pack(pady=10)
            entries[key] = entry

    return popup, entries