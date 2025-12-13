from functions.general import (
    save_json,
    load_json,
    show_error
)

class LocationBase:
    def __init__(self, name: str):
        self.name = name
        self.information = ""
        self.persons = []
        self.notes = []

    def set_information(self, info: str):
        self.information = info

    def reindex_notes(self):
        for i, note in enumerate(self.notes, start=1):
            note["id"] = i

    def delete_notes(self, note_id: int):
        self.notes = [n for n in self.notes if n["id"] != note_id]
        self.reindex_notes()

    def add_note(self, note: str):
        note_id = len(self.notes) + 1
        self.notes.append({"id": note_id, "note": note})

class City(LocationBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.shops = []
        self.poi = []

    def add_poi(self, poi_name: str):
        self.poi.append(poi_name)

    def add_shop(self, shop_name: str):
        self.shops.append(shop_name)

    def to_dict(self):
        return {
            "City": self.name,
            "Information": self.information,
            "Places of Interest": self.poi,
            "Shops": self.shops,
            "Persons of Interest": [p.to_dict() for p in self.persons],
            "Notes": self.notes
        }

class PointOfInterest(LocationBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.theme = ""
        self.effects = []

    def set_theme(self, theme: str):
        self.theme = theme

    def add_effect(self, effect: str):
        self.effects.append(effect)

    def to_dict(self):
        return {
            "Point of Interest": self.name,
            "Information": self.information,
            "Theme": self.theme,
            "Effects": self.effects,
            "Persons of Interest": [p.to_dict() for p in self.persons],
            "Notes": self.notes
        }

class Region:
    def __init__(self, name: str):
        self.name = name
        self.cities = []
        self.poi = []
        self.notes = []

    @staticmethod
    def delete(name: str):
        data = load_json("regions.json")
        del data[name]
        save_json("regions.json", data)

    @classmethod
    def load_from_file(cls, name: str):
        data = load_json("regions.json")

        if name not in data:
            return None

        region_data = data[name]
        region = cls(name)

        region.notes = region_data("Notes", [])

        return region

    def add_city(self, city: City):
        if not isinstance(city, City):
            raise TypeError("Expected City Instance")
        self.cities.append(city)

    def add_poi(self, poi: PointOfInterest):
        if not isinstance(poi, PointOfInterest):
            raise TypeError("Expected POI Instance")
        self.poi.append(poi)

    def add_note(self, note: str):
        note_id = len(self.notes) + 1
        self.notes.append({"id": note_id, "note": note})

    def reindex_notes(self):
        for i, note in enumerate(self.notes, start=1):
            note["id"] = i

    def to_dict(self):
        return {
            "Region": self.name,
            "Cities": [c.to_dict() for c in self.cities],
            "POI": [p.to_dict() for p in self.poi],
            "Notes": self.notes
        }

    def save_to_file(self):
        data = load_json("regions.json")
        data[self.name] = self.to_dict()
        save_json("regions.json", data)