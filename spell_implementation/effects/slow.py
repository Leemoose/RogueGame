from .effect import StatusEffect
class Slow(StatusEffect):
    def __init__(self, inflictor, duration = 5, dexterity = 5, cumulative = False):
        super().__init__(805, "Slow", "feels slow", duration, cumulative = cumulative)
        self.action_cost_change = {}

    def apply_effect(self, target):
        self.action_cost_change = target.character.get_all_action_costs()
        for action in self.action_cost_change:
            target.character.change_action_cost(action, self.action_cost_change[action])


    def remove(self, target):
        for action in self.action_cost_change:
            target.character.change_action_cost(action, -self.action_cost_change[action])