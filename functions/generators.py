import random
import tkinter as tk

from functions.general import (
    load_json,
    show_error,
    find_number
)

LOOT_LIST = load_json("treasure_tables.json")

def random_currency(randnum, dicenum, multiplier, currency):
    count = randnum
    amount = 0
    while count > 0:
        add = random.randint(1, dicenum)
        count -= 1
        amount += add
    amount *= multiplier
    return f"{amount} {currency}"

def random_weapon():
    weapon_list = ["battleaxe", "club", "dagger", "dart", "flail", "glaive", "greataxe", "greatclub", "greatsword",
                   "halberd", "hand crossbow", "handaxe", "heavy crossbow", "javelin", "lance", "light crossbow",
                   "light hammer", "longbow", "longsword", "mace", "maul", "morningstar", "pike", "quarterstaff",
                   "rapier", "scimitar", "shortbow", "shortsword", "sickle", "sling", "spear", "warhammer", "whip"]
    weapon = random.choice(weapon_list)
    return weapon

def figurine_of_power():
    figurine_list = ["bronze griffon", "ebony fly", "golden lions", "ivory goats",
                     "marble elephant", "onyx dog", "onyx dog", "serpentine owl"]
    figurine = random.choice(figurine_list)
    return figurine

def random_armor():
    armor_list = ["+2 half plate armor", "+2 half plate armor", "+2 plate armor", "+2 plate armor",
                  "+3 studded leather armor", "+3 studded leather armor", "+3 breastplate", "+3 breastplate",
                  "+3 splint armor", "+3 splint armor", "+3 half plate armor", "+3 plate armor"]
    armor = random.choice(armor_list)
    return armor

def random_magic_item(letter, count, dicenum):
    loot_list = []

    countone = count
    num_rolls = 0
    while countone > 0:
        num_rolls += random.randint(1, dicenum)
        countone -= 1

    while num_rolls > 0:
        table_name = f"Magic Item Table {letter.upper()}"
        table = LOOT_LIST.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found.")

        roll = random.randint(1, 100)
        item_name = None

        for range_str, data in table.items():
            parts = range_str.split("-")
            if len(parts) == 2:
                start, end = int(parts[0]), int(parts[1])
            elif len(parts) == 1:
                start = end = int(parts[0])
            else:
                raise ValueError(f"Invalid range: {range_str}")

            if start <= roll <= end:
                item_name = data
                break

        match item_name:
            case _ if "Spell scroll (" in item_name:
                spell_level = find_number(item_name)
                item_name = random_spell(spell_level)
            case "+1 weapon":
                item_name = f"+1 {random_weapon()}"
            case "Figurine of wondrous power, ":
                item_name = item_name + f"{figurine_of_power()}"
            case "+2 weapon":
                item_name = f"+2 {random_weapon()}"
            case "+3 weapon":
                item_name = f"+3 {random_weapon()}"
            case "Random armor":
                item_name = random_armor()
            case "Vicious weapon":
                item_name = f"Vicious {random_weapon()}"
            case "Weapon of warning":
                item_name = f"{random_weapon().capitalize()} of warning"
        loot_list.append(item_name)
        num_rolls -= 1

    return loot_list

def random_spell(level):
    spell_list = {
        "0": ["Acid Splash", "Blade Ward", "Chill Touch", "Control Flames", "Create Bonfire", "Dancing Lights",
              "Druidcraft", "Eldritch Blast", "Fire Bolt", "Friends", "Frostbite", "Guidance", "Gust", "Light",
              "Mage Hand", "Magic Stone", "Mending", "Message", "Minor Illusion", "Mold Earth", "Poison Spray",
              "Prestidigitation", "Produce Flame", "Ray of Frost", "Resistance", "Sacred Flame", "Shape Water",
              "Shillelagh", "Shocking Grasp", "Spare the Dying", "Thaumaturgy", "Thorn Whip", "Thunderclap",
              "True Strike", "Vicious Mockery"],
        "1": ["Absorb Elements", "Alarm", "Animal Friendship", "Bane", "Beast Bond", "Bless", "Burning Hands",
              "Catapult", "Charm Person", "Chromatic Orb", "Color Spray", "Command", "Compelled Duel",
              "Comprehend Languages", "Create or Destroy Water", "Cure Wounds", "Detect Evil and Good", "Detect Magic",
              "Detect Poison and Disease", "Disguise Self", "Dissonant Whispers", "Divine Favor", "Earth Tremor",
              "Ensnaring Strike", "Entangle", "Expeditious Retreat", "Faerie Fire", "False Life", "Feather Fall",
              "Find Familiar", "Floating Disk", "Fog Cloud", "Goodberry", "Grease", "Guiding Bolt", "Hail of Thorns",
              "Healing Word", "Hellish Rebuke", "Heroism", "Hex", "Hideous Laughter", "Hunter's Mark", "Ice Knife",
              "Identify", "Illusory Script", "Inflict Wounds", "Jump", "Longstrider", "Mage Armor", "Magic Missile",
              "Protection from Evil and Good", "Purify Food and Drink", "Ray of Sickness", "Sanctuary", "Searing Smite",
              "Shield", "Shield of Faith", "Silent Image", "Sleep", "Speak with Animals", "Thunderous Smite",
              "Thunderwave", "Unseen Servant", "Witch Bolt", "Wrathful Smite"],
        "2": ["Acid Arrow", "Aid", "Alter Self", "Animal Messenger", "Arcane Lock", "Arcanist’s Magic Aura", "Augury",
              "Barkskin", "Beast Sense", "Blindness/Deafness", "Blur", "Branding Smite", "Calm Emotions",
              "Cloud of Daggers", "Continual Flame", "Cordon Of Arrows", "Crown of Madness", "Darkness", "Darkvision",
              "Detect Thoughts", "Dust Devil", "Earthbind", "Enhance Ability", "Enlarge/Reduce", "Enthrall",
              "Find Steed", "Find Traps", "Flame Blade", "Flaming Sphere", "Gentle Repose", "Gust of Wind",
              "Heat Metal", "Hold Person", "Invisibility", "Knock", "Lesser Restoration", "Levitate",
              "Locate Animals or Plants", "Locate Object", "Magic Mouth", "Magic Weapon", "Mirror Image", "Misty Step",
              "Moonbeam", "Pass without Trace", "Phantasmal Force", "Prayer of Healing", "Protection from Poison",
              "Pyrotechnics", "Ray of Enfeeblement", "Rope Trick", "Scorching Ray", "See Invisibility", "Shatter",
              "Silence", "Skywrite", "Spider Climb", "Spike Growth", "Spiritual Weapon", "Suggestion", "Warding Bond",
              "Warding Wind", "Web", "Zone of Truth"],
        "3": ["Animate Dead", "Aura Of Vitality", "Beacon of Hope", "Bestow Curse", "Blinding Smite", "Blink",
              "Call Lightning", "Clairvoyance", "Conjure Animals", "Conjure Barrage", "Counterspell",
              "Create Food and Water", "Crusader's Mantle", "Daylight", "Dispel Magic", "Elemental Weapon",
              "Erupting Earth", "Fear", "Feign Death", "Fireball", "Flame Arrows", "Fly", "Gaseous Form",
              "Glyph of Warding", "Haste", "Hypnotic Pattern", "Lightning Arrow", "Lightning Bolt", "Magic Circle",
              "Major Image", "Mass Healing Word", "Meld into Stone", "Nondetection", "Phantom Steed", "Plant Growth",
              "Protection from Energy", "Remove Curse", "Revivify", "Sending", "Sleet Storm", "Slow", "Speak with Dead",
              "Speak with Plants", "Spirit Guardians", "Stinking Cloud", "Tidal Wave", "Tiny Hut", "Tongues",
              "Vampiric Touch", "Wall of Sand", "Wall of Water", "Water Breathing", "Water Walk", "Wind Wall"],
        "4": ["Arcane Eye", "Aura of Life", "Aura of Purity", "Banishment", "Black Tentacles", "Blight", "Compulsion",
              "Confusion", "Conjure Minor Elementals", "Conjure Woodland Beings", "Control Water", "Death Ward",
              "Dimension Door", "Divination", "Dominate Beast", "Elemental Bane", "Fabricate", "Faithful Hound",
              "Fire Shield", "Freedom of Movement", "Giant Insect", "Grasping Vine", "Greater Invisibility",
              "Guardian of Faith", "Hallucinatory Terrain", "Ice Storm", "Locate Creature", "Phantasmal Killer",
              "Polymorph", "Private Sanctum", "Resilient Sphere", "Secret Chest", "Staggering Smite", "Stone Shape",
              "Stoneskin", "Storm Sphere", "Vitriolic Sphere", "Wall of Fire", "Watery Sphere"],
        "5": ["Animate Objects", "Antilife Shell", "Arcane Hand", "Awaken", "Banishing Smite", "Circle of Power",
              "Cloudkill", "Commune", "Commune with Nature", "Cone of Cold", "Conjure Elemental", "Conjure Volley",
              "Contact Other Plane", "Contagion", "Control Winds", "Creation", "Destructive Wave",
              "Dispel Evil and Good", "Dominate Person", "Dream", "Flame Strike", "Geas", "Greater Restoration",
              "Hallow", "Hold Monster", "Immolation", "Insect Plague", "Legend Lore", "Maelstrom", "Mass Cure Wounds",
              "Mislead", "Modify Memory", "Passwall", "Planar Binding", "Raise Dead", "Reincarnate", "Scrying",
              "Seeming", "Swift Quiver", "Telekinesis", "Telepathic Bond", "Teleportation Circle", "Transmute Rock",
              "Tree Stride", "Wall of Force", "Wall of Stone"],
        "6": ["Arcane Gate", "Blade Barrier", "Bones of the Earth", "Chain Lightning", "Circle of Death", "Conjure Fey",
              "Contingency", "Create Undead", "Disintegrate", "Eyebite", "Find the Path", "Flesh to Stone",
              "Forbiddance", "Freezing Sphere", "Globe of Invulnerability", "Guards and Wards", "Harm", "Heal",
              "Heroes' Feast", "Instant Summons", "Investiture of Flame", "Investiture of Ice", "Investiture of Stone",
              "Investiture of Wind", "Irresistible Dance", "Magic Jar", "Mass Suggestion", "Move Earth", "Planar Ally",
              "Primordial Ward", "Programmed Illusion", "Sunbeam", "Transport via Plants", "True Seeing", "Wall of Ice",
              "Wall of Thorns", "Wind Walk", "Word of Recall"],
        "7": ["Arcane Sword", "Conjure Celestial", "Delayed Blast Fireball", "Divine Word", "Etherealness",
              "Finger of Death", "Fire Storm", "Forcecage", "Magnificent Mansion", "Mirage Arcane", "Plane Shift",
              "Prismatic Spray", "Project Image", "Regenerate", "Resurrection", "Reverse Gravity", "Sequester",
              "Simulacrum", "Symbol", "Teleport", "Whirlwind"],
        "8": ["Animal Shapes", "Antimagic Field", "Antipathy/Sympathy", "Clone", "Control Weather", "Demiplane",
              "Dominate Monster", "Earthquake", "Feeblemind", "Glibness", "Holy Aura", "Incendiary Cloud", "Maze",
              "Mind Blank", "Power Word Stun", "Sunburst", "Telepathy", "Tsunami"],
        "9": ["Astral Projection", "Foresight", "Gate", "Imprisonment", "Mass Heal", "Meteor Swarm", "Power Word Heal",
              "Power Word Kill", "Prismatic Wall", "Shapechange", "Storm of Vengeance", "Time Stop", "True Polymorph",
              "True Resurrection", "Weird", "Wish"]
    }
    level_str = str(level)
    return f"Spell scroll ({random.choice(spell_list[level_str])})"

def generate_encounter(root, left_frame=None, right_frame=None):
    from functions.gui import create_scrollable_frame

    party_list = load_json("party.json")
    random_list = load_json("random.json")
    required_list = load_json("required.json")

    settings_adjustment = load_json("settings.json")
    party_action = settings_adjustment["Action Buffer"]
    party_power = settings_adjustment["Power Buffer"]

    if not party_list:
        show_error("No characters in Party.", root)
    elif not random_list and not required_list:
        show_error("No monsters in Random or Required bestiary", root)

    for plyr in party_list:
        party_power += plyr["combat_value"]
        party_action += plyr["actions"]

    generated_encounter = []
    encounter_actions = 0
    encounter_rating = 0

    for req in required_list:
        tempcount = int(req["count"])
        while tempcount > 0:
            generated_encounter.append(req)
            tempcount -= 1
            encounter_actions += int(req["actions"])
            encounter_rating += float(req["challenge_rating"])

    if random_list:
        failsafe = party_action + 4
        while encounter_rating < party_power and encounter_actions < party_action and failsafe > 0:
            failsafe -= 1
            rand_mon = random.choice(random_list)
            generated_encounter.append(rand_mon)
            encounter_rating += (float(rand_mon["challenge_rating"]) * 0.75)
            encounter_actions += int(rand_mon["actions"])

    encounter_popup = tk.Toplevel(root)
    encounter_popup.title = "Suggested Encounter"

    scroll_frame = create_scrollable_frame(encounter_popup)

    if not generated_encounter:
        error_text = "No Required monsters, and Random monsters are too strong for the current party!"
        label = tk.Label(scroll_frame, text=error_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
        label.pack(fill="x", pady=2)
    else:
        for mon in generated_encounter:
            mon_text = f"{mon['name']} - Challenge Rating: {mon['challenge_rating']}"
            label = tk.Label(scroll_frame, text=mon_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
            label.pack(fill="x", pady=2)

    button_frame = tk.Frame(encounter_popup)
    button_frame.pack(side="bottom", pady=10)

    okay_btn = tk.Button(button_frame, text="OK", command=encounter_popup.destroy)
    okay_btn.pack(pady=10)

    root.wait_window(encounter_popup)

def generate_individual_loot(root, challenge_rating, left_frame=None, right_frame=None):
    from functions.gui import create_scrollable_frame
    loot = []
    roll = random.randint(1, 100)
    if challenge_rating <= 4:
        if roll <= 30:
            loot.append(random_currency(5, 6, 1, "copper"))
        elif 30 < roll <= 60:
            loot.append(random_currency(4, 6, 1, "silver"))
        elif 60 < roll <= 70:
            loot.append(random_currency(3, 6, 1, "electrum"))
        elif 70 < roll <= 95:
            loot.append(random_currency(3, 6, 1, "gold"))
        elif 95 < roll <= 100:
            loot.append(random_currency(1, 6, 1, "platinum"))
    elif 4 < challenge_rating <= 10:
        if roll <= 30:
            loot.append(random_currency(4, 6, 100, "copper"))
            loot.append(random_currency(1, 6, 10, "electrum"))
        elif 30 < roll <= 60:
            loot.append(random_currency(6, 6, 10, "silver"))
            loot.append(random_currency(2, 6, 10, "gold"))
        elif 60 < roll <= 70:
            loot.append(random_currency(3, 6, 10, "electrum"))
            loot.append(random_currency(2, 6, 10, "gold"))
        elif 70 < roll <= 95:
            loot.append(random_currency(4, 6, 10, "gold"))
        elif 95 < roll <= 100:
            loot.append(random_currency(2, 6, 10, "gold"))
            loot.append(random_currency(3, 6, 1, "platinum"))
    elif 10 < challenge_rating <= 16:
        if roll <= 20:
            loot.append(random_currency(4, 6, 100, "silver"))
            loot.append(random_currency(1, 6, 100, "gold"))
        elif 20 < roll <= 35:
            loot.append(random_currency(1, 6, 100, "electrum"))
            loot.append(random_currency(1, 6, 100, "gold"))
        elif 35 < roll <= 75:
            loot.append(random_currency(2, 6, 100, "gold"))
            loot.append(random_currency(1, 6, 10, "platinum"))
        elif 75 < roll <= 100:
            loot.append(random_currency(2, 6, 100, "gold"))
            loot.append(random_currency(2, 6, 10, "platinum"))
    elif challenge_rating > 16:
        if roll <= 15:
            loot.append(random_currency(2, 6, 1000, "electrum"))
            loot.append(random_currency(8, 6, 100, "gold"))
        elif 15 < roll <= 55:
            loot.append(random_currency(1, 6, 1000, "gold"))
            loot.append(random_currency(1, 6, 100, "platinum"))
        elif 55 < roll <= 100:
            loot.append(random_currency(1, 6, 1000, "gold"))
            loot.append(random_currency(2, 6, 100, "platinum"))

    treasure_popup = tk.Toplevel(root)
    treasure_popup.title = "Individual Loot"

    scroll_frame = create_scrollable_frame(treasure_popup)
    for item in loot:
        item_text = f"{item}"
        label = tk.Label(scroll_frame, text=item_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
        label.pack(fill="x", pady=2)

    button_frame = tk.Frame(treasure_popup)
    button_frame.pack(side="bottom", pady=10)

    okay_btn = tk.Button(button_frame, text="OK", command=treasure_popup.destroy)
    okay_btn.pack(pady=10)

    root.wait_window(treasure_popup)

def generate_treasure_hoard(root, challenge_rating, left_frame=None, right_frame=None):
    from functions.gui import create_scrollable_frame
    loot_list = []
    roll = random.randint(1, 100)
    if challenge_rating <= 4:
        loot_list.append(random_currency(6, 6, 100, "copper"))
        loot_list.append(random_currency(3, 6, 100, "silver"))
        loot_list.append(random_currency(2, 6, 10, "gold"))
        if roll <= 6:
            pass
        elif 6 < roll <= 16:
            loot_list.append(random_currency(2, 6, 1, "10 gp gems"))
        elif 16 < roll <= 26:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
        elif 26 < roll <= 36:
            loot_list.append(random_currency(2, 6, 1, "50 gp gems"))
        elif 36 < roll <= 44:
            loot_list.append(random_currency(2, 6, 1, "10 gp gems"))
            loot_list.append(random_magic_item("a", 1, 6))
        elif 44 < roll <= 52:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("a", 1, 6))
        elif 52 < roll <= 60:
            loot_list.append(random_currency(2, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("a", 1, 6))
        elif 60 < roll <= 65:
            loot_list.append(random_currency(2, 6, 1, "10 gp gems"))
            loot_list.append(random_magic_item("b", 1, 4))
        elif 65 < roll <= 70:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("b", 1, 4))
        elif 70 < roll <= 75:
            loot_list.append(random_currency(2, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("b", 1, 4))
        elif 75 < roll <= 78:
            loot_list.append(random_currency(2, 6, 1, "10 gp gems"))
            loot_list.append(random_magic_item("c", 1, 4))
        elif 78 < roll <= 80:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("c", 1, 4))
        elif 80 < roll <= 85:
            loot_list.append(random_currency(2, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("c", 1, 4))
        elif 85 < roll <= 92:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("f", 1, 4))
        elif 92 < roll <= 97:
            loot_list.append(random_currency(2, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("f", 1, 4))
        elif 97 < roll <= 99:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("g", 1, 1))
        elif roll == 100:
            loot_list.append(random_currency(2, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("g", 1, 1))
    elif 4 < challenge_rating <= 10:
        loot_list.append(random_currency(2, 6, 100, "copper"))
        loot_list.append(random_currency(2, 6, 1000, "silver"))
        loot_list.append(random_currency(6, 6, 100, "gold"))
        loot_list.append(random_currency(3, 6, 10, "platinum"))
        if roll <= 4:
            pass
        elif 4 < roll <= 10:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
        elif 10 < roll <= 16:
            loot_list.append(random_currency(2, 6, 1, "50 gp gems"))
        elif 16 < roll <= 22:
            loot_list.append(random_currency(3, 6, 1, "100 gp gems"))
        elif 22 < roll <= 28:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
        elif 28 < roll <= 32:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("a", 1, 6))
        elif 32 < roll <= 36:
            loot_list.append(random_currency(3, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("a", 1, 6))
        elif 36 < roll <= 40:
            loot_list.append(random_currency(3, 6, 1, "100 gp gems"))
            loot_list.append(random_magic_item("a", 1, 6))
        elif 40 < roll <= 44:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("a", 1, 6))
        elif 44 < roll <= 49:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("b", 1, 4))
        elif 49 < roll <= 54:
            loot_list.append(random_currency(3, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("b", 1, 4))
        elif 54 < roll <= 59:
            loot_list.append(random_currency(3, 6, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("b", 1, 4))
        elif 59 < roll <= 63:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("b", 1, 4))
        elif 63 < roll <= 66:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("c", 1, 4))
        elif 66 < roll <= 69:
            loot_list.append(random_currency(3, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("c", 1, 4))
        elif 69 < roll <= 72:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("c", 1, 4))
        elif 72 < roll <= 74:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("c", 1, 4))
        elif 74 < roll <= 76:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("d", 1, 1))
        elif 76 < roll <= 78:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("d", 1, 1))
        elif roll == 79:
            loot_list.append(random_currency(3, 6, 1, "100 gp gems"))
            loot_list.append(random_magic_item("d", 1, 1))
        elif roll == 80:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("d", 1, 1))
        elif 80 < roll <= 84:
            loot_list.append(random_currency(2, 4, 1, "25 gp art objects"))
            loot_list.append(random_magic_item("f", 1, 4))
        elif 84 < roll <= 88:
            loot_list.append(random_currency(3, 6, 1, "50 gp gems"))
            loot_list.append(random_magic_item("f", 1, 4))
        elif 88 < roll <= 91:
            loot_list.append(random_currency(3, 6, 1, "100 gp gems"))
            loot_list.append(random_magic_item("f", 1, 4))
        elif 91 < roll <= 94:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("f", 1, 4))
        elif 94 < roll <= 96:
            loot_list.append(random_currency(3, 6, 1, "100 gp gems"))
            loot_list.append(random_magic_item("g", 1, 4))
        elif 96 < roll <= 98:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("g", 1, 4))
        elif roll == 99:
            loot_list.append(random_currency(3, 6, 1, "100 gp gems"))
            loot_list.append(random_magic_item("h", 1, 1))
        elif roll == 100:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("h", 1, 1))
    elif 10 < challenge_rating <= 16:
        loot_list.append(random_currency(4, 6, 1000, "gold"))
        loot_list.append(random_currency(5, 6, 100, "platinum"))
        if roll <= 3:
            pass
        elif 3 < roll <= 6:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
        elif 6 < roll <= 9:
            loot_list.append(random_currency(2, 4, 1, "750 gp art objects"))
        elif 9 < roll <= 12:
            loot_list.append(random_currency(3, 6, 1, "500 gp gems"))
        elif 12 < roll <= 15:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
        elif 15 < roll <= 19:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("a", 1, 4))
            loot_list.append(random_magic_item("b", 1, 6))
        elif 19 < roll <= 23:
            loot_list.append(random_currency(2, 4, 1, "750 gp art objects"))
            loot_list.append(random_magic_item("a", 1, 4))
            loot_list.append(random_magic_item("b", 1, 6))
        elif 23 < roll <= 26:
            loot_list.append(random_currency(3, 6, 1, "500 gp gems"))
            loot_list.append(random_magic_item("a", 1, 4))
            loot_list.append(random_magic_item("b", 1, 6))
        elif 26 < roll <= 29:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("a", 1, 4))
            loot_list.append(random_magic_item("b", 1, 6))
        elif 29 < roll <= 35:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("c", 1, 6))
        elif 35 < roll <= 40:
            loot_list.append(random_currency(2, 4, 1, "750 gp art objects"))
            loot_list.append(random_magic_item("c", 1, 6))
        elif 40 < roll <= 45:
            loot_list.append(random_currency(3, 6, 1, "500 gp gems"))
            loot_list.append(random_magic_item("c", 1, 6))
        elif 45 < roll <= 50:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("c", 1, 6))
        elif 50 < roll <= 54:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("d", 1, 4))
        elif 54 < roll <= 58:
            loot_list.append(random_currency(2, 4, 1, "750 gp art objects"))
            loot_list.append(random_magic_item("d", 1, 4))
        elif 58 < roll <= 62:
            loot_list.append(random_currency(3, 6, 1, "500 gp gems"))
            loot_list.append(random_magic_item("d", 1, 4))
        elif 62 < roll <= 66:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("d", 1, 4))
        elif 66 < roll <= 68:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("e", 1, 1))
        elif 68 < roll <= 70:
            loot_list.append(random_currency(2, 4, 1, "750 gp art objects"))
            loot_list.append(random_magic_item("e", 1, 1))
        elif 70 < roll <= 72:
            loot_list.append(random_currency(3, 6, 1, "500 gp gems"))
            loot_list.append(random_magic_item("e", 1, 1))
        elif 72 < roll <= 74:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("e", 1, 1))
        elif 74 < roll <= 76:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("f", 1, 1))
            loot_list.append(random_magic_item("g", 1, 4))
        elif 76 < roll <= 78:
            loot_list.append(random_currency(2, 4, 1, "750 gp art objects"))
            loot_list.append(random_magic_item("f", 1, 1))
            loot_list.append(random_magic_item("g", 1, 4))
        elif 78 < roll <= 80:
            loot_list.append(random_currency(3, 6, 1, "500 gp gems"))
            loot_list.append(random_magic_item("f", 1, 1))
            loot_list.append(random_magic_item("g", 1, 4))
        elif 80 < roll <= 82:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("f", 1, 1))
            loot_list.append(random_magic_item("g", 1, 4))
        elif 82 < roll <= 85:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("h", 1, 4))
        elif 85 < roll <= 88:
            loot_list.append(random_currency(2, 4, 1, "750 gp art objects"))
            loot_list.append(random_magic_item("h", 1, 4))
        elif 88 < roll <= 90:
            loot_list.append(random_currency(3, 6, 1, "500 gp gems"))
            loot_list.append(random_magic_item("h", 1, 4))
        elif 90 < roll <= 92:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("h", 1, 4))
        elif 92 < roll <= 94:
            loot_list.append(random_currency(2, 4, 1, "250 gp art objects"))
            loot_list.append(random_magic_item("i", 1, 1))
        elif 94 < roll <= 96:
            loot_list.append(random_currency(2, 4, 1, "750 gp art objects"))
            loot_list.append(random_magic_item("i", 1, 1))
        elif 96 < roll <= 98:
            loot_list.append(random_currency(3, 6, 1, "500 gp gems"))
            loot_list.append(random_magic_item("i", 1, 1))
        elif 98 < roll <= 100:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("i", 1, 1))
    elif challenge_rating > 16:
        loot_list.append(random_currency(12, 6, 1000, "gold"))
        loot_list.append(random_currency(8, 6, 1000, "platinum"))
        if roll <= 2:
            pass
        elif 2 < roll <= 5:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("c", 1, 8))
        elif 5 < roll <= 8:
            loot_list.append(random_currency(1, 10, 1, "2500 gp art objects"))
            loot_list.append(random_magic_item("c", 1, 8))
        elif 8 < roll <= 11:
            loot_list.append(random_currency(1, 4, 1, "7500 gp art objects"))
            loot_list.append(random_magic_item("c", 1, 8))
        elif 11 < roll <= 14:
            loot_list.append(random_currency(1, 8, 1, "5000 gp gems"))
            loot_list.append(random_magic_item("c", 1, 8))
        elif 14 < roll <= 22:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("d", 1, 6))
        elif 22 < roll <= 30:
            loot_list.append(random_currency(1, 10, 1, "2500 gp art objects"))
            loot_list.append(random_magic_item("d", 1, 6))
        elif 30 < roll <= 38:
            loot_list.append(random_currency(1, 4, 1, "7500 gp art objects"))
            loot_list.append(random_magic_item("d", 1, 6))
        elif 38 < roll <= 46:
            loot_list.append(random_currency(1, 8, 1, "5000 gp gems"))
            loot_list.append(random_magic_item("d", 1, 6))
        elif 46 < roll <= 52:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("e", 1, 6))
        elif 52 < roll <= 58:
            loot_list.append(random_currency(1, 10, 1, "2500 gp art objects"))
            loot_list.append(random_magic_item("e", 1, 6))
        elif 58 < roll <= 63:
            loot_list.append(random_currency(1, 4, 1, "7500 gp art objects"))
            loot_list.append(random_magic_item("e", 1, 6))
        elif 63 < roll <= 68:
            loot_list.append(random_currency(1, 8, 1, "5000 gp gems"))
            loot_list.append(random_magic_item("e", 1, 6))
        elif roll == 69:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("g", 1, 4))
        elif roll == 70:
            loot_list.append(random_currency(1, 10, 1, "2500 gp art objects"))
            loot_list.append(random_magic_item("g", 1, 4))
        elif roll == 71:
            loot_list.append(random_currency(1, 4, 1, "7500 gp art objects"))
            loot_list.append(random_magic_item("g", 1, 4))
        elif roll == 72:
            loot_list.append(random_currency(1, 8, 1, "5000 gp gems"))
            loot_list.append(random_magic_item("g", 1, 4))
        elif 72 < roll <= 74:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("h", 1, 4))
        elif 74 < roll <= 76:
            loot_list.append(random_currency(1, 10, 1, "2500 gp art objects"))
            loot_list.append(random_magic_item("h", 1, 4))
        elif 76 < roll <= 78:
            loot_list.append(random_currency(1, 4, 1, "7500 gp art objects"))
            loot_list.append(random_magic_item("h", 1, 4))
        elif 78 < roll <= 80:
            loot_list.append(random_currency(1, 8, 1, "5000 gp gems"))
            loot_list.append(random_magic_item("h", 1, 4))
        elif 80 < roll <= 85:
            loot_list.append(random_currency(3, 6, 1, "1000 gp gems"))
            loot_list.append(random_magic_item("i", 1, 4))
        elif 85 < roll <= 90:
            loot_list.append(random_currency(1, 10, 1, "2500 gp art objects"))
            loot_list.append(random_magic_item("i", 1, 4))
        elif 90 < roll <= 95:
            loot_list.append(random_currency(1, 4, 1, "7500 gp art objects"))
            loot_list.append(random_magic_item("i", 1, 4))
        elif 95 < roll <= 100:
            loot_list.append(random_currency(1, 8, 1, "5000 gp gems"))
            loot_list.append(random_magic_item("i", 1, 4))

    final_list = []
    for item in loot_list:
        if isinstance(item, list):
            final_list.extend(item)
        else:
            final_list.append(item)

    treasure_popup = tk.Toplevel(root)
    treasure_popup.title = "Generated Treasure Hoard"

    scroll_frame = create_scrollable_frame(treasure_popup)
    for item in final_list:
        item_text = f"{item}"
        label = tk.Label(scroll_frame, text=item_text, anchor="w", justify="left", wraplength=scroll_frame.wrap_width)
        label.pack(fill="x", pady=2)

    button_frame = tk.Frame(treasure_popup)
    button_frame.pack(side="bottom", pady=10)

    okay_btn = tk.Button(button_frame, text="OK", command=treasure_popup.destroy)
    okay_btn.pack(pady=10)

    root.wait_window(treasure_popup)