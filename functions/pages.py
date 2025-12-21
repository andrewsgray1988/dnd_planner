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
    SPECIFIC_REGION_BUTTON_LABELS,
    CITY_BUTTON_LABELS,
    POI_BUTTON_LABELS,
    SHOP_BUTTON_LABELS
)
from text import (
    MAIN_PAGE_BODY_TEXT,
    MANAGE_PARTY_TEXT,
    BESTIARY_PAGE_TEXT,
    BESTIARY_PAGE_BODY_TEXT,
    GENERATORS_PAGE_TEXT,
    GENERATORS_PAGE_BODY_TEXT,
    SETTINGS_TEXT,
    REGIONS_TEXT,
)
from functions.general import (
    load_json,
    line_break,
    find_category,
    populate_info
)

def main_page(root, left_scroll_frame, right_scroll_frame):
    scroll_frame = initiate_page(root, left_scroll_frame, "Main Page")

    tk.Label(scroll_frame, text="Hello and welcome to the DnD Planner!", font=("Arial", 13)).pack(anchor="w")
    line_break(scroll_frame)

    tk.Label(scroll_frame, text="Navigation", font=("Arial", 18, "bold")).pack(anchor="w")
    line_break(scroll_frame)
    tk.Label(scroll_frame, text="Party and NPCs", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Manage party members and party NPCs, and those at camp.").pack(anchor="w")
    tk.Label(scroll_frame, text="Bestiary", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Manage creatures to enable combat generator.").pack(anchor="w")
    tk.Label(scroll_frame, text="Regions", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Manage regions and location info within the world.").pack(anchor="w")
    tk.Label(scroll_frame, text="Generators", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="A list of helpful generators for DnD sessions.").pack(anchor="w")
    tk.Label(scroll_frame, text="Settings", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Adjust settings for the program.").pack(anchor="w")
    tk.Label(scroll_frame, text="Close Program", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Closes the program.").pack(anchor="w")

    line_break(scroll_frame)

    initiate_buttons(root, left_scroll_frame, right_scroll_frame, MAIN_PAGE_BUTTON_LABELS)

def manage_party_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Manage Party Page")

    tk.Label(scroll_frame, text="Add Party Member", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Adds a party member to the active party.").pack(anchor="w")
    tk.Label(scroll_frame, text="Power is calculated based off Level (modified by settings), armor class, items, and automatically applied").pack(anchor="w")
    tk.Label(scroll_frame, text="Action count is calculated at 1 per class, 0.5 for bonus action (1 for monks.) Classes that get extra attacks gain an extra 1.").pack(anchor="w")
    tk.Label(scroll_frame, text="Active - Party member power will be considered for generated encounters.").pack(anchor="w")
    tk.Label(scroll_frame, text="Camp - Party member power will not be considered for generated encounters, and just stored until use.")
    tk.Label(scroll_frame, text="Update Party Member", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Updates a party member's information. This can be used to multi-class if you add a different class.").pack(anchor="w")
    tk.Label(scroll_frame, text="Delete Party Member", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Deletes a party member from the party. This is a permanent action and can't be undone.").pack(anchor="w")
    tk.Label(scroll_frame, text="Move Member", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Moves a party member to/from camp.").pack(anchor="w")
    line_break(scroll_frame)

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
        header_label = tk.Label(scroll_frame, text="Active Player Characters", font=("Arial", 12, "bold"), wraplength=scroll_frame.wrap_width)
        header_label.pack(pady=10)

        for member in party_data:
            classes_text = ", ".join([f"{cls['name']} {cls['level']}" for cls in member['classes']])
            member_text = f"{member['name']} - Combat Value: {member['combat_value']}, AC: {member['armor_class']}, Magic Item Count: {member['magic_items']}, Classes: {classes_text}"
            label = tk.Label(scroll_frame, text=member_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
            label.pack(fill="x", pady=2)

    if npc_data:
        header_label = tk.Label(scroll_frame, text="Active NPCs", font=("Arial", 12, "bold"), wraplength=scroll_frame.wrap_width)
        header_label.pack(pady=10)

        for member in npc_data:
            classes_text = ", ".join([f"{cls['name']} {cls['level']}" for cls in member['classes']])
            member_text = f"{member['name']} - Combat Value: {member['combat_value']}, AC: {member['armor_class']}, Magic Item Count: {member['magic_items']}, Classes: {classes_text}"
            label = tk.Label(scroll_frame, text=member_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
            label.pack(fill="x", pady=2)

    if inactive:
        header_label = tk.Label(scroll_frame, text="Characters at Camp", font=("Arial", 12, "bold"), wraplength=scroll_frame.wrap_width)
        header_label.pack(pady=10)

        for member in inactive:
            classes_text = ", ".join([f"{cls['name']} {cls['level']}" for cls in member['classes']])
            member_text = f"{member['name']} ({member['status']}) - Combat Value: {member['combat_value']}, AC: {member['armor_class']}, Magic Item Count: {member['magic_items']}, Classes: {classes_text}"
            label = tk.Label(scroll_frame, text=member_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
            label.pack(fill="x", pady=2)

    initiate_buttons(root, left_frame, right_frame, MANAGE_PARTY_BUTTON_LABELS)

def manage_bestiary_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Bestiary Page")

    tk.Label(scroll_frame, text="Add Monster", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Adds a monster to the bestiary").pack(anchor="w")
    tk.Label(scroll_frame, text="Required - Generators will use everything within the required first.").pack(anchor="w")
    tk.Label(scroll_frame, text="Random - Once filled with required, the generator will pull from random to compare against power/action count.").pack(anchor="w")
    tk.Label(scroll_frame, text="Archive - Creatures will not be used for generators, but stored for future use.").pack(anchor="w")
    tk.Label(scroll_frame, text="Delete Monster", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Deletes a party member from the bestiary. This is a permanent action and can't be undone.").pack(anchor="w")
    tk.Label(scroll_frame, text="Move Monster", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Moves a party member to/from camp.").pack(anchor="w")
    line_break(scroll_frame)

    required_data = load_json("required.json")
    random_data = load_json("random.json")
    archive_data = load_json("archive.json")

    header_label = tk.Label(scroll_frame, text="Required Encounters", font=("Arial", 12, "bold"), wraplength=scroll_frame.wrap_width)
    header_label.pack(pady=10)

    for creature in required_data:
        creature_text = f"{creature['name']} - Challenge Rating: {creature['challenge_rating']}, Actions: {creature['actions']}, Creature Count: {creature['count']}"
        label = tk.Label(scroll_frame, text=creature_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
        label.pack(fill="x", pady=2)

    header_label = tk.Label(scroll_frame, text="Random Encounters", font=("Arial", 12, "bold"), wraplength=scroll_frame.wrap_width)
    header_label.pack(pady=10)

    for creature in random_data:
        creature_text = f"{creature['name']} - Challenge Rating: {creature['challenge_rating']}, Actions: {creature['actions']}"
        label = tk.Label(scroll_frame, text=creature_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
        label.pack(fill="x", pady=2)

    header_label = tk.Label(scroll_frame, text="Archived Encounters", font=("Arial", 12, "bold"), wraplength=scroll_frame.wrap_width)
    header_label.pack(pady=10)

    for creature in archive_data:
        creature_text = f"{creature['name']} - Challenge Rating: {creature['challenge_rating']}, Actions: {creature['actions']}"
        label = tk.Label(scroll_frame, text=creature_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
        label.pack(fill="x", pady=2)

    initiate_buttons(root, left_frame, right_frame, MANAGE_BESTIARY_BUTTON_LABELS)

def generators_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Generators Page")

    placeholder_label = tk.Label(scroll_frame, text=GENERATORS_PAGE_BODY_TEXT, anchor="nw", justify="left", wraplength=scroll_frame.wrap_width)
    placeholder_label.pack(fill=tk.BOTH, expand=True)

    initiate_buttons(root, left_frame, right_frame, GENERATORS_BUTTON_LABELS)

def settings_page(root, left_frame, right_frame):
    scroll_frame = initiate_page(root, left_frame, "Settings Page", SETTINGS_TEXT)

    tk.Label(scroll_frame, text="Width and Height", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(scroll_frame, text="Adjusts base Width and Height. (This will only take effect after reload) ").pack(anchor="w")

    settings_data = load_json("settings.json")

    for key, value in settings_data.items():
        frame = tk.Frame(scroll_frame)
        frame.pack(fill="x", padx=5, pady=2)

        top_row = tk.Frame(frame)
        top_row.pack(fill="x")
        tk.Label(top_row, text=f"{key}:", width=15, anchor="w").pack(side="left")
        tk.Label(top_row, text=str(value), anchor="w").pack(side="left")

        if key == "Height":
            line_break(scroll_frame)
            tk.Label(scroll_frame, text="Buffers", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(scroll_frame, text="Adjusts encounter strength. Positive numbers make encounters harder, negative numbers make encounters easier").pack(anchor="w")
        if key == "Power Buffer":
            line_break(scroll_frame)
            tk.Label(scroll_frame, text="Modifiers", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(scroll_frame, text="Adjusts calculated powers of base classes. Custom/Homebrew classes fall under Custom.").pack(anchor="w")
    initiate_buttons(root, left_frame, right_frame, SETTINGS_BUTTON_LABELS)

def dynamic_page_loader(name, root, left_frame, right_frame):
    data = load_json("regions.json")
    if config.regions_flag is None and name != "Regions":
        return

    def remaining_layout():
        pass
    if name == "Regions":
        buttons = REGIONS_BUTTON_LABELS
        header = REGIONS_TEXT
        def remaining_layout():
            for region_name, region_data in data.items():
                region_label = tk.Label(scroll_frame, text=region_name, font=("Arial", 12, "bold"), anchor="nw", justify="left", wraplength=scroll_frame.wrap_width)
                region_label.pack(fill=tk.BOTH, expand=True)
                desc_label = tk.Label(scroll_frame, text=region_data["Description"], anchor="nw", justify="left",
                                      wraplength=scroll_frame.wrap_width)
                desc_label.pack(fill=tk.BOTH, expand=True, padx=(20, 0))
    elif config.regions_flag and name == config.regions_flag:
        buttons = SPECIFIC_REGION_BUTTON_LABELS
        region_name = config.nav_stack[-1]
        region_data = data[region_name]
        header = region_data["Description"]
        def remaining_layout():
            notes = region_data.get("Notes", [])
            if notes:
                populate_info(region_data, "Notes", "note", 20, scroll_frame)
            cities = region_data.get("Cities", [])
            if cities:
                populate_info(region_data, "Cities", "City", 20, scroll_frame)
            pois = region_data.get("Points Of Interest", [])
            if pois:
                populate_info(region_data, "Points Of Interest", "POI", 20, scroll_frame)
    else:
        if not config.regions_flag:
            return
        info_name = config.regions_flag
        result = find_category(name, {info_name: data[info_name]})
        info_type = result[0]
        region_data = data[info_name]
        item_data = None

        match info_type:
            case "City":
                _, item_data = result
                buttons = CITY_BUTTON_LABELS
                header = item_data.get("Description", "")

                def remaining_layout():
                    notes = item_data.get("Notes", [])
                    if notes:
                        populate_info(item_data, "Notes", "note", 20, scroll_frame)
                    if item_data.get("Places"):
                        populate_info(item_data, "Places", "Name", 20, scroll_frame)
                    if item_data.get("Shops"):
                        populate_info(item_data, "Shops", "Name", 20, scroll_frame)

            case "POI":
                _, item_data = result
                buttons = POI_BUTTON_LABELS
                header = item_data.get("Description", "")

                def remaining_layout():
                    notes = item_data.get("Notes", [])
                    if notes:
                        populate_info(item_data, "Notes", "note", 20, scroll_frame)
                    if item_data.get("Effects"):
                        populate_info(item_data, "Effects", "Name", 20, scroll_frame)
                    if item_data.get("People"):
                        populate_info(item_data, "People", "Name", 20, scroll_frame)

            case "Place":
                _, parent_city, place = result
                buttons = POI_BUTTON_LABELS
                header = place.get("Description", "")

                def remaining_layout():
                    notes = place.get("Notes", [])
                    if notes:
                        populate_info(place, "Notes", "note", 20, scroll_frame)
                    effects = place.get("Effects", [])
                    if effects:
                        populate_info(place, "Effects", "Name", 20, scroll_frame)
                    people = place.get("People", [])
                    if people:
                        populate_info(place, "People", "Name", 20, scroll_frame)

            case "Shop":
                _, parent_city, shop = result
                buttons = SHOP_BUTTON_LABELS
                header = shop.get("Description", "")

                def remaining_layout():
                    notes = shop.get("Notes", [])
                    if notes:
                        populate_info(shop, "Notes", "note", 20, scroll_frame)
                    inventory = shop.get("Inventory", [])
                    if inventory:
                        populate_info(shop, "Inventory", "Name", 20, scroll_frame)
                    people = shop.get("People", [])
                    if people:
                        populate_info(shop, "People", "Name", 20, scroll_frame)

    scroll_frame = initiate_page(root, left_frame, f"{name} Page", header)

    remaining_layout()

    initiate_buttons(root, left_frame, right_frame, buttons)
    generate_buttons(root, left_frame, right_frame)