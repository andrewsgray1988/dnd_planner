import os
import json
import tkinter as tk
import config

from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
JSON_DIR = "jsons"

def load_json(file):
    with open(os.path.join(BASE_DIR, JSON_DIR, file)) as json_file:
        return json.load(json_file)

def save_json(file, data):
    full_path = os.path.join(BASE_DIR, JSON_DIR, file)
    with open(full_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def find_number(str_pull):
    num_pull = int("".join(filter(str.isdigit, str_pull)))
    return num_pull

def close_program(root, left_frame=None, right_frame=None):
    root.destroy()

def clear_data(root, left_frame, right_frame):
    popup = tk.Toplevel(root)
    popup.title("Clear Data Confirmation")

    instr_label = tk.Label(popup, text=f"This will delete all {config.clear_flag} data.\nPlease confirm.")
    instr_label.pack(pady=10)

    def on_submit():
        if config.clear_flag == "party" or config.clear_flag == "of your non-setting":
            save_json("party.json", [])
        if config.clear_flag == "bestiary" or config.clear_flag == "of your non-setting":
            save_json("random.json", [])
            save_json("required.json", [])
            save_json("archive.json", [])
        popup.destroy()

    def on_cancel():
        popup.destroy()

    submit_btn = tk.Button(popup, text="Confirm", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

def get_challenge_rating(root):
    popup = tk.Toplevel(root)
    popup.title("Enter Challenge Rating")

    tk.Label(popup, text="Challenge Rating:").pack(pady=5)

    entry = tk.Entry(popup)
    entry.pack(pady=5)
    entry.focus()

    result = {"value": None}

    def submit():
        val = entry.get().strip()
        if not val.isdigit():
            show_error("Value must be an integer", root)
            return
        result["value"] = int(val)
        popup.destroy()

    tk.Button(popup, text="OK", command=submit).pack(pady=10)
    tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

    return result["value"]

def show_error(msg, root):
    error_popup = tk.Toplevel(root)
    error_popup.title("Message")
    error_popup.resizable(False, False)

    error_label = tk.Label(error_popup, text=msg, padx=10, pady=10)
    error_label.pack(pady=10)

    okay_btn = tk.Button(error_popup, text="OK", command=error_popup.destroy)
    okay_btn.pack(pady=10)

    error_popup.grab_set()
    root.wait_window(error_popup)

def navigate_to(page_name):
    if not config.nav_stack or config.nav_stack[-1] != page_name:
        config.nav_stack.append(page_name)
    config.back_flag = page_name

def go_back():
    if len(config.nav_stack) > 1:
        config.nav_stack.pop()
        return config.nav_stack[-1]
    return "Main"

def line_break(frame):
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x', pady=10)

def find_category(name, data):
    for region_name, region in data.items():

        for city in region.get("Cities", []):
            if city.get("City") == name:
                return "City"

        for poi in region.get("POI", []):
            if poi.get("Point of Interest") == name:
                return "POI"

        for note in region.get("Notes", []):
            if note.get("note") == name:
                return "Note"

    return None  # Not found