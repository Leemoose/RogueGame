from monster_implementation import Monster_AI
from .ooze_utility import do_ooze_move
from monster_implementation import  rank_move

class Ooze_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.options["move"] = (rank_move, do_ooze_move)