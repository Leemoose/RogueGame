from monster_implementation import Monster_AI
from .kobold_utility import rank_burning_hands, do_burning_hands, rank_combat, rank_reposition, do_reposition
from monster_implementation import do_combat

class Kobold_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (50, 10),
                           "move": (40, 20),
                           "reposition": (100, 30),
                           "burning_hands": (60,10)
                           }
        #reposition
        self.options["burning_hands"] = (rank_burning_hands, do_burning_hands)
        self.options["combat"] = (rank_combat, do_combat)
        self.options["reposition"] = (rank_reposition, do_reposition)