from monsters.monster import Monster
from .goblin_ai import Goblin_AI

"""
Goblins deal a fair amount of damage but will not seek out enemies until they have cleared the floor of item_implementation. Attacks
they do will steal gold.
"""

class Goblin(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1010, name="Goblin", experience_given=10, health=10, min_damage=3, max_damage=5, rarity = "Common", brain = Goblin_AI):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=experience_given, health=health, min_damage=min_damage, max_damage=max_damage, rarity = rarity, brain = brain, gold = 5)
        self.character.action_costs["move"] = 80
        self.character.action_costs["grab"] = 20

        self.description = "These mischievous creatures are smaller and wiry compared to their larger counterparts. Their green skin is mottled and rough, often adorned with patches of scavenged armor and trinkets. With quick, darting eyes that gleam with greed, Goblins are driven by an insatiable desire for shiny objects and valuables. They scurry through the rift-ridden landscapes with nimble steps, their clawed hands eagerly snatching up any glittering loot they come across."

        self.strength = 1
        self.dexterity = 1
        self.endurance = 0
        self.intelligence = 0

        self.traits["goblins"] = True

    def do_attack(self, target, loop):
        #Make sure to add energy cost here
        damage = self.fighter.do_attack(target, loop)
        if damage > 0:
            gold_taken = target.inventory.get_gold() // 2
            self.inventory.change_gold_amount(gold_taken)
            target.inventory.change_gold_amount(-gold_taken)
            loop.add_message("The goblins takes gold away from the defender!")
        return damage