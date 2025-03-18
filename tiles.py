import objects as O
import monster as M
from items import BasicShield
from spell_implementation import Slow
import npc
import copy


class Floor(O.Tile):
    def __init__(self, x, y, render_tag = 2000, passable = True, blocks_vision = False, id_tag = 0, type = "Floor"):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, blocks_vision=blocks_vision, type = type)
        self.traits["floor"] = True

class Door(Floor):
    def __init__(self, x, y, render_tag = 30, passable = True, blocks_vision = True, id_tag = 0):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, blocks_vision=blocks_vision)

    def open(self):
        self.render_tag = 31
        self.shaded_render_tag = -31
        self.blocks_vision = False
#
# class NPCSpawn(Floor):
#     def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = None):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, type = "NPCSpawn")
#         self.entity = entity(x, y)
#         self.traits["npc_spawn"] = True
#
#     #Not currently supported
#     def spawn_entity(self):
#         return self.entity
#
# class ItemSpawn(Floor):
#     def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = None):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, type = "ItemSpawn")
#         self.entity = entity(x, y)
#         self.traits["item_spawn"] = True
#
#     #Not currently supported
#     def spawn_entity(self):
#         return self.entity
#
# class MonsterSpawn(Floor):
#     def __init__(self, x, y, render_tag, passable = False, id_tag = 0, entity = None):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, type = "MonsterSpawn")
#         self.entity = copy.deepcopy(entity(x, y))
#         self.traits["monster_spawn"] = True
#
#     def spawn_entity(self):
#         return self.entity
#
# class DummyTile(MonsterSpawn):
#     def __init__(self, x, y, render_tag = 6, passable = False, id_tag = 0, entity = M.Dummy):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)
#
# class KingTile(NPCSpawn):
#     def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.King):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)
#
# class GuardTile(NPCSpawn):
#     def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.Guard):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)
#
# class BobBrotherTile(GuardTile):
#     def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.BobBrother):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)
#
class Wall(O.Tile):
    def __init__(self, x, y, render_tag = 2100, passable = False, blocks_vision = True, id_tag = 0):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, blocks_vision = blocks_vision, id_tag = id_tag, type = "Wall")

# class SenseiTile(NPCSpawn):
#     def __init__(self, x, y, render_tag = 6, passable = True, id_tag = 0, entity = npc.Sensei):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)
#
# class ArchmageTile(NPCSpawn):
#     def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.Archmage):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)
#
# class GrabExplainerTile(NPCSpawn):
#     def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.GrabExplainer):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)
#
# class BasicShieldTile(ItemSpawn):
#     def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = BasicShield):
#         super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)


class Stairs(O.Tile):
    def __init__(self, x, y, render_tag = 0, passable = True, id_tag = 0):
        super().__init__(x, y, render_tag, passable, id_tag, type = "Stairs")
        self.stairs = True
        self.pair = None
        self.level_change = 0
        self.traits["stairs"] = True

    def pair_stairs(self, other_stairs):
        self.pair = other_stairs
        other_stairs.pair = self

    def get_paired_stairs(self):
        return self.pair

    def get_has_paired_stairs(self):
        return self.pair != None

    def get_level_change(self):
        return self.level_change


class DownStairs(Stairs):
    def __init__(self, x, y, render_tag = 91, passable = True, id_tag = 0):
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.level_change = 1

class UpStairs(Stairs):
    def __init__(self, x, y, render_tag = 90, passable = True, id_tag = 0):
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.level_change = -1

class Gateway(O.Tile):
    def __init__(self, x, y, level = 1, branch = "Dungeon", render_tag = 92, passable = True, id_tag = 0):
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag, type = "Gateway")
        self.branch = branch
        self.level = level
        self.outgoing = None
        self.incoming = None
        self.traits["gateway"] = True

    def relocate(self, branch, level):
        self.branch = branch
        self.level = level
    def get_branch(self):
        return self.branch

    def get_depth(self):
        return self.level

    def pair_gateway(self, other_gateway):
        self.outgoing = other_gateway
        other_gateway.incoming = self

    def has_outgoing(self):
        return self.outgoing != None

    def has_incoming(self):
        return self.incoming != None


class Water(Floor):
    def __init__(self, x, y, render_tag = 8, passable = True, blocks_vision = False, id_tag = 0, type = "Floor"):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, blocks_vision=blocks_vision, type = type)
        self.effect = [Slow(self, duration = 1)]
        self.traits["water"]= True

    def check_if_status_applies(self, entity):
        #If entity can fly, do not let it happen
        return True

class DeepWater(Floor):
    def __init__(self, x, y, render_tag = 10, passable = False, blocks_vision = False, id_tag = 0, type = "Floor"):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, blocks_vision=blocks_vision, type = type)
        self.effect = [Slow(self, duration = 1)]
        self.traits["deep_water"] = True
        #Make it so it is passable with flying

    def check_if_status_applies(self, entity):
        #If entity can fly, do not let it happen
        return True




