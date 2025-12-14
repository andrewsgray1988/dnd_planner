import config
import tkinter as tk

from models.monster import Monster
from models.player import Player
from models.classes import *
from models.region import *
from functions.general import (
    show_error,
    load_json,
    save_json,
    smart_title
)
from config import (
    VALID_CLASSES
)

def add_monster(root, left_frame=None, right_frame=None):
    #Initiates the pop-up
    popup = tk.Toplevel(root)
    popup.title(f"Add New Monster")

    instr_label = tk.Label(popup,
                           text="Adding a monster.\nFor Challenge Rating, please put either an integer or a decimal.\n(0.25 instead of 1/4)\nFor Actions, this is the number of (non-legendary action) attacks they get per round")
    instr_label.pack(pady=10)

    #Entry Values
    dest_label = tk.Label(popup, text="Destination:")
    dest_label.pack()
    dest_frame = tk.Frame(popup)
    dest_frame.pack()
    dest_entry = tk.StringVar(popup, value="required")
    for v in ["Required", "Random", "Archive"]:
        rb = tk.Radiobutton(
            dest_frame,
            text=v,
            variable=dest_entry,
            value=v.lower()
        )
        rb.pack(anchor="w")
    name_label = tk.Label(popup, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(popup)
    name_entry.pack()
    name_entry.focus_set()
    cr_label = tk.Label(popup, text="Challenge Rating:")
    cr_label.pack()
    cr_entry = tk.Entry(popup)
    cr_entry.pack()
    actions_label = tk.Label(popup, text="Actions:")
    actions_label.pack()
    actions_entry = tk.Entry(popup)
    actions_entry.pack()
    count_label = tk.Label(popup, text="Encounter Count (If going to Required):")
    count_label.pack()
    count_entry = tk.Entry(popup)
    count_entry.pack()

    def on_submit():
        #Gets the entered values
        name_val = name_entry.get().strip().title()
        cr_val = cr_entry.get()
        actions_val = actions_entry.get()
        count_val = count_entry.get()
        destination = dest_entry.get()

        #Checks if values are blank
        if destination != "required":
            for key, value in [("Name", name_val), ("Challenge Rating", cr_val), ("Actions", actions_val)]:
                if value.strip() == "":
                    show_error(f"Missing {key}", root)
                    return
        else:
            for key, value in [("Name", name_val), ("Challenge Rating", cr_val), ("Actions", actions_val), ("Count", count_val)]:
                if value.strip() == "":
                    show_error(f"Missing {key}", root)
                    return

        #Validates numbered entries and checks if they're correctly entered, then converts to int/float
        validation = [
            ("Actions", actions_val, int, "Actions must be a non-decimal number."),
            ("Challenge Rating", cr_val, float, "Challenge Rating must be a number."),
        ]
        if destination == "required":
            validation.append(("Count", count_val, int, "Count must be a non-decimal number."))
        converted = {}
        for key, value, cast, error_msg in validation:
            try:
                converted[key] = cast(value)
            except ValueError:
                show_error(error_msg, root)
                return

        #Double checks for duplicates
        monster_list = load_json(f"{destination}.json")
        for mon in monster_list:
            if mon["name"].lower() == name_val.lower():
                show_error(f"Monster already exists in {destination}", root)
                return

        #Creates the new monster class
        if destination == "required":
            new_monster = Monster(name_val, cr_val, actions_val, count_val)
        else:
            new_monster = Monster(name_val, cr_val, actions_val)
        new_monster.save_to_file(destination)

        #Closes popup and reloads page with new info
        popup.destroy()
        if left_frame and right_frame:
            from functions.pages import manage_bestiary_page
            manage_bestiary_page(root, left_frame, right_frame)

    #Command buttons
    tk.Button(popup, text="Submit", command=on_submit).pack(pady=10)
    tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def delete_monster(root, left_frame=None, right_frame=None):
    #Initiates the pop-up
    popup = tk.Toplevel(root)
    popup.title(f"Delete Monster")

    tk.Label(popup, text=f"Select from where").pack(pady=10)

    #Sets radio buttons to select where you want to send the monster to, detecting which
    valid_sources = ["required", "random", "archive"]
    source_var = tk.StringVar(value=valid_sources[0])

    source_frame = tk.Frame(popup)
    source_frame.pack()

    for loc in valid_sources:
        tk.Radiobutton(
            source_frame,
            text=loc.title(),
            variable=source_var,
            value=loc
        ).pack(anchor="w")

    def go_to_monster_selection():
        #Sets up the source (from) and delete previous pop-up. Checks if the source has any information to transfer
        source = source_var.get()
        for w in popup.winfo_children():
            w.destroy()

        monsters = load_json(f"{source}.json")
        if not monsters:
            show_error(f"No monsters found in {source}.", root)
            popup.destroy()
            return

        #Set up the next input to select transfer
        tk.Label(popup, text=f"Select a monster to move from {source.title()}:").pack(pady=10)

        monster_var = tk.StringVar(value=monsters[0]["name"])
        monster_frame = tk.Frame(popup)
        monster_frame.pack()

        for mon in monsters:
            tk.Radiobutton(
                monster_frame,
                text=mon["name"],
                variable=monster_var,
                value=mon["name"]
            ).pack(anchor="w")

        def finish_delete():
            #Verify chosen item
            chosen_name = monster_var.get()

            if not chosen_name:
                show_error("Please select a monster.", root)
                return

            #Remove the chosen item
            source_list = load_json(f"{source}.json")

            removed = next(
                (m for m in source_list if m["name"].lower() == chosen_name.lower()),
                None
            )

            source_list.remove(removed)
            save_json(f"{source}.json", source_list)

            #Clean up
            popup.destroy()
            show_error(f"{chosen_name} removed from {source}.", root)

            if left_frame and right_frame:
                from functions.pages import manage_bestiary_page
                manage_bestiary_page(root, left_frame, right_frame)
        #Button setup for final part of function
        tk.Button(popup, text="Confirm", command=finish_delete).pack(pady=10)
        tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=10)

        popup.grab_set()
        root.wait_window(popup)
    #Button setup for first part of the function
    tk.Button(popup, text="Next", command=go_to_monster_selection).pack(pady=10)
    tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def move_monster(root, to_location, left_frame=None, right_frame=None):
    #Setup initial popup
    popup = tk.Toplevel(root)
    popup.title(f"Move monster to {to_location}")

    tk.Label(popup, text=f"Select from where").pack(pady=10)

    #Set up from location
    valid_sources = [loc for loc in ("required", "random", "archive") if loc != to_location]
    source_var = tk.StringVar(value=valid_sources[0])

    source_frame = tk.Frame(popup)
    source_frame.pack()

    for loc in valid_sources:
        if loc == to_location:
            continue
        tk.Radiobutton(
            source_frame,
            text=loc.title(),
            variable=source_var,
            value=loc
        ).pack(anchor="w")

    def go_to_monster_selection():
        #Verify source selection and prepare next section
        source = source_var.get()

        if not source:
            show_error("Please select a source list.", root)
            return

        for w in popup.winfo_children():
            w.destroy()

        tk.Label(popup, text=f"Select a monster to move from {source.title()}:").pack(pady=10)

        monsters = load_json(f"{source}.json")

        if not monsters:
            popup.destroy()
            show_error("Chosen repository is empty.", root)
            return

        #Set up selection options
        monster_var = tk.StringVar(value=monsters[0]["name"])

        monster_frame = tk.Frame(popup)
        monster_frame.pack()

        for mon in monsters:
            tk.Radiobutton(
                monster_frame,
                text=mon["name"],
                variable=monster_var,
                value=mon["name"]
            ).pack(anchor="w")

        #Add Count if moving to Required
        if to_location == "required":
            tk.Label(popup, text="Encounter Count:").pack(pady=5)
            count_entry = tk.Entry(popup)
            count_entry.pack()

        def finish_transfer():
            chosen_name = monster_var.get()

            if not chosen_name:
                show_error("Please select a monster.", root)
                return

            source_list = load_json(f"{source}.json")

            transferred = next(
                (m for m in source_list if m["name"].lower() == chosen_name.lower()),
                None
            )

            if not transferred:
                show_error(f"{chosen_name} not found in {source}.", root)
                return

            if to_location == "required":
                try:
                    count_val = int(count_entry.get())
                except Exception:
                    show_error("Encounter must be a whole number.", root)
                    return
            else:
                count_val = None

            target_list = load_json(f"{to_location}.json")

            if any(m["name"].lower() == chosen_name.lower() for m in target_list):
                show_error(f"{chosen_name} already exists in {to_location}.", root)

            source_list.remove(transferred)
            save_json(f"{source}.json", source_list)

            new_mon = Monster(
                transferred["name"],
                transferred["challenge_rating"],
                transferred["actions"],
                count_val
            )

            temp_flag = config.bestiary_flag
            config.bestiary_flag = to_location
            new_mon.save_to_file(to_location)
            config.bestiary_flag = temp_flag

            popup.destroy()
            show_error(f"{chosen_name} moved from {source} to {to_location}.", root)

            if left_frame and right_frame:
                for widget in right_frame.winfo_children():
                    widget.destroy()
                from functions.pages import manage_bestiary_page
                manage_bestiary_page(root, left_frame, right_frame)

        tk.Button(popup, text="Transfer", command=finish_transfer).pack(pady=10)
        tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=10)

        popup.grab_set()
        root.wait_window(popup)

    tk.Button(popup, text="Next", command=go_to_monster_selection).pack(pady=10)
    tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def adjust_setting(root, left_frame=None, right_frame=None):
    popup = tk.Toplevel(root)
    popup.title("Adjust Settings")

    settings_data = load_json("settings.json")
    entry_widgets = {}

    instr_label = tk.Label(
        popup,
        text="Adjust settings below.\nModify any value and click Submit to save changes."
    )
    instr_label.pack(pady=10)

    container = tk.Frame(popup)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    form_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=form_frame, anchor="nw")

    form_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    for setting, value in settings_data.items():
        row = tk.Frame(form_frame)
        row.pack(fill="x", pady=2)

        label = tk.Label(row, text=f"{setting}:", width=20, anchor="w")
        label.pack(side="left", padx=5)

        entry = tk.Entry(row)
        entry.pack(side="left", fill="x", expand=True, padx=5)
        entry.insert(0, str(value))

        entry_widgets[setting] = entry

    def on_submit():
        new_values = {}

        for setting, entry in entry_widgets.items():
            raw = entry.get().strip()

            if raw == "":
                show_error(f"{setting} cannot be empty.", root)
                return

            try:
                if "." in raw:
                    new_values[setting] = float(raw)
                else:
                    new_values[setting] = int(raw)
            except ValueError:
                show_error(f"Value for {setting} must be a number.", root)
                return

        save_json("settings.json", new_values)
        popup.destroy()

        if left_frame and right_frame:
            from functions.pages import settings_page
            settings_page(root, left_frame, right_frame)

    def on_cancel():
        popup.destroy()

    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=10)

    submit_btn = tk.Button(btn_frame, text="Submit", command=on_submit)
    submit_btn.pack(side="left", padx=10)

    cancel_btn = tk.Button(btn_frame, text="Cancel", command=on_cancel)
    cancel_btn.pack(side="left", padx=10)

    popup.grab_set()
    root.wait_window(popup)

def add_member(root, left_frame=None, right_frame=None):
    popup = tk.Toplevel(root)
    popup.title("Add New Party Member")

    instr_label = tk.Label(popup, text="Please enter the character's details.\nIf the character is multi-classed, put one\nand then use Update Member to add other classes.")
    instr_label.pack(pady=10)

    def on_submit():
        name_val = name_entry.get().strip().title()
        status_val = status_var.get()
        ac_val = ac_entry.get()
        magic_items_val = items_entry.get()
        class_val = class_entry.get().strip().title()
        level_val = level_entry.get()

        class_val_input = class_val.lower()
        valid_map = {
            "artificer": Artificer,
            "barbarian": Barbarian,
            "bard": Bard,
            "cleric": Cleric,
            "druid": Druid,
            "fighter": Fighter,
            "monk": Monk,
            "paladin": Paladin,
            "ranger": Ranger,
            "rogue": Rogue,
            "sorcerer": Sorcerer,
            "warlock": Warlock,
            "wizard": Wizard,
        }

        for key, value in [("Name", name_val), ("Armor Class", ac_val), ("Magic Items", magic_items_val), ("Class", class_val), ("Level", level_val)]:
            if value.strip() == "":
                show_error("Missing a Value.", root)
                return
        try:
            ac_val = int(ac_val)
            magic_items_val = int(magic_items_val)
            level_val = int(level_val)
        except ValueError:
            show_error("Armor Class, Magic Items, and Level must be non-decimal number.", root)
            return

        if class_val_input not in valid_map:
            show_error(f"Invalid class. Must be one of: {', '.join(VALID_CLASSES)} (Not case sensitive).", root)
            return

        class_obj = valid_map[class_val_input]

        players_list = load_json("party.json")
        for player in players_list:
            if player["name"] == name_val:
                show_error("Player already exists in party.", root)
                return

        new_player = Player(name_val, ac_val, magic_items_val, status_val)
        new_player.add_class(class_obj, level_val)
        new_player.get_combat_value()
        new_player.get_action_count()
        new_player.save_to_file()

        popup.destroy()

        if left_frame and right_frame:
            from functions.pages import manage_party_page
            manage_party_page(root, left_frame, right_frame)

    def on_cancel():
        popup.destroy()

    name_label = tk.Label(popup, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(popup)
    name_entry.pack()
    name_entry.focus_set()
    status_label = tk.Label(popup, text="Status:")
    status_label.pack()
    status_var = tk.StringVar(value="Player")  # default is Player
    player_radio = tk.Radiobutton(popup, text="Player", variable=status_var, value="Player")
    player_radio.pack()
    npc_radio = tk.Radiobutton(popup, text="NPC", variable=status_var, value="NPC")
    npc_radio.pack()
    ac_label = tk.Label(popup, text="Armor Class:")
    ac_label.pack()
    ac_entry = tk.Entry(popup)
    ac_entry.pack()
    items_label = tk.Label(popup, text="Combat Magic Item Count:")
    items_label.pack()
    items_entry = tk.Entry(popup)
    items_entry.pack()
    class_label = tk.Label(popup, text="Character Class:")
    class_label.pack()
    class_entry = tk.Entry(popup)
    class_entry.pack()
    level_label = tk.Label(popup, text="Class Level:")
    level_label.pack()
    level_entry = tk.Entry(popup)
    level_entry.pack()
    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def delete_member(root, left_frame=None, right_frame=None):
    popup = tk.Toplevel(root)
    popup.title("Delete Party Member")

    instr_label = tk.Label(popup, text="Please type the name of the character you wish to delete.\nThis is a permanent action, and they will have to be added again if needed!")
    instr_label.pack(pady=10)

    players_list = load_json("party.json")
    camp_list = load_json("camp.json")
    button_list = players_list + camp_list

    if not button_list:
        show_error("No players available.", root)
        return

    def on_submit():
        name_val = name_entry.get()

        found = False
        for player in players_list:
            if player["name"].lower() == name_val.lower():
                players_list.remove(player)
                save_json("party.json", players_list)
                popup.destroy()

                if left_frame and right_frame:
                    from functions.pages import manage_party_page
                    manage_party_page(root, left_frame, right_frame)
                found = True
                break

        if not found:
            for player in camp_list:
                if player["name"].lower() == name_val.lower():
                    camp_list.remove(player)
                    save_json("camp.json", camp_list)
                    popup.destroy()

                    if left_frame and right_frame:
                        from functions.pages import manage_party_page
                        manage_party_page(root, left_frame, right_frame)
                    found = True
                    break

            if not found:
                show_error(f"{name_val} not found in current party.", root)
                return

    def on_cancel():
        popup.destroy()

    name_label = tk.Label(popup, text="Name:")
    name_label.pack()
    names_frame = tk.Frame(popup)
    names_frame.pack()
    name_entry = tk.StringVar(popup)
    name_entry.set(button_list[0])

    for player in button_list:
        rb = tk.Radiobutton(
            names_frame,
            text=player["name"],
            variable=name_entry,
            value=player["name"]
        )
        rb.pack(anchor="w")
    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def update_member(root, left_frame=None, right_frame=None):
    popup = tk.Toplevel(root)
    popup.title("Update Party Member")

    instr_label = tk.Label(popup, text="Which character would you like to update, and what?\nIf adding a multiclass, you can input that here under the Character Class and Level.\nIf a section does not need to be updated, it can be left blank!")
    instr_label.pack(pady=10)

    players_list = load_json("party.json")
    camp_list = load_json("camp.json")
    button_list = players_list + camp_list

    if not button_list:
        show_error("No characters in party or camp.", root)
        return

    def on_submit():
        name_val = name_entry.get().strip().title()
        status_val = status_var.get()
        ac_val = ac_entry.get()
        magic_items_val = items_entry.get()
        class_val = class_entry.get().strip().title()
        level_val = level_entry.get()

        valid_map = {
            "artificer": Artificer,
            "barbarian": Barbarian,
            "bard": Bard,
            "cleric": Cleric,
            "druid": Druid,
            "fighter": Fighter,
            "monk": Monk,
            "paladin": Paladin,
            "ranger": Ranger,
            "rogue": Rogue,
            "sorcerer": Sorcerer,
            "warlock": Warlock,
            "wizard": Wizard,
        }

        if class_val:
            class_val_input = class_val.lower()
            if class_val_input not in valid_map:
                show_error(f"Invalid class. Must be one of: {', '.join(VALID_CLASSES)} (Not case sensitive).", root)
                return
            class_obj = valid_map[class_val_input]
        else:
            class_obj = None

        found = False
        for player in players_list:
            if player["name"].lower() == name_val.lower():
                found = True
                player_update = Player(name_val, player["armor_class"], player["magic_items"])
                for cls in player["classes"]:
                    class_type = valid_map[cls["name"].lower()]
                    player_update.add_class(class_type, cls["level"])
                    player_update.status = status_val
                if ac_val:
                    try:
                        player_update.armor_class = int(ac_val)
                    except ValueError:
                        show_error("Armor Class must be a number.", root)
                        return
                if magic_items_val:
                    try:
                        player_update.magic_items = int(magic_items_val)
                    except ValueError:
                        show_error("Magic Items must be a number.", root)
                        return
                if (class_val and not level_val) or (level_val and not class_val):
                    show_error("If updating Class, both Class and Level must be provided.", root)
                    return
                if class_val and level_val:
                    existing_classes = [cls.name.lower() for cls in player_update.classes]
                    class_val_lower = class_val.lower()
                    if class_val_lower in existing_classes:
                        player_update.update_class_level(class_val, int(level_val))
                    else:
                        player_update.add_class(class_obj, int(level_val))

                players_list.remove(player)
                players_list.append(player_update.to_dict())

                save_json("party.json", players_list)

                popup.destroy()

                if left_frame and right_frame:
                    from functions.pages import manage_party_page
                    manage_party_page(root, left_frame, right_frame)
                break

        if not found:

            found = False
            for player in camp_list:
                if player["name"].lower() == name_val.lower():
                    found = True
                    player_update = Player(name_val, player["armor_class"], player["magic_items"])
                    for cls in player["classes"]:
                        class_type = valid_map[cls["name"].lower()]
                        player_update.add_class(class_type, cls["level"])
                        player_update.status = status_val
                    if ac_val:
                        try:
                            player_update.armor_class = int(ac_val)
                        except ValueError:
                            show_error("Armor Class must be a number.", root)
                            return
                    if magic_items_val:
                        try:
                            player_update.magic_items = int(magic_items_val)
                        except ValueError:
                            show_error("Magic Items must be a number.", root)
                            return
                    if (class_val and not level_val) or (level_val and not class_val):
                        show_error("If updating Class, both Class and Level must be provided.", root)
                        return
                    if class_val and level_val:
                        existing_classes = [cls.name.lower() for cls in player_update.classes]
                        class_val_lower = class_val.lower()
                        if class_val_lower in existing_classes:
                            player_update.update_class_level(class_val, int(level_val))
                        else:
                            player_update.add_class(class_obj, int(level_val))

                    camp_list.remove(player)
                    camp_list.append(player_update.to_dict())

                    save_json("camp.json", camp_list)

                    popup.destroy()

                    if left_frame and right_frame:
                        from functions.pages import manage_party_page
                        manage_party_page(root, left_frame, right_frame)
                    break

            if not found:
                show_error(f"No player named '{name_val}' found in party.", root)
                return

    def on_cancel():
        popup.destroy()


    name_label = tk.Label(popup, text="Name:")
    name_label.pack()
    names_frame = tk.Frame(popup)
    names_frame.pack()
    name_entry = tk.StringVar(popup)
    name_entry.set(button_list[0])

    for player in button_list:
        rb = tk.Radiobutton(
            names_frame,
            text=player["name"],
            variable=name_entry,
            value=player
        )
        rb.pack(anchor="w")
    status_label = tk.Label(popup, text="Status:")
    status_label.pack()
    status_var = tk.StringVar(value="Player")
    player_radio = tk.Radiobutton(popup, text="Player", variable=status_var, value="Player")
    player_radio.pack()
    npc_radio = tk.Radiobutton(popup, text="NPC", variable=status_var, value="NPC")
    npc_radio.pack()
    ac_label = tk.Label(popup, text="Armor Class:")
    ac_label.pack()
    ac_entry = tk.Entry(popup)
    ac_entry.pack()
    items_label = tk.Label(popup, text="Combat Magic Item Count:")
    items_label.pack()
    items_entry = tk.Entry(popup)
    items_entry.pack()
    class_label = tk.Label(popup, text="Character Class:")
    class_label.pack()
    class_entry = tk.Entry(popup)
    class_entry.pack()
    level_label = tk.Label(popup, text="Class Level:")
    level_label.pack()
    level_entry = tk.Entry(popup)
    level_entry.pack()
    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def move_member(root, left_frame=None, right_frame=None):
    if config.party_flag == "Active":
        from_var = "Active"
        to_var = "Camp"
        from_json = "party.json"
        to_json = "camp.json"
    else:
        from_var = "Camp"
        to_var = "Active"
        from_json = "camp.json"
        to_json = "party.json"

    party_list_from = load_json(from_json)
    party_list_to = load_json(to_json)

    if not party_list_from:
        show_error(f"No characters found in {from_var}", root)
        return

    popup = tk.Toplevel(root)
    popup.title(f"Move character from {from_var} to {to_var}")

    tk.Label(popup, text=f"Please type the name of the character you wish to move to {to_var}.").pack(
        pady=10)

    name_label = tk.Label(popup, text="Name:")
    name_label.pack()
    names_frame = tk.Frame(popup)
    names_frame.pack()
    name_entry = tk.StringVar(popup)
    name_entry.set(party_list_from[0])

    for player in party_list_from:
        rb = tk.Radiobutton(
            names_frame,
            text=player["name"],
            variable=name_entry,
            value=player["name"]
        )
        rb.pack(anchor="w")

    def on_submit():
        name_val = name_entry.get()

        temp_char = None
        for char in party_list_from:
            if char["name"].lower() == name_val.lower():
                temp_char = char
                party_list_from.remove(char)

        party_list_to.append(temp_char)

        save_json(from_json, party_list_from)
        save_json(to_json, party_list_to)

        popup.destroy()
        show_error(f"{name_val} has been moved to {to_var}", root)

        if left_frame and right_frame:
            from functions.pages import manage_party_page
            manage_party_page(root, left_frame, right_frame)

    tk.Button(popup, text="Submit", command=on_submit).pack(pady=10)
    tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def add_new_region(root, left_frame=None, right_frame=None):
    popup = tk.Toplevel(root)
    popup.title("Adding New Region")

    instr_label = tk.Label(popup,text="Name the New Region")
    instr_label.pack(pady=10)

    def on_submit():
        name_val = name_entry.get().strip().title()

        if not name_val:
            show_error("Please add a name to continue.", root)
            return

        regions_dict = load_json("regions.json")

        if name_val in regions_dict:
            show_error("Region already exists.", root)
            return

        region = Region(name_val)
        region.save_to_file()

        popup.destroy()

        if left_frame and right_frame:
            from functions.pages import regions_base_page
            regions_base_page(root, left_frame, right_frame)

    def on_cancel():
        popup.destroy()

    name_label = tk.Label(popup, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(popup)
    name_entry.pack()
    name_entry.focus_set()
    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def remove_region(root, left_frame=None, right_frame=None):
    popup = tk.Toplevel(root)
    popup.title("Delete Region")

    instr_label = tk.Label(popup,
                           text="Select which region you wish to delete.\nThis is a permanent action, and will delete ALL information included in that region!")
    instr_label.pack(pady=10)

    regions = load_json("regions.json")

    if not regions:
        show_error("No regions available to delete.", root)
        return

    def on_submit():
        name_val = name_entry.get()

        if name_val not in regions:
            show_error("Region does not exist.", root)
            return

        del regions[name_val]
        save_json("regions.json", regions)
        popup.destroy()

        if left_frame and right_frame:
            from functions.pages import regions_base_page
            regions_base_page(root, left_frame, right_frame)

    def on_cancel():
        popup.destroy()

    first_region = next(iter(regions))

    name_label = tk.Label(popup, text="Choose a Region:")
    name_label.pack()
    names_frame = tk.Frame(popup)
    names_frame.pack()
    name_entry = tk.StringVar(popup)
    name_entry.set(first_region)

    for region_name in regions:
        rb = tk.Radiobutton(
            names_frame,
            text=region_name,
            variable=name_entry,
            value=region_name
        )
        rb.pack(anchor="w")
    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def add_note(section, root, left_frame=None, right_frame=None):
    popup = tk.Toplevel(root)
    popup.title(f"Add {section} Note")

    instr_label = tk.Label(popup, text=f"Add Note to {section}")
    instr_label.pack(pady=10)

    text_box = tk.Text(popup, height=8, width=50)
    text_box.pack(pady=10)

    def on_submit():
        note_text = text_box.get("1.0", tk.END).strip()
        if not note_text:
            show_error("Please insert a note.", root)
            return

        if config.last_flag == "Regions":
            region_name = section
        else:
            region_name = config.last_flag

        region = Region.load_from_file(region_name)
        target_name = section

        if target_name == region_name:
            region.add_note(note_text)
        else:
            pass
        popup.destroy()

        if left_frame and right_frame:
            from functions.pages import dynamic_page_loader
            label = config.button_flag
            dynamic_page_loader(label, root, left_frame, right_frame)

    def on_cancel():
        popup.destroy()

    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)
    
def delete_note(section, root, left_frame=None, right_frame=None):
    if config.last_flag == "Regions":
        region_name = section
    else:
        region_name = config.last_flag

    region = Region.load_from_file(region_name)

    if section == region_name:
        notes = region.notes
    else:
        notes = []
        for city in region.cities:
            if city.name == section:
                notes = city.notes
                break
        for poi in region["POI"]:
            if poi.name == section:
                notes = poi.notes
                break

    if not notes:
        show_error("No notes found.", root)
        return

    popup = tk.Toplevel(root)
    popup.title(f"Delete {section} note.")

    instr_label = tk.Label(popup, text=f"Delete Note from {section}")
    instr_label.pack(pady=10)

    def on_submit():
        target_name = section
        note_to_delete = note_id.get()

        if target_name == region_name:
            region.delete_note(note_to_delete)

            popup.destroy()
            if left_frame and right_frame:
                from functions.pages import dynamic_page_loader
                label = config.button_flag
                dynamic_page_loader(label, root, left_frame, right_frame)
            return
        return

    def on_cancel():
        popup.destroy()

    note_frame = tk.Frame(popup)
    note_frame.pack(pady=10)

    note_id = tk.IntVar(popup)
    note_id.set(notes[0]["id"])

    for note in notes:
        rb = tk.Radiobutton(
            note_frame,
            text=f"{note['id']}",
            variable=note_id,
            value=note['id']
        )
        rb.pack(anchor="w")


    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def add_type(section, section_type, root, left_frame=None, right_frame=None):
    type_map = {
        "city": City,
        "poi": PointOfInterest
    }

    if section_type not in type_map:
        show_error(f"Unknown section type: {section_type}", root)
        return

    ChildClass = type_map[section_type]
    descrip = section_type if section_type != "poi" else "point of interest"

    popup = tk.Toplevel(root)
    popup.title(f"Add {descrip} to {section}")

    instr_label = tk.Label(popup, text=f"Add {descrip} to {section}")
    instr_label.pack(pady=10)

    name_label = tk.Label(popup, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(popup)
    name_entry.pack()
    name_entry.focus_set()

    def on_submit():
        name_val = smart_title(name_entry.get())
        if not name_val:
            show_error("Please insert a name.", root)
            return

        region = Region.load_from_file(section)

        child_obj = ChildClass(name_val)

        if section_type == "city":
            region.add_city(child_obj)
        elif section_type == "poi":
            region.add_poi(child_obj)

        region.save_to_file()

        popup.destroy()

        if left_frame and right_frame:
            from functions.pages import dynamic_page_loader
            label = config.button_flag
            dynamic_page_loader(label, root, left_frame, right_frame)

    def on_cancel():
        popup.destroy()

    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def remove_type(section, section_type, root, left_frame=None, right_frame=None):
    type_map = {
        "city": {
            "label": "city",
            "list_attr": "cities",
            "delete": "delete_city"
        },
        "poi": {
            "label": "point of interest",
            "list_attr": "poi",
            "delete": "delete_poi"
        }
    }

    if section_type not in type_map:
        show_error(f"Unknown section type: {section_type}", root)
        return

    cfg = type_map[section_type]

    region = Region.load_from_file(section)
    locations = getattr(region, cfg['list_attr'])

    if not locations:
        show_error(f"No locations found for {section}", root)
        return

    popup = tk.Toplevel(root)
    popup.title(f"Remove {cfg['label']} from {section}")

    instr_label = tk.Label(popup,
                           text=f"Select which {cfg['label']} you wish to delete.\nThis is a permanent action, and will delete ALL information included in that region!")
    instr_label.pack(pady=10)

    region = Region.load_from_file(section)
    locations = getattr(region, cfg['list_attr'])

    name_var = tk.StringVar(popup)
    name_var.set(locations[0].name)

    names_frame = tk.Frame(popup)
    names_frame.pack(pady=10)

    for loc in locations:
        rb = tk.Radiobutton(
            names_frame,
            text=loc.name,
            variable=name_var,
            value=loc.name
        )
        rb.pack(anchor="w")

    def on_submit():
        delete_func = getattr(region, cfg['delete'])
        delete_func(name_var.get())

        popup.destroy()

        if left_frame and right_frame:
            from functions.pages import dynamic_page_loader
            dynamic_page_loader(config.button_flag, root, left_frame, right_frame)

    def on_cancel():
        popup.destroy()

    submit_btn = tk.Button(popup, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)

def reset_settings(root, left_frame=None, right_frame=None):
    popup = tk.Toplevel(root)
    popup.title("Default Settings Confirmation")

    instr_label = tk.Label(popup, text="This will reset Buffers to 0 and Classes to 1.\nPlease confirm.")
    instr_label.pack(pady=10)

    def on_submit():
        data = load_json("settings.json")
        data["Action Buffer"] = "0"
        data["Power Buffer"] = "0"
        data["Artificer"] = "1"
        data["Barbarian"] = "1"
        data["Bard"] = "1"
        data["Cleric"] = "1"
        data["Druid"] = "1"
        data["Fighter"] = "1"
        data["Monk"] = "1"
        data["Paladin"] = "1"
        data["Ranger"] = "1"
        data["Rogue"] = "1"
        data["Sorcerer"] = "1"
        data["Warlock"] = "1"
        data["Wizard"] = "1"
        save_json("settings.json", data)

        if left_frame and right_frame:
            from functions.pages import settings_page
            settings_page(root, left_frame, right_frame)
        popup.destroy()

    def on_cancel():
        popup.destroy()

    submit_btn = tk.Button(popup, text="Confirm", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)

    popup.grab_set()
    root.wait_window(popup)