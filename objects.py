
class Objects():
    def __init__(self, x = -1, y = -1, id_tag = -1, render_tag = -1, name = "Unknown object"):
        self.id_tag = id_tag
        self.render_tag = render_tag
        self.shaded_render_tag = -render_tag
        self.name = name
        self.description = ""
        self.traits = {"object": True}
        self.x = x
        self.y = y

    def __str__(self):
        return self.name

    def has_trait(self, trait):
        if trait in self.traits:
            return self.traits[trait]
        else:
            return False

    def gain_ID(self, ID):
        self.id_tag = ID

    def get_location(self):
        return (self.x,self.y)

    def get_distance(self, x, y):
        return ((self.x - x)**2 + (self.y - y)**2)**(1/2)

    def get_render_tag(self):
        return self.render_tag

    def get_id_tag(self):
        return self.id_tag

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_name(self):
        return self.name

    def get_is_in_square(self, x_start, x_end, y_start, y_end):
        if self.get_x() >= x_start and self.get_x() < x_end and self.get_y()>= y_start and self.get_y() < y_end:
            return True
        else:
            return False

    def set_location(self, x, y):
        self.x = x
        self.y = y


class Tile(Objects):
    def __init__(self, x, y, render_tag = 0, passable = False, blocks_vision = True, id_tag = 0, type = None, walkable = False):
        super().__init__(x, y, id_tag, render_tag, "Tile")
        self.passable = passable
        self.blocks_vision = blocks_vision
        self.walkable = walkable

        self.seen = False
        self.visible = False
        self.on_fire = False
        self.type = type

        self.effect = []

    def get_visible(self):
        return self.visible

    def set_seen(self, seen):
        self.seen = seen

    def get_seen(self):
        return self.seen

    def is_passable(self):
        return self.passable

    def is_blocking_vision(self):
        return self.blocks_vision

    def check_if_status_applies(self, entity):
        return True

    def get_status_effects(self):
        return self.effect

    def __str__(self):
        if self.passable:
            return(".")
        else:
            return("#")

class Item(Objects):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name=-1):
        super().__init__(x, y, id_tag, render_tag, name)
        self.equipable = False
        self.dropable = True
        self.consumeable = False
        self.equipped = False
        self.destroy = False
        self.description = "Its a " + name + "."
        self.stackable = False
        self.yendorb = False
        self.can_be_levelled = True
        self.level = 1
        self.attached_skill_exists = False
        self.equipment_type = None
        self.traits["item"] = True
        self.rarity = "Common"

    def get_string_description(self):
        description = []
        description.append(self.get_name())
        description.append("Equipment Type " + str(self.equipment_type))
        return description
