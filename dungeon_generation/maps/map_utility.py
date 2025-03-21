import random
from .room import Room
from dungeon_generation.tiles import UpStairs, DownStairs, Floor, Wall
def place_room(tilemap, rWidth, rHeight, circularity):
    MaxTries = 100
    startX = random.randint(1, tilemap.get_width() - rWidth - 1)
    startY = random.randint(1, tilemap.get_height() - rHeight - 1)
    room = Room(startX, startY, rWidth, rHeight)
    tries = 0
    while (tilemap.overlaps_any(room) and tilemap.get_in_squircle(room, circularity) and tries < MaxTries):
        room.x = random.randint(1, tilemap.get_width() - rWidth - 1)
        room.y = random.randint(1, tilemap.get_height() - rHeight - 1)
        tries += 1
    if (tries < MaxTries):
        tilemap.rooms.append(room)
        carve_room(tilemap, room, circularity)

def construct_rooms(tilemap):
    for roomNum in range(tilemap.get_num_rooms()):
        size = random.randint(4, tilemap.get_room_size())
        place_room(tilemap, size, size, tilemap.get_circularity())

    # Connect Rooms
    for i in range(len(tilemap.rooms) - 1):
        connect_rooms(tilemap, tilemap.rooms[i], tilemap.rooms[i + 1])


def connect_rooms(tilemap, room1, room2):
    cornerX: int = room1.GetCenterX()
    cornerY: int = room2.GetCenterY()

    lower1X = min(room1.GetCenterX(), cornerX)
    upper1X = max(room1.GetCenterX(), cornerX) + 1
    lower1Y = min(room1.GetCenterY(), cornerY)
    upper1Y = max(room1.GetCenterY(), cornerY) + 1

    for x in range(lower1X, upper1X):
        for y in range(lower1Y, upper1Y):
            if tilemap.track_map_render[x][y] == "x":
                tilemap.track_map_render[x][y] = "."

    lower2X = min(room2.GetCenterX(), cornerX)
    upper2X = max(room2.GetCenterX(), cornerX) + 1
    lower2Y = min(room2.GetCenterY(), cornerY)
    upper2Y = max(room2.GetCenterY(), cornerY) + 1

    for x in range(lower2X, upper2X):
        for y in range(lower2Y, upper2Y):
            if tilemap.track_map_render[x][y] == "x":
                tilemap.track_map_render[x][y] = "."

def carve_room(tilemap, room, circularity):
    originX = 1.0 * (room.width - 1) / 2
    originY = 1.0 * (room.height - 1) / 2
    radius = max(room.width, room.height) / 2

    radiusSqrd = radius ** 2
    squircConst = ((1 - circularity) / radius) ** 2

    for x in range(room.width):
        for y in range(room.height):
            localX = x - originX
            localY = y - originY

            xSqrd = localX ** 2
            ySqrd = localY ** 2

            squircleVal = xSqrd + ySqrd - squircConst * xSqrd * ySqrd

            if (squircleVal < radiusSqrd):
                tilemap.track_map_render[x + room.x][y + room.y] = "."

def place_stairs(tilemap):
    startx, starty = tilemap.get_random_location()
    upstairs = UpStairs(startx, starty)
    tilemap.stairs.append(upstairs)
    tilemap.place_tile(upstairs)

    for i in range(2):
        startx, starty = tilemap.get_random_location()
        downstairs = DownStairs(startx, starty)
        tilemap.stairs.append(downstairs)
        tilemap.place_tile(downstairs)

    if tilemap.get_depth() != 1:
        startx, starty = tilemap.get_random_location()
        upstairs = UpStairs(startx, starty)
        tilemap.stairs.append(upstairs)
        tilemap.place_tile(upstairs)

def render_to_map(tilemap):
    if tilemap.width != len(tilemap.track_map_render) or tilemap.height != len(tilemap.track_map_render[0]):
        raise Exception(
            "The sizing of your map and the render map our different {}, {}, {}, {}".format(tilemap.width, tilemap.height,
                                                                                            len(tilemap.track_map_render),
                                                                                            len(
                                                                                                tilemap.track_map_render[
                                                                                                    0])))
    tilemap.entity_map = []
    for x in range(tilemap.width):
        temp = []
        for y in range(tilemap.height):
            text = tilemap.track_map_render[x][y]
            if x == 0 or y == 0 or x == tilemap.width - 1 or y == tilemap.height - 1:
                if text != "x":
                    print(
                        "Warning: You did not properly buffer the edges of your map and it was overridden to walls")
                temp.append(Wall(x, y))
            elif text == "x":
                temp.append(Wall(x, y))
            elif text == ".":
                temp.append(Floor(x, y))
        tilemap.entity_map.append(temp)


