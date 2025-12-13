import config

from functions.general import (
    clear_data,
    get_challenge_rating,
    navigate_to,
    go_back
)
from functions.generators import (
    generate_individual_loot,
    generate_treasure_hoard
)

def on_button_click(label, root, left_frame=None, right_frame=None):
    match label:
        case "Add Monster":
            from functions.functions import add_monster
            func = add_monster
        case "Delete Monster":
            from functions.functions import delete_monster
            func = delete_monster
        case "Move Monster to Random":
            from functions.functions import move_monster
            func = move_monster(root, "random", left_frame, right_frame)
        case "Move Monster to Archive":
            from functions.functions import move_monster
            func = move_monster(root, "archive", left_frame, right_frame)
        case "Move Monster to Required":
            from functions.functions import move_monster
            func = move_monster(root, "required", left_frame, right_frame)
        case "Generate Encounter":
            from functions.generators import generate_encounter
            func = generate_encounter
        case "Clear Party Data":
            config.clear_flag = "party"
            func = clear_data
        case "Clear Bestiary Data":
            config.clear_flag = "bestiary"
            func = clear_data
        case "Clear All Data":
            config.clear_flag = "of your non-setting"
            func = clear_data
        case "Generate Individual Loot":
            cr = get_challenge_rating(root)
            if cr is not None:
                generate_individual_loot(root, cr)
                return
        case "Generate Treasure Hoard":
            cr = get_challenge_rating(root)
            if cr is not None:
                generate_treasure_hoard(root, cr)
            return
        case "Add Party Member":
            from functions.functions import add_member
            func = add_member
        case "Close Program":
            from functions.general import close_program
            func = close_program
        case "Delete Party Member":
            from functions.functions import delete_member
            func = delete_member
        case "Main Page":
            from functions.pages import main_page
            navigate_to("Main")
            func = main_page
        case "Generators":
            from functions.pages import generators_page
            navigate_to("Generators")
            func = generators_page
        case "Bestiary":
            from functions.pages import manage_bestiary_page
            navigate_to("Bestiary")
            func = manage_bestiary_page
        case "Party and NPCs":
            from functions.pages import manage_party_page
            navigate_to("Party")
            func = manage_party_page
        case "Update Party Member":
            from functions.functions import update_member
            func = update_member
        case "Regions":
            from functions.pages import regions_base_page
            navigate_to("Regions")
            config.last_flag = "Regions"
            config.regions_flag = label
            config.button_flag = "Regions"
            func = regions_base_page
        case "Settings":
            from functions.pages import settings_page
            navigate_to("Settings")
            func = settings_page
        case "Adjust Setting":
            from functions.functions import adjust_setting
            func = adjust_setting
        case "Add New Region":
            from functions.functions import add_new_region
            func = add_new_region
        case "Remove Region":
            from functions.functions import remove_region
            func = remove_region
        case "Go Back":
            config.last_flag = config.nav_stack[-1]
            previous = go_back()
            config.button_flag = previous
            print(f"label = {label}")
            print(f"previous = {previous}")
            print(f"config.nav_stack = {config.nav_stack}")
            match previous:
                case "Main":
                    from functions.pages import main_page
                    func = main_page
                case "Regions":
                    from functions.pages import regions_base_page
                    config.button_flag = "Regions"
                    func = regions_base_page
                case _:
                    from functions.pages import dynamic_page_loader
                    func = lambda r=root, lf=left_frame, rf=right_frame: dynamic_page_loader(previous, r, lf, rf)
        case "Move Member to Camp":
            from functions.functions import move_member
            config.party_flag = "Active"
            func = move_member
        case "Move Active from Camp":
            from functions.functions import move_member
            config.party_flag = "Camp"
            func = move_member
        case "Add Region Note":
            from functions.functions import add_note
            region = config.button_flag
            func = lambda r=root, l=left_frame, rt=right_frame: add_note(region, r, l, rt)
        case "Remove Region Note":
            from functions.functions import delete_note
            region = config.button_flag
            func = lambda r=root, l=left_frame, rt=right_frame: delete_note(region, r, l, rt)
        case "Add City":
            from functions.functions import add_type
            section = config.button_flag
            func = lambda r=root, l=left_frame, rt=right_frame: add_type(section, "city", r, l, rt)
        case "Remove City":
            from functions.functions import remove_type
            section = config.button_flag
            func = lambda r=root, l=left_frame, rt=right_frame: remove_type(section, "city", r, l, rt)
        case "Add POI":
            from functions.functions import add_type
            section = config.button_flag
            func = lambda r=root, l=left_frame, rt=right_frame: add_type(section, "poi", r, l, rt)
        case "Remove POI":
            from functions.functions import remove_type
            section = config.button_flag
            func = lambda r=root, l=left_frame, rt=right_frame: remove_type(section, "poi", r, l, rt)
        case "Reset Settings to Default":
            from functions.functions import reset_settings
            func = reset_settings
        case _:
            from functions.pages import dynamic_page_loader
            navigate_to(label)
            config.button_flag = label
            print(f"label = {label}")
            print(f"config.nav_stack = {config.nav_stack}")
            print(f"config.button_flag = {config.button_flag}")
            print(f"config.nav_stack[-1] = {config.nav_stack[-1]}")
            print(f"config.nav_stack[-2] = {config.nav_stack[-2]}")
            print(f"config.nav_stack[-3] = {config.nav_stack[-3]}")
            func = dynamic_page_loader(label, root, left_frame, right_frame)

    if func:
        if left_frame and right_frame:
            func(root, left_frame, right_frame)
        else:
            func(root)