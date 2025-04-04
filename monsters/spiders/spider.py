from monsters.monster import Monster
from .spider_ai import Spider_AI
from spell_implementation.effects.poison import Poison

#Venom on hit
#Can spin web that slows people
class Spider(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1040, name="Spider", experience_given = 10): #1210 is also working render tag
        super().__init__(x=x, y=y, render_tag=render_tag, name=name, experience_given=experience_given)
        self.description = "These black and white spiders, each the size of a small dog, are swift and deadly predators of the forest. With their distinctive striped patterns, they move with alarming speed, darting through the underbrush and leaping onto unsuspecting prey. Their agile legs and sharp mandibles allow them to navigate any terrain, while their ability to weave intricate webs on tiles makes them formidable hunters and trappers. A single bite from a Rift Spider delivers potent poison, weakening and paralyzing its victims. Beware their sudden, silent approach and the venomous sting that follows, for these spiders are relentless and deadly in their pursuit."
        self.traits["spider"] = True
        self.character.change_action_cost("move", 50)
        self.character.set_action_cost("spin_web", 200)
        self.brain = Spider_AI(self)

        weapon = self.body.get_weapon()
        weapon.add_on_damage_effect(Poison)

