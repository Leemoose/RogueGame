from monster_implementation.monster_ai import Monster_AI
from .spider_utility import rank_spin_web, do_spin_web
class Spider_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.set_tendency("spin_web", (40, 5))
        self.options["spin_web"] = (rank_spin_web, do_spin_web)

