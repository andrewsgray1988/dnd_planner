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
    find_category,
    type_flags,
    recalculate_combat_values,
    check_unique,
    validate_and_convert
)
from functions.gui import (
    create_scrollable_frame,
    submit_buttons,
    close_popup_and_refresh,
    initiate_popup
)
from config import (
    VALID_CLASSES,
    VALID_MAP
)

def add_monster(root, left_frame=None, right_frame=None):
    #Initiates the pop-up
    popup_title = "Add New Monster"
    popup_label = "Adding a monster.\nFor Challenge Rating, please put either an integer or a decimal.\n(0.25 instead of 1/4)\nFor Actions, this is the number of (non-legendary action) attacks they get per round"
    popup_fields = [
        {
            "key": "dest",
            "label": "Destination:",
            "type": "radio",
            "options": ["required", "random", "archive"],
            "default": "required"
        },
        {
            "key": "name",
            "label": "Name:",
            "type": "entry"
        },
        {
            "key": "cr",
            "label": "Challenge Rating:",
            "type": "entry"
        },
        {
            "key": "actions",
            "label": "Actions:",
            "type": "entry"
        },
        {
            "key": "count",
            "label": "Encounter Count (If going to Required):",
            "type": "entry"
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        #Gets the entered values
        name_val = values["name"].get().strip().title()
        cr_val = values["cr"].get()
        actions_val = values["actions"].get()
        count_val = values["count"].get()
        destination = values["dest"].get()

        if destination == "required":
            validation_list = [(name_val, str, "Name"), (cr_val, int, "Challenge Rating"), (actions_val, int, "Actions"), (count_val, int, "Encounter Count"), (destination, str, "Destination")]
            checked = validate_and_convert(validation_list, root)
            if not checked:
                return
            name_val, cr_val, actions_val, count_val, destination = checked
        else:
            validation_list = [(name_val, str), (cr_val, int), (actions_val, int), (destination, str)]
            checked = validate_and_convert(validation_list, True, root)
            if not checked:
                return
            name_val, cr_val, actions_val, destination = checked

        #Double checks for duplicates
        flag = check_unique(name_val, ("archive.json", "required.json", "random.json"), None, "name", popup)

        if flag:
            #Creates the new monster class
            if destination == "required":
                new_monster = Monster(name_val, cr_val, actions_val, count_val)
            else:
                new_monster = Monster(name_val, cr_val, actions_val)
            new_monster.save_to_file(destination)

            #Closes popup and reloads page with new info
            from functions.pages import manage_bestiary_page
            close_popup_and_refresh(popup, root, left_frame, right_frame, manage_bestiary_page)

    #Command buttons
    submit_buttons(root, popup, "Confirm", on_submit)

def delete_monster(root, left_frame=None, right_frame=None):
    #Initiates the pop-up
    popup_title = "Delete Monster"
    popup_label = "Select from where"
    popup_fields = [
        {
            "key": "source",
            "label": "Source:",
            "type": "radio",
            "options": ["required", "random", "archive"],
            "default": "required"
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def go_to_monster_selection():
        #Sets up the source (from) and delete previous pop-up. Checks if the source has any information to transfer
        source = values["source"].get()
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
            from functions.pages import manage_bestiary_page
            close_popup_and_refresh(popup, root, left_frame, right_frame, manage_bestiary_page)
            show_error(f"{chosen_name} removed from {source}.", root)

        #Button setup for final part of function
        submit_buttons(root, popup, "Confirm", finish_delete)
    #Button setup for first part of the function
    submit_buttons(root, popup, "Next", go_to_monster_selection)

def move_monster(root, to_location, left_frame=None, right_frame=None):
    #Setup initial popup
    # Initiates the pop-up
    valid_sources = [loc for loc in ("required", "random", "archive") if loc != to_location]
    popup_title = f"Move monster to {to_location}"
    popup_label = "Select from where"
    popup_fields = [
        {
            "key": "source",
            "label": "Source:",
            "type": "radio",
            "options": valid_sources,
            "default": valid_sources[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def go_to_monster_selection():
        #Verify source selection and prepare next section
        source = values["source"].get()
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
            #Check for monster entry
            chosen_name = monster_var.get()

            if not chosen_name:
                show_error("Please select a monster.", root)
                return

            #Check for transfer list
            source_list = load_json(f"{source}.json")

            transferred = next(
                (m for m in source_list if m["name"].lower() == chosen_name.lower()),
                None
            )

            if not transferred:
                show_error(f"{chosen_name} not found in {source}.", root)
                return

            #If moving to required, add the count
            if to_location == "required":
                try:
                    count_val = int(count_entry.get())
                except Exception:
                    show_error("Encounter must be a whole number.", root)
                    return
            else:
                count_val = None

            #Check for duplicates
            target_list = load_json(f"{to_location}.json")

            if any(m["name"].lower() == chosen_name.lower() for m in target_list):
                show_error(f"{chosen_name} already exists in {to_location}.", root)

            #Remove the creature from the source list
            source_list.remove(transferred)
            save_json(f"{source}.json", source_list)

            #Add the creature to the transfer source
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

            #Cleanup and reload page
            from functions.pages import manage_bestiary_page
            close_popup_and_refresh(popup, root, left_frame, right_frame, manage_bestiary_page)
            show_error(f"{chosen_name} moved from {source} to {to_location}.", root)

        #Command buttons for the second part of the functions
        submit_buttons(root, popup, "Submit", finish_transfer)

    #Command buttons for the first part of the function
    submit_buttons(root, popup, "Next", go_to_monster_selection)

def adjust_setting(root, left_frame=None, right_frame=None):
    #Load the popup for the function
    popup_title = "Adjust Settings"
    popup_label = "Adjust settings below.\nModify any value and click Submit to save changes."
    popup, _ = initiate_popup(root, popup_title, popup_label, None)

    settings_data = load_json("settings.json")
    entry_widgets = {}


    #Fill the frame with the settings
    for setting, value in settings_data.items():
        row = tk.Frame(popup)
        row.pack(fill="x", pady=2)

        label = tk.Label(row, text=f"{setting}:", width=20, anchor="w")
        label.pack(side="left", padx=5)

        entry = tk.Entry(row)
        entry.pack(side="left", fill="x", expand=True, padx=5)
        entry.insert(0, str(value))

        entry_widgets[setting] = entry

    def on_submit():
        #Update settings
        new_values = {}

        for setting, entry in entry_widgets.items():
            raw = entry.get().strip()

            #Catch any that are empty
            if raw == "":
                show_error(f"{setting} cannot be empty.", root)
                return

            #Will convert appropriately to float or int
            try:
                if "." in raw:
                    new_values[setting] = float(raw)
                else:
                    new_values[setting] = int(raw)
            except ValueError:
                show_error(f"Value for {setting} must be a number.", root)
                return

        #Cleanup and reset page
        save_json("settings.json", new_values)
        recalculate_combat_values()
        from functions.pages import settings_page
        close_popup_and_refresh(popup, root, left_frame, right_frame, settings_page)
        popup.destroy()

    submit_buttons(root, popup, "Submit", on_submit)

def add_member(root, left_frame=None, right_frame=None):
    #Initiate popup and create entry
    popup_title = "Add New Party Member"
    popup_label = "Please enter the character's details.\nIf the character is multi-classed, put one\nand then use Update Member to add other classes."
    popup_fields = [
        {
            "key": "name",
            "label": "Name:",
            "type": "entry"
        },
        {
            "key": "status",
            "label": "Status:",
            "type": "radio",
            "options": ["Player", "NPC"],
            "default": "Player"
        },
        {
            "key": "ac",
            "label": "Armor Class:",
            "type": "entry"
        },
        {
            "key": "items",
            "label": "Combat Magic Item Count",
            "type": "entry"
        },
        {
            "key": "class",
            "label": "Character Class:",
            "type": "entry"
        },
        {
            "key": "level",
            "label": "Class Level:",
            "type": "entry"
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        name_val = values["name"].get().strip().title()
        status_val = values["status"].get()
        ac_val = values["ac"].get()
        magic_items_val = values["items"].get()
        class_val = values["class"].get().strip().title()
        level_val = values["level"].get()

        class_val_input = class_val.lower()

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

        if class_val_input in VALID_MAP:
            class_obj = VALID_MAP[class_val_input]
        else:
            class_obj = lambda level: CustomClass(class_val, level)

        flag = check_unique(name_val, ("party.json", "camp.json"), None, "name", popup)

        if flag:
            new_player = Player(name_val, ac_val, magic_items_val, status_val)
            new_player.add_class(class_obj, level_val)
            new_player.get_combat_value()
            new_player.get_action_count()
            new_player.save_to_file()

            from functions.pages import manage_party_page
            close_popup_and_refresh(popup, root, left_frame, right_frame, manage_party_page)
            popup.destroy()

    submit_buttons(root, popup, "Submit", on_submit)

def delete_member(root, left_frame=None, right_frame=None):
    # Initiate popup and create entry
    players_list = load_json("party.json")
    camp_list = load_json("camp.json")
    button_list = [p["name"] for p in players_list] + [c["name"] for c in camp_list]

    if not button_list:
        show_error("No players available.", root)
        return

    popup_title = "Delete Party Member"
    popup_label = "Please type the name of the character you wish to delete.\nThis is a permanent action, and they will have to be added again if needed!"
    popup_fields = [
        {
            "key": "name",
            "label": "Name:",
            "type": "radio",
            "options": button_list,
            "default": button_list[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        name_val = values["name"].get()

        found = False
        for player in players_list:
            if player["name"].lower() == name_val.lower():
                players_list.remove(player)
                save_json("party.json", players_list)
                from functions.pages import manage_party_page
                close_popup_and_refresh(popup, root, left_frame, right_frame, manage_party_page)
                found = True
                break

        if not found:
            for player in camp_list:
                if player["name"].lower() == name_val.lower():
                    camp_list.remove(player)
                    save_json("camp.json", camp_list)
                    from functions.pages import manage_party_page
                    close_popup_and_refresh(popup, root, left_frame, right_frame, manage_party_page)
                    break

            if not found:
                show_error(f"{name_val} not found in current party.", root)
                return

    submit_buttons(root, popup, "Submit", on_submit)

def update_member(root, left_frame=None, right_frame=None):
    players_list = load_json("party.json")
    camp_list = load_json("camp.json")
    button_list = [p["name"] for p in players_list] + [c["name"] for c in camp_list]

    if not button_list:
        show_error("No characters in party or camp.", root)
        return
    popup_title = "Update Party Member"
    popup_label = "Which character would you like to update, and what?\nIf adding a multiclass, you can input that here under the Character Class and Level.\nIf a section does not need to be updated, it can be left blank!"
    popup_fields = [
        {
            "key": "name",
            "label": "Name:",
            "type": "radio",
            "options": button_list,
            "default": button_list[0]
        },
        {
            "key": "status",
            "label": "Status:",
            "type": "radio",
            "options": ["Player", "NPC"],
            "default": "Player"
        },
        {
            "key": "ac",
            "label": "Armor Class:",
            "type": "entry"
        },
        {
            "key": "items",
            "label": "Combat Magic Item Count",
            "type": "entry"
        },
        {
            "key": "class",
            "label": "Character Class:",
            "type": "entry"
        },
        {
            "key": "level",
            "label": "Class Level:",
            "type": "entry"
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        name_val = values["name"].get().strip().title()
        status_val = values["status"].get()
        ac_val = values["ac"].get()
        magic_items_val = values["items"].get()
        class_val = values["class"].get().strip().title()
        level_val = values["level"].get()

        if class_val:
            class_val_input = class_val.lower()
            if class_val_input not in VALID_MAP:
                show_error(f"Invalid class. Must be one of: {', '.join(VALID_CLASSES)} (Not case sensitive).", root)
                return
            class_obj = VALID_MAP[class_val_input]
        else:
            class_obj = None

        found = False
        for player in players_list:
            if player["name"].lower() == name_val.lower():
                found = True
                player_update = Player(name_val, player["armor_class"], player["magic_items"])
                for cls in player["classes"]:
                    class_name_lower = cls["name"].lower()
                    if class_name_lower in VALID_MAP:
                        class_type = VALID_MAP[class_name_lower]
                    else:
                        class_type = lambda level: CustomClass(cls["name"], level)
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
                if class_val:
                    class_val_lower = class_val.lower()
                    if not level_val or int(level_val) == 0:
                        player_update.classes = [cls for cls in player_update.classes if cls.name.lower() != class_val_lower]
                    else:
                        if class_val_lower in [cls.name.lower() for cls in player_update.classes]:
                            player_update.update_class_level(class_val, level_val)
                        else:
                            player_update.add_class(class_obj, level_val)

                players_list.remove(player)
                players_list.append(player_update.to_dict())

                save_json("party.json", players_list)

                from functions.pages import manage_party_page
                close_popup_and_refresh(popup, root, left_frame, right_frame, manage_party_page)
                break

        if not found:
            found = False
            for player in camp_list:
                if player["name"].lower() == name_val.lower():
                    found = True
                    player_update = Player(name_val, player["armor_class"], player["magic_items"])
                    for cls in player["classes"]:
                        class_name_lower = cls["name"].lower()
                        if class_name_lower in VALID_MAP:
                            class_type = VALID_MAP[class_name_lower]
                        else:
                            # Use a lambda so add_class works the same way as other classes
                            class_type = lambda level: CustomClass(cls["name"], level)
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

                    from functions.pages import manage_party_page
                    close_popup_and_refresh(popup, root, left_frame, right_frame, manage_party_page)
                    break
            if not found:
                show_error(f"No player named '{name_val}' found in party.", root)
                return

    submit_buttons(root, popup, "Submit", on_submit)

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

    party_list_from_raw = load_json(from_json)
    party_list_from = [p["name"] for p in party_list_from_raw]
    party_list_to = load_json(to_json)

    if not party_list_from:
        show_error(f"No characters found in {from_var}", root)
        return

    popup_title = f"Move character from {from_var} to {to_var}"
    popup_label = f"Please type the name of the character you wish to move to {to_var}."
    popup_fields = [
        {
            "key": "name",
            "label": "Name:",
            "type": "radio",
            "options": party_list_from,
            "default": party_list_from[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        name_val = values["name"].get()

        temp_char = None
        for char in party_list_from_raw:
            if char["name"].lower() == name_val.lower():
                temp_char = char
                party_list_from_raw.remove(char)

        party_list_to.append(temp_char)

        save_json(from_json, party_list_from_raw)
        save_json(to_json, party_list_to)

        from functions.pages import manage_party_page
        close_popup_and_refresh(popup, root, left_frame, right_frame, manage_party_page)
        show_error(f"{name_val} has been moved to {to_var}", root)

    submit_buttons(root, popup, "Submit", on_submit)

def add_new_region(root, left_frame=None, right_frame=None):
    popup_title = "Adding New Region"
    popup_label = "Name the New Region"
    popup_fields = [
        {
            "key": "name",
            "label": "Name:",
            "type": "entry"
        },
        {
            "key": "description",
            "label": "Description:",
            "type": "text"
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        name_val = values["name"].get().strip().title()
        desc_val = values["description"].get("1.0", tk.END).strip()

        if not name_val:
            show_error("Please add a name to continue.", root)
            return

        flag = check_unique(name_val, ("regions.json",), "Region", None, popup)

        if flag:
            region = Region(name_val, desc_val)
            region.save_to_file()

            from functions.pages import dynamic_page_loader
            close_popup_and_refresh(popup, root, left_frame, right_frame,
                                    lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))

    submit_buttons(root, popup, "Submit", on_submit)

def remove_region(root, left_frame=None, right_frame=None):
    regions = load_json("regions.json")
    if not regions:
        show_error("No regions available to delete.", root)
        return
    regions_list = list(regions.keys())

    popup_title = "Delete Region"
    popup_label = "Select which region you wish to delete.\nThis is a permanent action, and will delete ALL information included in that region!"
    popup_fields = [
        {
            "key": "name",
            "label": "Choose a Region:",
            "type": "radio",
            "options": regions_list,
            "default": regions_list[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        name_val = values["name"].get()

        if name_val not in regions:
            show_error("Region does not exist.", root)
            return

        del regions[name_val]
        save_json("regions.json", regions)

        from functions.pages import dynamic_page_loader
        close_popup_and_refresh(popup, root, left_frame, right_frame,
                                lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))

    submit_buttons(root, popup, "Submit", on_submit)

def add_note(section, root, left_frame=None, right_frame=None):
    data = load_json("regions.json")
    item_data = type_flags(section, data)

    popup_title = f"Add {section} Note"
    popup_label = f"Add Note to {section}"
    popup_fields = [
        {
            "key": "note",
            "label": "Please insert a note.",
            "type": "text",
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        note_text = values["note"].get("1.0", tk.END).strip()
        if not note_text:
            show_error("Please insert a note.", root)
            return

        note_id = len(item_data["Notes"]) + 1
        item_data["Notes"].append({"id": note_id, "note": note_text})
        save_json("regions.json", data)

        from functions.pages import dynamic_page_loader
        close_popup_and_refresh(popup, root, left_frame, right_frame,
                                lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))

    submit_buttons(root, popup, "Submit", on_submit)

def update_note(section, root, left_frame=None, right_frame=None):
    data = load_json("regions.json")
    item_data = type_flags(section, data)

    notes = item_data.get("Notes", [])
    if not notes:
        show_error("No notes found.", root)
        return

    note_ids = [note["id"] for note in notes]

    popup_title = f"Delete {section} note."
    popup_label = f"Delete Note from {section}"
    popup_fields = [
        {
            "key": "note_id",
            "label": "Please select a note.",
            "type": "radionum",
            "options": note_ids,
            "default": note_ids[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def note_selected():
        selected_id = values["note_id"].get()
        current_note = next((n for n in item_data.get("Notes", []) if n["id"] == selected_id), None)

        note_text = current_note["note"]
        for w in popup.winfo_children():
            w.destroy()

        tk.Label(popup, text="Update note").pack(pady=10)

        text_widget = tk.Text(popup, height=8, width=50)
        text_widget.pack(pady=10)
        text_widget.insert("1.0", note_text)

        def on_submit():
            text_info = text_widget.get("1.0", tk.END).strip()
            for note in item_data.get("Notes", []):
                if note["id"]== selected_id:
                    note["note"] = text_info
                    break

            save_json("regions.json", data)
            from functions.pages import dynamic_page_loader
            close_popup_and_refresh(popup, root, left_frame, right_frame,
                                    lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))

        submit_buttons(root, popup, "Submit", on_submit)
    submit_buttons(root, popup, "Select Note", note_selected)

def delete_note(section, root, left_frame=None, right_frame=None):
    data = load_json("regions.json")
    item_data = type_flags(section, data)

    notes = item_data.get("Notes", [])
    if not notes:
        show_error("No notes found.", root)
        return

    note_ids = [note["id"] for note in notes]

    popup_title = f"Delete {section} note."
    popup_label = f"Delete Note from {section}"
    popup_fields = [
        {
            "key": "note_id",
            "label": "Please select a note.",
            "type": "radionum",
            "options": note_ids,
            "default": note_ids[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        note_to_delete = values["note_id"].get()

        item_data["Notes"] = [n for n in notes if n["id"] != note_to_delete]

        for i, note in enumerate(item_data["Notes"], start=1):
            note["id"] = i

        save_json("regions.json", data)

        from functions.pages import dynamic_page_loader
        label = config.button_flag
        close_popup_and_refresh(popup, root, left_frame, right_frame,
                                lambda r, lf, rf: dynamic_page_loader(label, r, lf, rf))

    submit_buttons(root, popup, "Submit", on_submit)

def add_location(section, section_type, root, left_frame=None, right_frame=None):
    type_map = {
        "city": City,
        "poi": PointOfInterest
    }

    if section_type not in type_map:
        show_error(f"Unknown section type: {section_type}", root)
        return

    ChildClass = type_map[section_type]
    descrip = section_type if section_type != "poi" else "point of interest"

    popup_title = f"Add {descrip} to {section}"
    popup_label = f"Add {descrip} to {section}"
    popup_fields = [
        {
            "key": "name",
            "label": "Name:",
            "type": "entry",
        },
        {
            "key": "info",
            "label": "Description:",
            "type": "text",
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        name_val = values["name"].get()
        desc_text = values["info"].get("1.0", tk.END).strip()
        if not name_val:
            show_error("Please insert a name.", root)
            return
        elif not desc_text:
            show_error("Please insert a description.", root)
            return

        flag = check_unique(name_val, ("regions.json",), section_type, None, popup)

        if flag:
            region = Region.load_from_file(section)

            child_obj = ChildClass(name_val)
            child_obj.update_description(desc_text)

            if section_type == "city":
                region.add_city(child_obj)
            elif section_type == "poi":
                region.add_poi(child_obj)

            region.save_to_file()
            from functions.pages import dynamic_page_loader
            close_popup_and_refresh(popup, root, left_frame, right_frame,
                                    lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))

    submit_buttons(root, popup, "Submit", on_submit)

def remove_location(section, section_type, root, left_frame=None, right_frame=None):
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

    location_names = [loc.name for loc in locations]
    popup_title = f"Remove {cfg['label']} from {section}"
    popup_label = f"Select which {cfg['label']} you wish to delete.\nThis is a permanent action, and will delete ALL information included in that region!"
    popup_fields = [
        {
            "key": "name",
            "label": f"Select {cfg['label']} to delete:",
            "type": "radio",
            "options": location_names,
            "default": location_names[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    region = Region.load_from_file(section)

    def on_submit():
        delete_func = getattr(region, cfg['delete'])
        delete_func(values["name"].get())

        from functions.pages import dynamic_page_loader
        close_popup_and_refresh(popup, root, left_frame, right_frame,
                                lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))
        popup.destroy()

    submit_buttons(root, popup, "Submit", on_submit)

def reset_settings(root, left_frame=None, right_frame=None):
    popup_title = "Default Settings Confirmation"
    popup_label = "This will reset Buffers to 0 and Classes to 1.\nPlease confirm."
    popup, values = initiate_popup(root, popup_title, popup_label, None)

    def on_submit():
        data = load_json("settings.json")
        data["Action Buffer"] = 0
        data["Power Buffer"] = 0
        data["Artificer"] = 1
        data["Barbarian"] = 1
        data["Bard"] = 1
        data["Cleric"] = 1
        data["Druid"] = 1
        data["Fighter"] = 1
        data["Monk"] = 1
        data["Paladin"] = 1
        data["Ranger"] = 1
        data["Rogue"] = 1
        data["Sorcerer"] = 1
        data["Warlock"] = 1
        data["Wizard"] = 1
        data["Custom"] = 1
        save_json("settings.json", data)

        recalculate_combat_values()
        from functions.pages import settings_page
        close_popup_and_refresh(popup, root, left_frame, right_frame, settings_page)
    submit_buttons(root, popup, "Confirm", on_submit)

def update_description(name, root, left_frame=None, right_frame=None):
    data = load_json("regions.json")
    item_data = type_flags(name, data)
    result = find_category(name, data)
    item_type = result[0]
    match item_type:
        case "Region":
            item_data = result[1]
            current_name = item_data.get("Region", "")
        case "City":
            item_data = result[1]
            current_name = item_data.get("City", "")
        case "POI":
            item_data = result[1]
            current_name = item_data.get("POI", "")
        case "Place" | "Shop":
            item_data = result[2]
            current_name = item_data.get("Name", "")
    current_description = item_data.get("Description", "")

    popup_title = f"Update {name}'s description"
    popup_label = f"Update {name}'s description"
    popup_fields = [
        {
            "key": "name",
            "label": "Name:",
            "type": "entry"
        },
        {
            "key": "description",
            "label": "Description:",
            "type": "text",
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)
    name_widget = values.get("name")
    if name_widget:
        name_widget.insert(current_name)
    desc_widget = values.get("description")
    if desc_widget:
        desc_widget.insert("1.0", current_description)
        desc_widget.mark_set("insert", "1.0")

    def on_submit():
        new_text = desc_widget.get("1.0", tk.END).strip()
        if not new_text:
            show_error("Please insert a description.", root)
            return

        item_data["Description"] = new_text
        save_json("regions.json", data)

        from functions.pages import dynamic_page_loader
        close_popup_and_refresh(
            popup, root, left_frame, right_frame,
            lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf)
        )

    submit_buttons(root, popup, "Update", on_submit)

def add_feature(section, feature_type, root, left_frame=None, right_frame=None):
    data = load_json("regions.json")
    item_data = type_flags(section, data)
    inventory_flag = False
    if feature_type == "inventory":
        inventory_flag = True

    popup_title = f"Add {feature_type} to {section}"
    popup_label = f"Add Note to {section}"
    popup_fields = [
        {
            "key": "name",
            "label": f"Name the {feature_type}:",
            "type": "entry",
        },
        {
            "key": "description",
            "label": "Description:",
            "type": "text"
        }
    ]
    if inventory_flag:
        popup_fields.append({
            "key": "price",
            "label": "Price:",
            "type": "entry"
        })
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)
    def on_submit():
        name_val = values["name"].get().strip().title()
        desc_val = values["description"].get("1.0", tk.END).strip()
        if inventory_flag:
            price_val = values["price"].get().strip().title()

        if not name_val or not desc_val:
            show_error("Please insert a name and description.", root)
            return

        parent_name = config.nav_stack[-1]
        flag = check_unique(name_val, ("regions.json",), feature_type, None, popup, parent_name)

        if flag:
            match feature_type:
                case "shop":
                    item_data.setdefault("Shops", []).append({
                        "Name": name_val,
                        "Description": desc_val,
                        "Notes": [],
                        "Inventory": [],
                        "People": []
                    })
                case "place":
                    item_data.setdefault("Places", []).append({
                        "Name": name_val,
                        "Description": desc_val,
                        "Notes": [],
                        "Effects": [],
                        "People": []
                    })
                case "effect":
                    item_data.setdefault("Effects", []).append({
                        "Name": name_val,
                        "Description": desc_val
                    })
                case "inventory":
                    item_data.setdefault("Inventory", []).append({
                        "Name": name_val,
                        "Description": desc_val,
                        "Price": price_val
                    })

            save_json("regions.json", data)
            from functions.pages import dynamic_page_loader
            close_popup_and_refresh(popup, root, left_frame, right_frame,
                                    lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))
    submit_buttons(root, popup, "Submit", on_submit)

def remove_feature(section, feature_type, root, left_frame=None, right_frame=None):
    data = load_json("regions.json")
    item_data = type_flags(section, data)

    feature_list = []

    match feature_type:
        case "shop":
            removal = "Shops"
            for shop in item_data.get("Shops", []):
                feature_list.append(shop["Name"])
        case "place":
            removal = "Places"
            for place in item_data.get("Places", []):
                feature_list.append(place["Name"])
        case "effect":
            removal = "Effects"
            for effect in item_data.get("Effects", []):
                feature_list.append(effect["Name"])
        case "inventory":
            removal = "Inventory"
            for inventory in item_data.get("Inventory", []):
                feature_list.append(inventory["Name"])

    if not feature_list:
        show_error(f"No {feature_type} found in {section}.", root)
        return

    popup_title = f"Add {feature_type} to {section}"
    popup_label = f"Add Note to {section}"
    popup_fields = [
        {
            "key": "name",
            "label": f"Choose which {feature_type} to remove",
            "type": "radio",
            "options": feature_list,
            "default": feature_list[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def on_submit():
        name_val = values["name"].get()

        item_data[removal] = [v for v in item_data[removal] if v["Name"] != name_val]
        save_json("regions.json", data)

        from functions.pages import dynamic_page_loader
        close_popup_and_refresh(popup, root, left_frame, right_frame,
                                lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))

    submit_buttons(root, popup, "Submit", on_submit)

def update_feature(section, feature_type, root, left_frame=None, right_frame=None):
    data = load_json("regions.json")
    item_data = type_flags(section, data)
    result = find_category(section, data)

    inventory_flag = False
    feature_list = []

    item_type = result[0]
    match item_type:
        case "Region":
            item_data = result[1]
            current_name = item_data.get("Region", "")
        case "City":
            item_data = result[1]
            current_name = item_data.get("City", "")
        case "POI":
            item_data = result[1]
            current_name = item_data.get("POI", "")
        case "Place" | "Shop":
            item_data = result[2]
            current_name = item_data.get("Name", "")

    match feature_type:
        case "shop":
            update = "Shops"
            for shop in item_data.get("Shops", []):
                feature_list.append(shop["Name"])
        case "place":
            update = "Places"
            for place in item_data.get("Places", []):
                feature_list.append(place["Name"])
        case "effect":
            update = "Effects"
            for effect in item_data.get("Effects", []):
                feature_list.append(effect["Name"])
        case "inventory":
            inventory_flag = True
            update = "Inventory"
            for inventory in item_data.get("Inventory", []):
                feature_list.append(inventory["Name"])

    if not feature_list:
        show_error(f"No {feature_type} found in {section}.", root)
        return

    popup_title = f"Update {feature_type}"
    popup_label = f"Add Note to {section}"
    popup_fields = [
        {
            "key": "name",
            "label": f"Choose which {feature_type} to update",
            "type": "radio",
            "options": feature_list,
            "default": feature_list[0]
        }
    ]
    popup, values = initiate_popup(root, popup_title, popup_label, popup_fields)

    def feature_selected():
        selected_id = values["name"].get()
        current_feature = next((n for n in item_data.get(update, []) if n["Name"] == selected_id), None)

        desc_text = current_feature["Description"]
        for w in popup.winfo_children():
            w.destroy()

        tk.Label(popup, text="Name").pack()
        name_entry = tk.Entry(popup)
        name_entry.pack()
        name_entry.insert(0, current_feature["Name"])

        tk.Label(popup, text="Description").pack()
        text_widget = tk.Text(popup, height=8, width=50)
        text_widget.pack(pady=10)
        text_widget.insert("1.0", current_feature.get("Description", ""))

        if inventory_flag:
            tk.Label(popup, text="Price").pack()
            price_entry = tk.Entry(popup)
            price_entry.pack()
            price_entry.insert(0, current_feature.get("Price", ""))

        def on_submit():
            new_name = name_entry.get().strip()
            new_desc = text_widget.get("1.0", tk.END).strip()
            if inventory_flag:
                new_price = price_entry.get()
                if not new_name or not new_desc or not new_price:
                    show_error("Missing name, description, or price", root)
            else:
                if not new_name or not new_desc:
                    show_error("Name and Description cannot be empty.", root)
                    return

            for feature in item_data.get(update, []):
                if feature["Name"] == selected_id:
                    feature["Name"] = new_name
                    feature["Description"] = new_desc
                    if inventory_flag:
                        feature["Price"] = new_price
                    break

            save_json("regions.json", data)
            from functions.pages import dynamic_page_loader
            close_popup_and_refresh(popup, root, left_frame, right_frame,
                                    lambda r, lf, rf: dynamic_page_loader(config.button_flag, r, lf, rf))

        submit_buttons(root, popup, "Submit", on_submit)
    submit_buttons(root, popup, f"Select {feature_type}", feature_selected)

def clear_data(root, left_frame, right_frame):
    popup = tk.Toplevel(root)
    popup.title("Clear Data Confirmation")

    instr_label = tk.Label(popup, text=f"This will delete all {config.clear_flag} data.\nPlease confirm.")
    instr_label.pack(pady=10)

    def on_submit():
        if config.clear_flag == "party" or config.clear_flag == "of your non-setting":
            save_json("party.json", [])
            save_json("camp.json", [])
        if config.clear_flag == "bestiary" or config.clear_flag == "of your non-setting":
            save_json("random.json", [])
            save_json("required.json", [])
            save_json("archive.json", [])
        if config.clear_flag == "regions" or config.clear_flag == "of your non-setting":
            save_json("regions.json", {})
        popup.destroy()

    def on_cancel():
        popup.destroy()

    submit_btn = tk.Button(popup, text="Confirm", command=on_submit)
    submit_btn.pack(pady=10)
    cancel_btn = tk.Button(popup, text="Cancel", command=on_cancel)
    cancel_btn.pack(pady=10)