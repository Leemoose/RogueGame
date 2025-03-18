"""
ARMORS
SHIELDS
"""
from .equipment import Equipment
class Armor(Equipment):
    def __init__(self, x,y, id_tag, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, "Armor")
        self.name = "Armor"

    def can_be_equipped(self, entity):
        return (entity.get_attribute("Strength")) >= self.required_strength and self.equipable


