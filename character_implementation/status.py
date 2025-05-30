
from global_vars import global_bugtesting

class Status():
    def __init__(self, parent, invincible):
        self.parent = parent
        self.can_move = True
        self.can_grab = True
        self.can_spellcast = True
        self.can_take_actions = True
        self.flee = False
        self.can_teleport = True
        self.safe_rest = True
        self.alive = True
        self.invincible = invincible
        self.status_effects = []
        self.status_effects_immunity = []
        if self.parent.parent.has_trait("Player"):
            self.awake = True
        else:
            self.awake = False

    def get_status_effects(self):
        return self.status_effects

    def get_invincible(self):
        return self.invincible

    def get_safe_rest(self):
        return self.safe_rest

    def get_is_awake(self):
        return self.awake

    def get_flee(self):
        return self.flee

    def set_awake(self, status):
        self.awake = status

    def set_can_spellcast(self, status):
        self.can_spellcast = status

    def remove_status_effect(self, effect):
        if not effect.active:
            effect.remove(self.parent.parent)
            self.status_effects.remove(effect)
            if global_bugtesting:
                print(f"Removed status effect {effect.name} from {self.parent.parent.name}")
                print("Current status effects: " + str([x.name for x in self.status_effects]))

    def has_negative_effects(self):
        for x in self.status_effects:
            if not x.positive:
                return True
        return False

    def has_effect(self, effect_name):
        if effect_name in [x.name for x in self.status_effects]:
            return True
        return False

    def add_status_effect(self, effect):
        if effect.name not in self.status_effects_immunity:
            if not self.has_effect(effect.name):
                effect.apply_effect(self.parent.parent)
                self.status_effects.append(effect)
            else:
                # refresh duration of existing status effect
                for x in self.status_effects:
                    if x.id_tag == effect.id_tag:
                        if x.is_cumulative():
                            x.change_duration(effect.get_duration()) #add more duration
                        else:
                            x.change_duration(effect.get_duration() - x.get_duration()) #reset duration

    def get_status_messages(self):
        messages = []
        for effect in self.status_effects:
            messages.append(effect.message)
        return messages

    def tick_all_status_effects(self):
        for effect in self.get_status_effects():
            effect.tick(self.parent)
        for effect in self.get_status_effects():
            if not effect.active:
                self.remove_status_effect(effect)