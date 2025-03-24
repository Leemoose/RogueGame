from monster_implementation.monster_ai import Monster_AI
from .orc_utility import rank_berserk, do_berserk
class Orc_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "move": (40, 20),
                           "berserk": (80, 10)
                           }
        self.options["berserk"] = (rank_berserk, do_berserk)