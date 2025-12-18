class Player:
    def __init__(self, name, armor_class, magic_items, status="Player"):
        self.name = name
        self.status = status
        self.armor_class = armor_class
        self.magic_items = magic_items
        self.classes = []
        self.combat_value = 0
        self.actions = 0

    def add_class(self, class_obj, level):
        temp_instance = class_obj(level)
        for cls in self.classes:
            if cls.name == temp_instance.name:
                raise Exception("Duplicate class name")
        self.classes.append(temp_instance)

    def update_class_level(self, class_name, level):
        class_name_lower = class_name.lower()
        for cls in self.classes:
            if cls.name.lower() == class_name_lower:
                cls.level = level
                break
        else:
            raise ValueError(f"{self.name} does not have {class_name}.")

    def get_combat_value(self):
        combat_value = 0
        armor_value = max(0, 0.01 * (self.armor_class - 10))
        for cls in self.classes:
            combat_value += cls.get_combat_value()
        total = combat_value + armor_value + (self.magic_items * 0.1)
        return round(total, 2)

    def get_action_count(self):
        action_count = 1.5
        barb_level = sum(cls.level for cls in self.classes if cls.name == "Barbarian")
        figh_level = sum(cls.level for cls in self.classes if cls.name == "Fighter")
        monk_level = sum(cls.level for cls in self.classes if cls.name == "Monk")
        pala_level = sum(cls.level for cls in self.classes if cls.name == "Paladin")
        rang_level = sum(cls.level for cls in self.classes if cls.name == "Ranger")
        sorc_level = sum(cls.level for cls in self.classes if cls.name == "Sorcerer")
        wiza_level = sum(cls.level for cls in self.classes if cls.name == "Wizard")
        if barb_level >= 5 or figh_level >= 5 or monk_level >= 5 or pala_level >= 5 or rang_level >= 5 or sorc_level >= 5 or wiza_level >= 5:
            action_count += 1
        if monk_level >= 1:
            action_count += 0.5
        return action_count

    def to_dict(self):
        player_dict = {}
        classes_list = []
        player_dict["name"] = self.name
        player_dict["status"] = self.status
        player_dict["armor_class"] = self.armor_class
        player_dict["magic_items"] = self.magic_items
        player_dict["combat_value"] = self.get_combat_value()
        player_dict["actions"] = self.get_action_count()
        for cls in self.classes:
            classes_list.append({"name": cls.name, "level": cls.level})
        player_dict["classes"] = classes_list
        return player_dict

    def save_to_file(self):
        from functions.general import save_json, load_json
        players_list = load_json("party.json")
        player_dict = self.to_dict()
        players_list.append(player_dict)
        save_json("party.json", players_list)