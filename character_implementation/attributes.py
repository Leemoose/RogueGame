# In progress
class Attributes():
    def __init__(self, parent, endurance=0, intelligence=0, dexterity=0, strength=0, health=100, mana=0, health_regen=0.2, mana_regen=0.2):
        self.endurance = endurance
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.strength = strength

        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.health_regen = health_regen
        self.mana_regen = mana_regen

        self.parent = parent

        self.experience_given = 0  # monsters will overwrite this attribute, it just makes some class stuff easier if its stored in character
        self.experience = 0

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_health_regen(self):
        return self.health_regen

    def get_mana(self):
        return self.mana

    def get_max_mana(self):
        return self.max_mana

    def get_mana_regen(self):
        return self.mana_regen

    def get_strength(self):
        return self.strength

    def get_intelligence(self):
        return self.intelligence

    def get_endurance(self):
        return self.endurance

    def get_dexterity(self):
        return self.dexterity

    def get_experience_given(self):
        return self.experience_given

    def change_strength(self, change):
        self.strength += change

    def change_intelligence(self, change):
        self.intelligence += change

    def change_endurance(self, change):
        self.endurance += change

    def change_dexterity(self, change):
        self.dexterity += change

    def change_health(self, change):
        self.health += change
        self.health = int(self.health)
        if self.health > self.max_health:
            self.health = self.max_health

    def change_health_override(self, new_health):
        self.health = new_health
        if self.health > self.max_health:
            self.health = self.max_health

    def change_max_health(self, change):
        self.max_health += change
        self.change_health(change)

    def change_mana(self, change):
        self.mana += change
        if self.get_mana() > self.get_max_mana():
            self.mana = self.get_max_mana()

    def change_mana_override(self, new_mana):
        self.mana = new_mana
        if self.get_mana() > self.get_max_mana():
            self.mana = self.get_max_mana()

    def change_max_mana(self, change):
        self.max_mana += change
        self.change_mana(change)

    def level_up(self):
        self.change_max_mana(5)
        self.change_max_health(10)


