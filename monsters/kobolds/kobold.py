from monsters.monster import Monster
from spell_implementation.fire_school.fire_school import BurningAttack
from .kobold_ai import Kobold_AI
from item_implementation.weapons import Spear

"""
Kobolds should be wielding spears and reposition themselves so they are not next to the attacker, if forced to melee
they will use burning hands ability
"""
class Kobold(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1020, name="Kobold"):
        """
        Initializes a Kobold instance with specific attributes and abilities.

        Parameters:
        x (int): The x-coordinate of the Kobold's position. Defaults to -1.
        y (int): The y-coordinate of the Kobold's position. Defaults to -1.
        render_tag (int): The rendering tag for graphical representation. Defaults to 1020.
        name (str): The name of the Kobold. Defaults to "Kobold".

        Attributes:
        skills (list): The list of skills the Kobold possesses.
        mage (Mage): The mage component of the Kobold, which can cast spells.
        brain (Kobold_AI): The AI controlling the Kobold's behavior.
        inventory (Inventory): The inventory containing the Kobold's items.
        description (str): A description of the Kobold.
        """
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=10,health=20, mana = 10, gold = 5)
        self.skills = []
        self.mage.add_spell(BurningAttack(self, cooldown=10, cost=0, damage=10, burn_damage=4, burn_duration=5, range=1.5))
        self.brain = Kobold_AI(self)
        self.inventory.get_item(Spear())
        self.body.equip(Spear(), self.character.get_attribute("Strength"))

        self.endurance = 0
        self.strength = 0
        self.dexterity = 4
        self.intelligence = 4

        self.description = "Covered in reddish-brown scales that radiate heat, Infernal Kobolds possess razor-sharp claws and teeth. They worship a distant star whose fiery essence imbues them with a burning touch, capable of igniting flammable materials. Despite their small size, they are cunning ambushers, using their fiery abilities to deadly effect in battle. Their eyes glow with reverence and cunning, reflecting their devotion to the star's fiery power."

        self.traits["kobolds"] = True
