from monster_implementation import Monster_AI
from .ooze_utility import rank_destroy_items_in_inventory, do_destroy_items_in_inventory
from monster_implementation import rank_pickup, do_item_pickup

class Ooze_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "pickup": (100, 0),
                           "destroy_items": (110, 0),
                           "move": (40, 20),

                           }
        self.options["destroy_items"] = (rank_destroy_items_in_inventory, do_destroy_items_in_inventory)
        self.options["pickup"] = (rank_pickup, do_item_pickup)