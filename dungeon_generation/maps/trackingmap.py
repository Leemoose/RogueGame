from .id import ID
from .maps import Maps
"""
This map will either track items or monsters.
"""
class TrackingMap(Maps):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.dict = ID()  # Unique to this floor

    def place_thing(self, thing):
        self.dict.tag_subject(thing)
        self.place_entity(thing.x, thing.y, thing.get_id_tag())

    def get_num_entities(self):
        return self.dict.num_entities()

    def remove_thing(self, thing):
        self.clear_entity(thing.x, thing.y)
        return self.dict.remove_subject(thing.id_tag)

    def move_entity(self, x1, y1, x2, y2):
        self.place_entity(x2, y2, super().get_entity(x1, y1))
        self.clear_entity(x1, y1)

    def get_entity(self, x, y):
        if self.get_has_no_entity(x, y):
            return -1
        else:
            return self.dict.get_subject(super().get_entity(x,y))

    def get_all_entities(self):
        return self.dict.all_entities()

    def __str__(self):
        allrows = ""
        for x in range(self.width):
            row = ' '.join(str(self.entity_map[x][y].render_tag) for y in range(self.height))
            allrows = allrows + row + "\n"
        return allrows