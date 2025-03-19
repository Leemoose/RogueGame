from .do_actions_utility import *
from .ranking_actions_utility import *

class Monster_AI():
    def __init__(self, parent):
        self.parent = parent
        self.grouped = False
        self.target = None
        self.stairs_location = None

        # first number is average, second is spread
        self.tendencies = {"combat": (80, 10),
                           "move": (40, 20)
                           }
        #what it can actually do
        self.options = {"combat": (rank_combat, do_combat),
                        "move": (rank_move, do_move),
                        }

    """
    Think it would be better to first rank each action depending on the circumstances with a number between 1-100 and 
    then pick the action that ranks the highest
    """

    def rank_actions(self, loop):
        # print(ai.parent.character.energy)
        max_utility = 0
        called_function = (0, do_nothing)

        for action in self.options:
            utility = self.options[action][0](self, loop)
            if utility > max_utility:
                max_utility = utility
                called_function = action

        # print(max_utility)
        self.parent.character.energy -= 1
        # print(f"{ai.parent} is doing {called_function} with utility {max_utility}")
        self.options[called_function][1](self,loop)

    def change_tendency(self, type, new_value):
        if type in self.tendencies:
            self.tendencies[type] = new_value
        else:
            print("That {} cannot change their tendency ({})".format(self.parent, type))

    def get_tendency(self, type):
        if type in self.tendencies:
            return self.tendencies[type]
        else:
            print("That {} does not have that tendency ({})".format(self.parent, type))
            return -1

    def randomize_action(self, action):
        average, spread = self.tendencies[action]
        return max(-1, random.randint(average - spread, average + spread))


class Stumpy_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (90, 10),
                           "pickup": (-1, 0),
                           "find_item": (-1, 00),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (80, 20),
                           "skill": (80, 10),
                           "flee": (-1, 0),
                           "stairs": (-1, 0)
                           }
        
class Dummy_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (-1, 0),
                           "pickup": (-1, 0),
                           "find_item": (-1, 0),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (100, 10),
                           "ungroup": (-1, 0),
                           "skill": (-1, 0),
                           "flee": (-1, 0),
                           "stairs": (-1, 0)
                           }
    
    def do_move(self, loop):
        return

class Insect_Nest_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"nothing":(100,0)
                           }
        # what it can actually do
        self.options = {"nothing":(rank_nothing, do_nothing)}


