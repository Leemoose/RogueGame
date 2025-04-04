from monster_implementation import Monster_AI
from monster_implementation import rank_find_item, do_find_item, rank_pickup, do_item_pickup, rank_flee, do_flee

class Goblin_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.set_tendency("pickup", (100, 5))
        self.set_tendency("find_item", (80, 10))
        self.set_tendency("flee", (100, 10))
        self.options["find_item"] = (rank_find_item, do_find_item)
        self.options[ "pickup"] =  (rank_pickup, do_item_pickup)
        self.options[ "flee"] = (rank_flee, do_flee)
