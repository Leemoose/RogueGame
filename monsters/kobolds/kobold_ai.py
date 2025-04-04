from monster_implementation import Monster_AI
from .kobold_utility import rank_burning_hands, do_burning_hands, rank_combat, rank_reposition, do_reposition
from monster_implementation import do_combat

class Kobold_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.set_tendency("burning_hands", (10,0))
        self.set_tendency("reposition", (100,15))
        #reposition
        self.options["burning_hands"] = (rank_burning_hands, do_burning_hands)
        self.options["combat"] = (rank_combat, do_combat)
        self.options["reposition"] = (rank_reposition, do_reposition)