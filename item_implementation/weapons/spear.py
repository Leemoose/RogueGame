from item_implementation.weapons.weapons import Weapon
class Spear(Weapon):
    def __init__(self, render_tag=4500):
        super().__init__(-1, -1, 0, render_tag=render_tag, name="Spear", damage_min=4, damage_max=7)
        self.melee = True
        self.range = 2.9
        self.name = "Spear"
        self.description = "It is a spear"


