from monster_implementation import Monster_AI

class Lich_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (-1, 0),
                           "move": (40, 20),
                           "sap_vitality": (80,20)
                           }
        #reposition
        # self.options["sap_vitality"] = (rank_burning_hands, do_burning_hands)
