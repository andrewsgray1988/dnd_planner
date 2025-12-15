import config
import tkinter as tk

from functions.gui import (
    initiate_page,
    initiate_buttons,
    generate_buttons,
)
from config import (
    MAIN_PAGE_BUTTON_LABELS,
    MANAGE_PARTY_BUTTON_LABELS,
    MANAGE_BESTIARY_BUTTON_LABELS,
    GENERATORS_BUTTON_LABELS,
    SETTINGS_BUTTON_LABELS,
    REGIONS_BUTTON_LABELS,
    SPECIFIC_REGION_BUTTON_LABELS
)
from text import (
    MAIN_PAGE_TEXT,
    MAIN_PAGE_BODY_TEXT,
    MANAGE_PARTY_TEXT,
    BESTIARY_PAGE_TEXT,
    BESTIARY_PAGE_BODY_TEXT,
    GENERATORS_PAGE_TEXT,
    GENERATORS_PAGE_BODY_TEXT,
    SETTINGS_TEXT,
    REGIONS_TEXT,
    REGIONS_BODY_TEXT
)
from functions.general import (
    load_json,
    line_break,
    find_category
)

def main_page(root, left_scroll_frame, right_scroll_frame):
    scroll_frame = initiate_page(root, left_scroll_frame, "Main Page", MAIN_PAGE_TEXT)

    placeholder_label = tk.Label(scroll_frame, text=MAIN_PAGE_BODY_TEXT, anchor="nw", justify="left")
    placeholder_label.pack(fill=tk.BOTH, expand=True)

    line_break(scroll_frame)

    initiate_buttons(root, left_scroll_frame, right_scroll_frame, MAIN_PAGE_BUTTON_LABELS)

def manage_party_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Manage Party Page", MANAGE_PARTY_TEXT)

    pre_sort = load_json("party.json")
    inactive = load_json("camp.json")
    party_data = []
    npc_data = []

    for char in pre_sort:
        if char["status"] == "Player":
            party_data.append(char)
        elif char["status"] == "NPC":
            npc_data.append(char)

    if party_data:
        header_label = tk.Label(scroll_frame, text="Active Player Characters", font=("Arial", 12, "bold"))
        header_label.pack(pady=10)

        for member in party_data:
            classes_text = ", ".join([f"{cls['name']} {cls['level']}" for cls in member['classes']])
            member_text = f"{member['name']} - Combat Value: {member['combat_value']}, AC: {member['armor_class']}, Magic Item Count: {member['magic_items']}, Classes: {classes_text}"
            label = tk.Label(scroll_frame, text=member_text, anchor="w", justify="left")
            label.pack(fill="x", pady=2)

    if npc_data:
        header_label = tk.Label(scroll_frame, text="Active NPCs", font=("Arial", 12, "bold"))
        header_label.pack(pady=10)

        for member in npc_data:
            classes_text = ", ".join([f"{cls['name']} {cls['level']}" for cls in member['classes']])
            member_text = f"{member['name']} - Combat Value: {member['combat_value']}, AC: {member['armor_class']}, Magic Item Count: {member['magic_items']}, Classes: {classes_text}"
            label = tk.Label(scroll_frame, text=member_text, anchor="w", justify="left")
            label.pack(fill="x", pady=2)

    if inactive:
        header_label = tk.Label(scroll_frame, text="Characters at Camp", font=("Arial", 12, "bold"))
        header_label.pack(pady=10)

        for member in inactive:
            classes_text = ", ".join([f"{cls['name']} {cls['level']}" for cls in member['classes']])
            member_text = f"{member['name']} ({member['status']}) - Combat Value: {member['combat_value']}, AC: {member['armor_class']}, Magic Item Count: {member['magic_items']}, Classes: {classes_text}"
            label = tk.Label(scroll_frame, text=member_text, anchor="w", justify="left")
            label.pack(fill="x", pady=2)

    initiate_buttons(root, left_frame, right_frame, MANAGE_PARTY_BUTTON_LABELS)

def manage_bestiary_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Bestiary Page", BESTIARY_PAGE_TEXT)

    placeholder_label = tk.Label(scroll_frame, text=BESTIARY_PAGE_BODY_TEXT, anchor="nw", justify="left")
    placeholder_label.pack(fill="x", pady=5)

    required_data = load_json("required.json")
    random_data = load_json("random.json")
    archive_data = load_json("archive.json")

    header_label = tk.Label(scroll_frame, text="Required Encounters", font=("Arial", 12, "bold"))
    header_label.pack(pady=10)

    for creature in required_data:
        creature_text = f"{creature['name']} - Challenge Rating: {creature['challenge_rating']}, Actions: {creature['actions']}, Creature Count: {creature['count']}"
        label = tk.Label(scroll_frame, text=creature_text, anchor="w", justify="left")
        label.pack(fill="x", pady=2)

    header_label = tk.Label(scroll_frame, text="Random Encounters", font=("Arial", 12, "bold"))
    header_label.pack(pady=10)

    for creature in random_data:
        creature_text = f"{creature['name']} - Challenge Rating: {creature['challenge_rating']}, Actions: {creature['actions']}"
        label = tk.Label(scroll_frame, text=creature_text, anchor="w", justify="left")
        label.pack(fill="x", pady=2)

    header_label = tk.Label(scroll_frame, text="Archived Encounters", font=("Arial", 12, "bold"))
    header_label.pack(pady=10)

    for creature in archive_data:
        creature_text = f"{creature['name']} - Challenge Rating: {creature['challenge_rating']}, Actions: {creature['actions']}"
        label = tk.Label(scroll_frame, text=creature_text, anchor="w", justify="left")
        label.pack(fill="x", pady=2)

    initiate_buttons(root, left_frame, right_frame, MANAGE_BESTIARY_BUTTON_LABELS)

def generators_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Generators Page", GENERATORS_PAGE_TEXT)

    placeholder_label = tk.Label(scroll_frame, text=GENERATORS_PAGE_BODY_TEXT, anchor="nw", justify="left")
    placeholder_label.pack(fill=tk.BOTH, expand=True)

    initiate_buttons(root, left_frame, right_frame, GENERATORS_BUTTON_LABELS)

def settings_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Settings Page", SETTINGS_TEXT)

    first_line = tk.Label(scroll_frame, text="Width/Height placeholder", anchor="w", justify="left")
    first_line.pack(fill="x", padx=15)

    settings_data = load_json("settings.json")

    for key, value in settings_data.items():
        frame = tk.Frame(scroll_frame)
        frame.pack(fill="x", padx=5, pady=2)

        top_row = tk.Frame(frame)
        top_row.pack(fill="x")
        tk.Label(top_row, text=f"{key}:", width=15, anchor="w").pack(side="left")
        tk.Label(top_row, text=str(value), anchor="w").pack(side="left")

        if key == "Height":
            tk.Label(frame, text="Buffer placeholder", anchor="w").pack(fill="x", padx=15)
        if key == "Power Buffer":
            tk.Label(frame, text="Class placeholder", anchor="w").pack(fill="x", padx=15)
    initiate_buttons(root, left_frame, right_frame, SETTINGS_BUTTON_LABELS)

def regions_base_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Regions Page", REGIONS_TEXT)

    placeholder_label = tk.Label(scroll_frame, text=REGIONS_BODY_TEXT, anchor="nw", justify="left")
    placeholder_label.pack(fill=tk.BOTH, expand=True)

    initiate_buttons(root, left_frame, right_frame, REGIONS_BUTTON_LABELS)
    generate_buttons(root, left_frame, right_frame)

def dynamic_page_loader(name, root, left_frame, right_frame):
    data = load_json("regions.json")
    if config.nav_stack[-1] == "Regions":
        item_type = None
        region_data = data[name]
    elif config.nav_stack[-2] == "Regions":
        item_type = find_category(name, data)
        pass
    elif config.nav_stack[-3] == "Regions":
        item_type = find_category(name, data)
        region_name = config.nav_stack[-2]
        if item_type == "City":
            region_data = next(c for c in data[region_name]["Cities"] if c["City"] == name)
        elif item_type == "POI":
            region_data = next(p for p in data[region_name]["POI"] if p["Point of Interest"] == name)

    scroll_frame = initiate_page(root, left_frame, f"{name} Page", "")

    notes = region_data.get("Notes", [])
    notes_label = tk.Label(scroll_frame, text="Notes:", font=("Arial", 10, "bold"))
    notes_label.pack(anchor="w", pady=(10, 2))

    if notes:
        for note in notes:
            tk.Label(scroll_frame, text=f"{note['id']}. {note['note']}").pack(anchor="w", padx=10)

    if not item_type:
        cities = region_data.get("Cities", [])
        cities_label = tk.Label(scroll_frame, text="Cities:", font=("Arial", 10, "bold"))
        cities_label.pack(anchor="w", pady=(10, 2))

        if cities:
            for city in cities:
                tk.Label(scroll_frame, text=f"{city.get('City', 'Unnamed City')}").pack(anchor="w", padx=10)

        points = region_data.get("POI", [])
        points_label = tk.Label(scroll_frame, text="Points of Interest:", font=("Arial", 10, "bold"))
        points_label.pack(anchor="w", pady=(10, 2))

        if points:
            for point in points:
                tk.Label(scroll_frame, text=f"{point.get('Point of Interest', 'Unnamed POI')}").pack(anchor="w", padx=10)

        initiate_buttons(root, left_frame, right_frame, SPECIFIC_REGION_BUTTON_LABELS)
    elif item_type == "City":
        pass

    generate_buttons(root, left_frame, right_frame)