import random
from global_vars import *

class Maps():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entity_map = [x[:] for x in [[-1] * self.height] * self.width]

    def get_map(self):
        return self.entity_map

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_entity(self, x, y):
        if self.in_map(x, y):
            return self.entity_map[x][y]
        else:
            return -1

    def get_has_no_entity(self,x,y):
        if self.in_map(x,y):
            return not self.get_has_entity(x,y)
        else:
            return False

    def get_has_entity(self, x, y):
        if self.in_map(x,y):
            return (self.entity_map[x][y] != -1)
        elif not self.in_map(x,y):
            print("Tried to see if there was an entity outside of map")
        else:
            return False

    def get_random_no_entity_location(self):
        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        while (self.get_has_no_entity(x,y) == False):
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
        return (x,y)

    def get_distance(self, x1, x2, y1, y2):
        if self.in_map(x1,y1) and self.in_map(x2, y2):
            return ((x1-x2)**2+(y1-y2)**2)**(1/2)

    def in_map(self, x, y):
       return x>= 0 and x < self.width and y >= 0 and y < self.height

    def place_entity(self, x, y, entity):
        if self.in_map(x, y):
            if global_bugtesting:
                print("place_entity", x, y, entity)
            self.entity_map[x][y] = entity
        else:
            print("Tried to place entity outside of map")

    def clear_entity(self, x, y):
        if self.in_map(x, y):
            if global_bugtesting:
                print("clear_entity", x, y)
            self.entity_map[x][y] = -1
        else:
            print("Tried to clear entity outside of map")
