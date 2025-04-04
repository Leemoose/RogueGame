from .effect import StatusEffect
from global_vars import global_bugtesting
import copy
class Slow(StatusEffect):
    def __init__(self, inflictor, duration = 5, cumulative = False):
        super().__init__(805, "Slow", "feels slow", duration, cumulative = cumulative)
        self.action_cost_change = {}

    def apply_effect(self, target):
        self.action_cost_change = copy.deepcopy(target.character.get_all_action_costs())
        for action in self.action_cost_change:
            target.character.change_action_cost(action, self.action_cost_change[action])
            if global_bugtesting:
                print("The character's action cost for", action, "has been increased by", self.action_cost_change[action])

    def remove(self, target):
        for action in self.action_cost_change:
            target.character.change_action_cost(action, -self.action_cost_change[action])
            if global_bugtesting:
                print("The character's action cost for", action, "has been increased by", self.action_cost_change[action])
                print("The character's action cost is now", target.character.get_action_cost(action))