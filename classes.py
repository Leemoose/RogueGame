from items import Dagger, Sword
from spell_implementation import TeleportOther
class PlayerClass():
    def __init__(self, name = "Class", items = [], spells = [], endurance = 0, intelligence = 0, dexterity = 0, strength = 0, description = ""):
        self.name = name
        self.items = items
        self.spells = spells
        self.endurance = endurance
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.strength = strength
        self.description = description

    def get_items(self):
        return self.items

    def get_spells(self):
        return self.spells

    def get_attributes(self):
        return (self.endurance, self.intelligence, self.dexterity, self.strength)

    def get_description(self):
        return self.description

class Rogue(PlayerClass):
    def __init__(self):
        super().__init__(name = "Rogue", items = [Dagger()], spells = [TeleportOther], endurance=1, dexterity=2, description="A quick and lethal knife cut is all it takes.")

    def get_spell_names(self):
        return ["Teleport Other"]

class Warrior(PlayerClass):
    def __init__(self):
        super().__init__(name = "Warrior", items = [Sword()], spells = [], endurance=1, dexterity=1, strength=2, description="Brute power overcomes the day.")

    def get_spell_names(self):
        return [""]