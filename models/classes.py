from functions.general import load_json

class BaseClass:
    def __init__(self, name, level, mod):
        self.name = name
        self.level = level
        self.mod = mod

    def get_combat_value(self):
        return self.level * self.mod

class Artificer(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Artificer", level, float(settings["Artificer"]))

class Barbarian(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Barbarian", level, float(settings["Barbarian"]))

class Bard(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Bard", level, float(settings["Bard"]))

class Cleric(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Cleric", level, float(settings["Cleric"]))

class Druid(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Druid", level, float(settings["Druid"]))

class Fighter(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Fighter", level, float(settings["Fighter"]))

class Monk(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Monk", level, float(settings["Monk"]))

class Paladin(BaseClass):
    def  __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Paladin", level, float(settings["Paladin"]))

class Ranger(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Ranger", level, float(settings["Ranger"]))

class Rogue(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Rogue", level, float(settings["Rogue"]))

class Sorcerer(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Sorcerer", level, float(settings["Sorcerer"]))

class Warlock(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Warlock", level, float(settings["Warlock"]))

class Wizard(BaseClass):
    def __init__(self, level):
        settings = load_json("settings.json")
        super().__init__("Wizard", level, float(settings["Wizard"]))

class CustomClass(BaseClass):
    def __init__(self, name, level):
        settings = load_json("settings.json")
        super().__init__(name, level, float(settings["Custom"]))