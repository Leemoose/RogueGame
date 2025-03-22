from objects import Objects
from item_implementation.talismans.orbs.orb import *
from item_implementation.items import YellowFlowerPetal

class Interactable(Objects):
    def __init__(self, render_tag = 0, x=-1, y=-1, name="Interactable"):
        super().__init__(x=x, y=y,id_tag=-1, render_tag= render_tag, name = name)
        self.name = name
        self.active = True
        self.traits["interactable"] = True

    def interact(self, loop):
        pass

class Campfire(Interactable):
    def __init__(self, render_tag = 2100,x=-1, y = -1, name="Campfire"): #3000 is also render tag
        super().__init__(render_tag, x, y, name=name)
        self.description = "It is a cozy fireplace"

    def interact(self, loop):
        if self.active and loop.get_daytime() == "Nighttime":
            loop.change_daytime()
            self.active = False
            loop.add_message("You rested at the campfire")
            loop.player.character.change_health(loop.player.character.get_max_health()-loop.player.character.get_health())
            self.render_tag = 3001

class OrbPedastool(Interactable):
    def __init__(self, render_tag=0, x=-1, y=-1, name="Orb Pedastool"):
        super().__init__(x=x, y=y, render_tag= render_tag, name = name)
        self.name = name
        self.main_render_tag = 0
        self.deactivated_render_tag = 0
        self.traits["orb_pedastool"] = True
        self.orb_type = "orb"
        self.description = "You feel drawn to it..."

    def interact(self, loop):
        if self.active:
            loop.player.inventory.get_item(self.orb, loop)
            self.render_tag = self.deactivated_render_tag
            self.active = False
        else:
            for orb in loop.player.inventory.get_orb_inventory():
                if orb.has_trait(self.orb_type):
                    self.orb = orb
                    loop.player.inventory.remove_item(orb)
                    self.active = True
                    self.render_tag = self.main_render_tag
                    break

class ForestOrbPedastool(OrbPedastool):
    def __init__(self, render_tag = 3900, x=-1, y=-1, name="Forest Orb Pedastool"):
        super().__init__( render_tag= render_tag, x=x, y=y, name = name)
        self.name = name
        self.orb = ForestOrb()
        self.deactivated_render_tag = 3901
        self.main_render_tag = 3900
        self.traits["forest_orb_pedastool"] = True
        self.orb_type = "forest_orb"

class OceanOrbPedastool(OrbPedastool):
    def __init__(self, render_tag = 3910, x=-1, y=-1, name="Ocean Orb Pedastool"):
        super().__init__( render_tag= render_tag, x=x, y=y, name = name)
        self.name = name
        self.orb = OceanOrb()
        self.deactivated_render_tag = 3911
        self.main_render_tag = 3910
        self.traits["ocean_orb_pedastool"] = True
        self.orb_type = "ocean_orb"

class YellowPlant(Interactable):
    def __init__(self, render_tag = 3800,x=-1, y = -1, name="Yellow Plant"): #3000 is also render tag
        super().__init__(render_tag, x, y, name=name)
        self.used = False
        self.description = "Beautiful yellow plant. I wonder if I can pluck it?"
        self.charges = 3
        self.item = YellowFlowerPetal

    def interact(self, loop):
        if self.charges > 0:
            loop.player.inventory.get_item(self.item(), loop)
            self.charges -= 1
        if self.charges <= 0:
            loop.generator.interact_map.remove_thing(self)





