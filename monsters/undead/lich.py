from monsters.monster import Monster
from spell_implementation.necromancy_school import SapVitality

"""
Kobolds should be wielding spears and reposition themselves so they are not next to the attacker, if forced to melee
they will use burning hands ability
"""
class Lich(Monster):
    def __init__(self, x=-1, y=-1, render_tag=-1, name="Lich"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=10,health=10, mana = 10, gold = 20)
        self.skills = []
        self.mage.add_spell(SapVitality(self, cooldown=5, cost=3, damage=3, range=5))
        self.brain = Kobold_AI(self)
        self.endurance = 0
        self.strength = 0
        self.dexterity = 0
        self.intelligence = 10

        self.description = "The king of the dead"
        self.traits["lich"] = True
