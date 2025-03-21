
"""
AMULETS
"""
from .equipment import Equipment

class Amulet(Equipment):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Amulet")
        self.equipment_type = "Amulet"
        self.name = "Amulet"
        self.can_be_levelled = False
        self.description = "A heavy amulet in heavy iron?"
        self.slot = "amulet_slot"
        self.traits["amulet"] = True
