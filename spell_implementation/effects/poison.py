from .effect import StatusEffect
class Poison(StatusEffect):
    def __init__(self, inflictor, duration = 2, damage = 3):
        super().__init__(801, "Poison", "is being poisoned for " + str(damage) + "damage", duration)
        self.damage = damage
        self.inflictor = inflictor
        self.cumulative = True

    def tick(self, target):
        if self.duration == -100: # -100 is a special value that means the effect lasts forever, -1 probably works too but made it larger just in case
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.inflictor, self.damage)