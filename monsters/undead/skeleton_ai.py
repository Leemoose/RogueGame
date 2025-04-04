from monster_implementation.monster_ai import Monster_AI

class Skeleton_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "move": (40, 25)
                           }
        # self.options["combat"] = (rank_combat, do_archer_combat)


