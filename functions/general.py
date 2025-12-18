import os
import json
import tkinter as tk
import config

from models.player import Player
from tkinter import ttk, font

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

def line_break(frame):
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x', pady=10)

def find_category(name, data):
    region_name = config.regions_flag
    region = data.get(region_name)
    if not region:
        return None

    for city in region.get("Cities", []):
        if city.get("City") == name:
            return ("City", city)
        for place in city.get("Places", []):
            if place.get("Name") == name:
                return ("Place", city, place)
        for shop in city.get("Shops", []):
            if shop.get("Name") == name:
                return ("Shop", city, shop)

    for poi in region.get("Points Of Interest", []):
        if poi.get("POI") == name:
            return ("POI", poi)

    return ("Region", region)

def populate_info(data, section, subsection, pad, scroll_frame):
    inventory_flag = False
    if section == "Inventory":
        inventory_flag = True
    region_font = font.Font(size=12, weight="bold")
    header_text = str(section)
    count = 1
    header_label = tk.Label(scroll_frame, text=header_text, font=region_font, anchor="nw", justify="left")
    header_label.pack(fill=tk.BOTH, expand=True)
    if not inventory_flag:
        for d in data[section]:
            value = d.get(subsection, "Unnamed")
            ins_text = f'{count}: {value}'

            label = tk.Label(scroll_frame, text=ins_text, anchor="nw", justify="left")
            label.pack(fill=tk.BOTH, expand=True)

            desc = d.get("Description")
            if desc:
                desc_label = tk.Label(scroll_frame, text=desc, anchor="nw", justify="left", wraplength=500)
                desc_label.pack(fill=tk.BOTH, expand=True, padx=(pad, 0))
            count += 1
    else:
        for item in data.get(section, []):
            name = item.get("Name", "Unnamed")
            price = item.get("Price", "Unknown price")
            desc = item.get("Description", "")

            line_text = f"{count}: {name} - {price}"
            label = tk.Label(scroll_frame, text=line_text, anchor="nw", justify="left")
            label.pack(fill=tk.BOTH, expand=True)

            if desc:
                desc_label = tk.Label(scroll_frame, text=desc, anchor="nw", justify="left", wraplength=500)
                desc_label.pack(fill=tk.BOTH, expand=True, padx=(pad, 0))
            count += 1

def type_flags(name, data):
    regions_flag = config.regions_flag
    region_data = data.get(regions_flag)
    result = find_category(name, data)
    item_type = result[0]
    item_data = region_data

    match item_type:
        case "City":
            for city in region_data.get("Cities", []):
                if city.get("City") == name:
                    item_data = city
                    break
        case "POI":
            for poi in region_data.get("Points Of Interest", []):
                if poi.get("POI") == name:
                    item_data = poi
                    break
        case "Place":
            for city in region_data.get("Cities", []):
                for place in city.get("Places", []):
                    if place.get("Name") == name:
                        item_data = place
                        return item_data
        case "Shop":
            for city in region_data.get("Cities", []):
                for shop in city.get("Shops", []):
                    if shop.get("Name") == name:
                        item_data = shop
                        return item_data
        case _:
            pass

    return item_data

def recalculate_combat_values():
    from config import VALID_MAP
    for filename in ["party.json", "camp.json"]:
        data = load_json(filename)
        updated_data = []

        for p in data:
            player_obj = Player(p["name"], p["armor_class"], p["magic_items"], p.get("status", "Player"))

            for cls in p.get("classes", []):
                cls_name = cls["name"]
                cls_level = cls["level"]
                cls_lower = cls_name.lower()

                if cls_lower in VALID_MAP:
                    class_type = VALID_MAP[cls_lower]
                else:
                    from models.classes import CustomClass
                    class_type = (lambda name: lambda level: CustomClass(name, level))(cls_name)

                player_obj.add_class(class_type, cls_level)

            updated_data.append(player_obj.to_dict())

        save_json(filename, updated_data)

def check_unique(name, jsons, level, context, popup, parent_name=None):
    for json_file in jsons:
        data = load_json(json_file)

        if isinstance(data, dict):
            if level == "Region":
                if name in data:
                    show_error(f"Region '{name}' already exists.", popup)
                    return False

            elif level in ("city", "poi"):
                region = data.get(config.regions_flag)
                if not region:
                    return True

                for city in region.get("Cities", []):
                    if city.get("City") == name:
                        show_error(f"{name} already exists in this region.", popup)
                        return False

                for poi in region.get("Points Of Interest", []):
                    if poi.get("POI") == name:
                        show_error(f"{name} already exists in this region.", popup)
                        return False

            elif level in ("place", "shop"):
                result = find_category(parent_name, data)
                if not result or result[0] != "City":
                    return True

                city = result[1]

                for place in city.get("Places", []):
                    if place.get("Name") == name:
                        show_error(f"{name} already exists in {parent_name}.", popup)
                        return False

                for shop in city.get("Shops", []):
                    if shop.get("Name") == name:
                        show_error(f"{name} already exists in {parent_name}.", popup)
                        return False

        elif isinstance(data, list):
            for dat in data:
                if dat[context] == name:
                    show_error(f"{name} already exists.", popup)
                    return False
    return True