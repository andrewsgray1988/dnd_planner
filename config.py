import tkinter as tk

from functions.general import (
    load_json
)

# Flags
bestiary_flag = None
clear_flag = None
regions_flag = None
button_flag = None
back_flag = None
party_flag = None
last_flag = None
nav_stack = ['Main']

# Settings
SETTINGS_LIST = load_json("settings.json")
ARTI_MOD = SETTINGS_LIST["Artificer"]
BARB_MOD = SETTINGS_LIST["Barbarian"]
BARD_MOD = SETTINGS_LIST["Bard"]
CLER_MOD = SETTINGS_LIST["Cleric"]
DRUI_MOD = SETTINGS_LIST["Druid"]
FIGH_MOD = SETTINGS_LIST["Fighter"]
MONK_MOD = SETTINGS_LIST["Monk"]
PALA_MOD = SETTINGS_LIST["Paladin"]
RANG_MOD = SETTINGS_LIST["Ranger"]
ROGU_MOD = SETTINGS_LIST["Rogue"]
SORC_MOD = SETTINGS_LIST["Sorcerer"]
WARL_MOD = SETTINGS_LIST["Warlock"]
WIZA_MOD = SETTINGS_LIST["Wizard"]
WIDTH = str(SETTINGS_LIST["Width"])
HEIGHT = str(SETTINGS_LIST["Height"])

# Button Labels
MAIN_PAGE_BUTTON_LABELS = [
    "Party and NPCs",
    "Bestiary",
    "Generators",
    "Regions",
    "Settings",
    "Close Program"
]
MANAGE_PARTY_BUTTON_LABELS = [
    "Add Party Member",
    "Update Party Member",
    "Delete Party Member",
    "Move Member to Camp",
    "Move Active from Camp",
    "Go Back"
]
MANAGE_BESTIARY_BUTTON_LABELS = [
    "Add Monster",
    "Delete Monster",
    "Move Monster to Required",
    "Move Monster to Random",
    "Move Monster to Archive",
    "Go Back"
]
SETTINGS_BUTTON_LABELS = [
    "Adjust Setting",
    "Clear Party Data",
    "Clear Bestiary Data",
    "Clear All Data",
    "Reset Settings to Default",
    "Go Back"
]

GENERATORS_BUTTON_LABELS = [
    "Generate Encounter",
    "Generate Individual Loot",
    "Generate Treasure Hoard",
    "Go Back"
]
REGIONS_BUTTON_LABELS = [
    "Add New Region",
    "Remove Region",
    "Go Back"
]
SPECIFIC_REGION_BUTTON_LABELS = [
    "Update Description",
    "Add Note",
    "Remove Note",
    "Add City",
    "Remove City",
    "Add Point",
    "Remove Point",
    "Go Back"
]
CITY_BUTTON_LABELS = [
    "Update Description",
    "Add Note",
    "Remove Note",
    "Add Shop",
    "Remove Shop",
    "Add Place",
    "Remove Place",
    "Go Back"
]
POI_BUTTON_LABELS = {
    "Update Description",
    "Add Note",
    "Remove Note",
    "Add Effect",
    "Remove Effect",
    "Go Back"
}

# Constants
WINDOW_SIZE = f"{WIDTH}x{HEIGHT}"
BUTTON_PACK_OPTIONS = {"fill": tk.X, "pady": 5}

VALID_CLASSES = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid",
                 "Fighter", "Monk", "Paladin", "Ranger", "Rogue",
                 "Sorcerer", "Warlock", "Wizard"]