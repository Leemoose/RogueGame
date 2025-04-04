from monster_implementation.monster_ai import Monster_AI
from .orc_utility import rank_berserk, do_berserk
class Orc_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.set_tendency("berserk", (80, 10))
        self.options["berserk"] = (rank_berserk, do_berserk)