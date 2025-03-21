from monsters.monster import Monster
from .ooze_ai import Ooze_AI
import random

"""
Oozes are slow moving monsters that will destroy any item they touch. Sometimes they destroy the attackers weapon.
"""

class Ooze(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1000, name="Ooze"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=5, brain = Ooze_AI, health=5)
        self.description = "These amorphous blobs of translucent, gelatinous matter emerge from the depths of the rifts. Their bodies pulse with a sickly green glow, fueled by the chaotic energies of their environment. Rift Slimes mindlessly dissolve anything they touch with acidic secretions, leaving behind only a faint, acrid odor. They show no preference or intelligence, simply drawn to any items they encounter, which they swiftly corrode beyond recognition.."
        self.character.action_costs["grab"] = 0
        self.character.action_costs["move"] = 300
        self.character.attributes.experience_given = 10
        self.traits["ooze"] = True

    def do_defend(self, attacker, loop):
        chance_to_destroy_weapon = random.randint(1, 100)
        if chance_to_destroy_weapon <= 5:
            weapon = attacker.body.get_weapon()
            if weapon is not None:
                weapon.set_destroy(True)
                attacker.body.unequip(weapon)
                attacker.inventory.remove_item(weapon)
                loop.add_message("The ooze destroys the weapon of the attacker!")
            else:
                attacker.character.take_damage(self, 1)
        return self.fighter.do_defend()
