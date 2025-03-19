from monster_implementation import Monster_AI
from monster_implementation import rank_find_item, do_find_item, rank_pickup, do_item_pickup, rank_flee, do_flee

class Goblin_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "pickup": (100, 5),
                           "find_item": (80, 10),
                           "move": (40, 10),
                           "flee": (100, 10)
                           }
        self.options["find_item"] = (rank_find_item, do_find_item)
        self.options[ "pickup"] =  (rank_pickup, do_item_pickup)
        self.options[ "flee"] = (rank_flee, do_flee)
                        