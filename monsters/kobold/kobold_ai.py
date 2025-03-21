from monster_implementation import Monster_AI
from kobold_utility import rank_burning_hands, do_burning_hands

class Kobold_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "move": (40, 20),
                           "burning_hands": (50,10)
                           }
        #reposition
        self.options["burning_hands"] = (rank_burning_hands, do_burning_hands)
        # self.options["pickup"] = (rank_pickup, do_item_pickup)