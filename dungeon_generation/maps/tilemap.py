from .maps import Maps
from .map_utility import *

"""
This map is responsible for all the tiles in the game.
"""

class TileMap(Maps):

    def __init__(self, mapData, depth, branch):
        super().__init__(mapData.width, mapData.height)
        self.mapData = mapData
        self.stairs = []
        self.gateway = []
        self.rooms = []
        self.depth = depth
        self.branch = branch

        self.track_map_render = [x[:] for x in [["x"] * self.height] * self.width]
        construct_rooms(self)
        render_to_map(self)
        place_stairs(self)

    def __str__(self):
        map = ""
        for row in self.get_map():
            for block in row:
                if block.passable:
                    map += "."
                else:
                    map += "x"
            map += "\n"
        return map

    #Need to get rid of eventually


    def get_depth(self):
        return self.depth

    def get_branch(self):
        return self.branch

    def get_num_rooms(self):
        return self.mapData.get_numRooms()

    def get_tag(self, x, y):
        return self.get_entity(x, y).get_render_tag()

    def get_stairs(self):
        return self.stairs

    def place_tile(self, tile):
        self.place_entity(tile.get_x(), tile.get_y(), tile)

    def get_passable(self, x, y):
        if (self.in_map(x, y) and self.get_entity(x,y).is_passable()):
            return True
        else:
            return False

    def get_visible(self, x, y):
        if (self.in_map(x, y) and self.get_entity(x,y).get_visible()):
            return True
        else:
            return False

    def get_seen(self, x, y):
        if (self.in_map(x, y) and self.get_entity(x,y).get_seen()):
            return True
        else:
            return False

    def get_is_all_visible(self):
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                if self.get_entity(x,y).has_trait("floor") and not self.get_entity(x,y).get_seen():
                    return False
        return True

    def get_next_not_visible_coordinate(self):
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                if self.get_entity(x,y).has_trait("floor") and not self.get_entity(x,y).get_seen():
                    return (x,y)
        return (-1,-1)

    def mark_visible(self, x, y):
        self.get_entity(x, y).set_seen(True)

    def overlaps_any(self, room):
        for other in self.rooms:
            if (room.intersects(other)):
                return True
        return False

    def get_point_in_squircle(self, x, y, circularity):
        originX = 1.0 * (self.width - 1) / 2
        originY = 1.0 * (self.height - 1) / 2
        radius = max(self.width, self.height) / 2

        radiusSqrd = radius ** 2
        squircConst = ((1 - circularity) / radius) ** 2
        localX = x - originX
        localY = y - originY

        xSqrd = localX ** 2
        ySqrd = localY ** 2

        squircleVal = xSqrd + ySqrd - squircConst * xSqrd * ySqrd

        return (squircleVal < radiusSqrd)

    def get_in_squircle(self, room, circularity):
        return self.get_point_in_squircle(room.x, room.y, circularity) and self.get_point_in_squircle(room.x + room.width - 1,
                                                                                              room.y + room.width - 1,
                                                                                           circularity)
    def get_random_location_ascaii(self, stairs_block=True):
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)
        while (not self.track_map_render[startx][starty] == "."):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
        return startx, starty

    def get_random_location(self, stairs_block=True):
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)
        while (not self.get_passable(startx, starty)):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
        return startx, starty




    """
    """
    def get_circularity(self):
        return self.mapData.get_circularity()

    def get_room_size(self):
        return self.mapData.get_roomSize()

