from .spawning import branch_params, item_spawner, monster_spawner, interactable_spawner
from .maps import TileMap, TrackingMap
from .mapping_utility import *

"""
Theme: Mapping is responsible for creating all maps at the start of the level, placing monsters, placing item_implementation,
 as well as providing basic information about those maps.
Classes:
    TileDict --> Maps a render tag to the actual image (makes it easy to switch out the image)
    DungeonGenerator --> Sets up the dungeon when the player goes downward. Creates several different maps
        MonsterMap --> Has a unique tag for each monster at their x, y coordinates
        MonsterDict --> Maps the unique tag to the actual monster
        TileMap --> Has each tile in an x, y position
"""


class DungeonGenerator():
    #Generates a width by height 2d array of tiles. Each type of tile has a unique tile
    #tag ranging from 0 to 99
    def __init__(self, depth, player, branch, dungeon_data):
        self.mapData = dungeon_data.get_map_data(branch, depth)
        self.spawn_params = branch_params[branch]

        self.summoner = []

        self.tile_map = TileMap(self.mapData, depth, branch)
        self.monster_map = TrackingMap(self.get_width(), self.get_height())
        self.interact_map = TrackingMap(self.get_width(), self.get_height())
        self.item_map = TrackingMap(self.get_width(), self.get_height())

        self.player = player

        place_spawn_monsters(self, monster_spawner)
        place_spawn_interactables(self, interactable_spawner)
        place_spawn_items(self, item_spawner)

    def get_width(self):
        return self.mapData.get_width()
    
    def get_height(self):
        return self.mapData.get_height()

    def get_branch(self):
        return self.tile_map.get_branch()

    def get_depth(self):
        return self.tile_map.get_depth()
    def get_random_passable_location(self,stairs_block = True):
        start_x = random.randint(0, self.get_width() - 1)
        start_y = random.randint(0, self.get_height() - 1)
        count = 0
        while (not self.get_passable((start_x, start_y))) or (not stairs_block or self.get_is_on_stairs(start_x, start_y)):
            start_x = random.randint(0, self.get_width() - 1)
            start_y = random.randint(0, self.get_height() - 1)
            count += 1
            if count > 1000:
                raise Exception("Stuck in infinite loop for checking random location.")
        return start_x, start_y

    def get_random_location(self, stairs_block = True, condition = None):
        candidates = []
        if condition == None:
            return self.get_random_passable_location(stairs_block)
        for x in range(0, self.get_width()):
            for y in range(0, self.get_height()):
                if condition((x, y)) or \
                    (not stairs_block or self.get_is_on_stairs(x, y)):
                    candidates.append((x, y))
        startx, starty = random.choice(candidates)
        return startx, starty

    def get_monsters_in_sight(self):
        in_sight = []
        for monster in self.monster_map.get_all_entities():
            monster_x, monster_y = monster.get_location()
            if self.tile_map.get_entity(monster_x, monster_y).get_visible():
                in_sight.append(monster)
        return in_sight

    def get_all_seen(self):
        return self.tile_map.get_is_all_visible(), self.tile_map.get_next_not_visible_coordinate()

    def count_passable_neighbors(self, x, y):
        count = 0
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if self.get_passable((x + direction[0], y + direction[1])):
                count += 1
        return count

    # def get_nearest_exit (self, entity):
    #     # find the nearest exit to some entity, exit is adjacent to a tile with only tiles adjacent to it that are passable
    #     # if no such tile exists, return None
    #     list_of_exits = []
    #     for x in range(self.get_width()):
    #         for y in range(self.get_height()):
    #             if self.tile_map.get_entity(x,y).passable:
    #                 if self.count_passable_neighbors(x, y) == 2:
    #                     list_of_exits.append((x, y))
    #     entityx, entityy = entity.get_location()
    #     closest_exit = None
    #     closest_distance = 100000
    #     for exit in list_of_exits:
    #         distance = ((entityx - exit[0]) ** 2 + (entityy - exit[1]) ** 2) ** 0.5
    #         if distance < closest_distance:
    #             closest_distance = distance
    #             closest_exit = exit
    #     adjacent_to_exit = None
    #     for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
    #         # check all directions to find tile adjacent to exit that isnt an exit
    #         if self.tile_map.get_has_no_entity(closest_exit[0] + direction[0], closest_exit[1] + direction[1]):
    #             if self.count_passable_neighbors(closest_exit[0] + direction[0], closest_exit[1] + direction[1]) > 2:
    #                 # if tile has a character on it already
    #                 adjacent_to_exit = (closest_exit[0] + direction[0], closest_exit[1] + direction[1])
    #                 break
    #     return adjacent_to_exit
    
    def get_not_on_player(self, x, y):
        if self.player == None:
            return True
        else:
            return (x != self.player.get_x() or y != self.player.get_y())

    def get_passable(self, location):
        if type(location) is not tuple:
            print("You are trying to parse a non tuple")
        if location == None:
            return None
        elif (self.monster_map.get_has_no_entity(location[0], location[1])
              and self.get_not_on_player(location[0], location[1])
              and self.tile_map.get_passable(location[0], location[1])
              and self.interact_map.get_has_no_entity(location[0], location[1])):
            return True
        return False

    def get_nearest_empty_tile(self, location, move = False):
      #  import pdb; pdb.set_trace()
        if location == None:
            return None
        if not move and self.monster_map.get_has_no_entity(location[0], location[1]) and self.get_not_on_player(location[0], location[1]) and self.tile_map.get_has_no_entity(location[0], location[1]):
            return location
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if self.get_passable((location[0] + direction[0], location[1] + direction[1])):
                return (location[0] + direction[0], location[1] + direction[1])
        return None

    def in_map(self, x, y):
       return self.tile_map.in_map(x, y) and self.monster_map.in_map(x, y) and self.interact_map.in_map(x, y)


    def place_monster_at_location(self, creature, x, y):
        if self.get_passable((x, y)):
            creature.set_location(x, y)
            self.monster_map.place_thing(creature)
        else:
            print("Tried to place a creature at an invalid location")

    def place_item_at_location(self, item, x, y):
        if self.in_map(x, y):
            item.set_location(x, y)
            self.item_map.place_thing(item)
        else:
            print("Tried to place an item at an invalid location")

    def place_interactable_at_location(self, interactable, x, y):
        if self.get_passable((x, y)):
            interactable.set_location(x, y)
            self.interact_map.place_thing(interactable)
        else:
            print("Tried to place a interactable at an invalid location")

    def get_is_on_stairs(self, x, y):
        for stair in self.tile_map.stairs:
            if stair.get_x() == x and stair.get_y() == y:
                return True
        return False

    def get_is_in_corridor(self, x, y):
        count_passable = self.count_passable_neighbors(x, y)
        if count_passable > 4:
            return False
        else:
            directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            min_passable = 8
            for dx, dy in directions:
                adj_x = x + dx
                adj_y = y + dy
                if self.tile_map.get_passable(adj_x, adj_y):
                    min_passable = min(min_passable, self.count_passable_neighbors(adj_x, adj_y))
            return min_passable < 3

    def get_passible_map_copy(self):
        tile_map = []
        for x in range(self.get_width()):
            new_row = []
            for y in range(self.get_height()):
                if self.get_passable((x, y)):
                    new_row.append(0)
                else:
                    new_row.append(-1)
            tile_map.append(new_row)
        return tile_map

    # def get_nearest_item(self, x, y):
    #     if self.item_map.get_has_entity(x, y):
    #         return (self.item_map.get_entity(x,y), x, y)
    #     else:
    #         queue = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
    #         flood_map = self.get_passible_map_copy()
    #         return self.get_nearest_item_helper_function(x, y, queue, flood_map)


    # def get_nearest_item_helper_function(self, x, y, queue, flood_map):
    #     for direction in queue:
    #         xdelta, ydelta = direction
    #         if self.in_map(x + xdelta, y + ydelta) and flood_map[x + xdelta][y + ydelta] == 0:
    #             if self.item_map.get_has_entity(x + xdelta, y + ydelta):
    #                 return (self.item_map.get_entity(x + xdelta, y + ydelta), x, y)
    #             else:
    #                 flood_map[x + xdelta][y + ydelta] = -1
    #                 queue_additions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    #                 for direction in queue_additions:
    #                     if self.in_map(x + xdelta, y + ydelta) and flood_map[x + xdelta][y + ydelta] == 0:
    #                         queue.append(direction)
    #     return (None, -1, -1)








