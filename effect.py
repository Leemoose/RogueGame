import dice as R

class StatusEffect():
    def __init__(self, id_tag, name, message, duration):
        self.id_tag = id_tag
        self.name = name
        self.duration = duration
        self.active = True
        self.message = message

    def apply_effect(self, target):
        pass

    def tick(self, target):
        self.duration -= 1
        if self.duration <= 0:
            self.active = False

class Burn(StatusEffect):
    def __init__(self, duration, damage):
        super().__init__(801, "Burn", "is Burning", duration)
        self.damage = damage

    def apply_effect(self, target):
        pass

    def tick(self, target):
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.damage)
            self.duration -= 1

    def remove(self, target):
        pass

class Petrify(StatusEffect):
    def __init__(self, duration):
        super().__init__(802, "Petrify", "is Petrified", duration)

    def apply_effect(self, target):
        target.movable = False
    
    def remove(self, target):
        target.movable = True

class Might(StatusEffect):
    def __init__(self, duration, strength):
        super().__init__(803, "Might", "feels strong", duration)
        self.strength = strength

    def apply_effect(self, target):
        target.base_damage += self.strength

    def remove(self, target):
        target.base_damage -= self.strength

class Haste(StatusEffect):
    def __init__(self, duration, dexterity):
        super().__init__(804, "Dexterity", "feels fast", duration)
        self.dexterity = dexterity

    def apply_effect(self, target):
        target.dexterity -= self.dexterity
    
    def remove(self, target):
        target.dexterity += self.dexterity