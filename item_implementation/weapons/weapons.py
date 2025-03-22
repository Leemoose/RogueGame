"""
WEAPONS
"""
from item_implementation.equipment import Equipment
# from skills import MagicMissile
import random

class Weapon(Equipment):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name="Unknown weapon", damage_min=0, damage_max=0,
                 armor_piercing=0, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name)
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.armor_piercing = armor_piercing
        self.equipment_type = "Weapon"
        self.slots_taken = 1
        self.on_hit = None
        self.effective = []
        self.attack_cost = attack_cost
        self.diff_action_cost = 0
        self.range = 1
        self.traits["weapon"] = True
        self.slot = "hand_slot"

    def can_be_equipped(self, entity):
        return super().can_be_equipped(entity)

    def get_armor_piercing(self):
        return self.armor_piercing

    def get_damage_min(self):
        return self.damage_min

    def get_damage_max(self):
        return self.damage_max

    def get_range(self):
        return self.range

    def attack(self):
        damage = random.randint(self.damage_min, self.damage_max)
        return damage


class RangedWeapon(Weapon):  # Still working
    def __init__(self, render_tag=351):
        super().__init__(-1, -1, 0, render_tag=render_tag, name="Ranged Weapon")
        self.melee = True
        self.name = "Ranged Weapon"
        self.description = "A ranged weapon"
        self.damage_min = 4
        self.damage_max = 7
        self.effective.append("wood")
        self.traits["ranged_weapon"] = True

    def level_up(self):
        self.enchant()
        self.damage_min += 1
        self.damage_max += 2


class Ax(Weapon):
    def __init__(self, render_tag=300):
        super().__init__(-1, -1, 0, render_tag=render_tag, name="Axe")
        self.melee = True
        self.name = "Axe"
        self.description = "An axe with a round edge (could be rounder). A solid weapon for a solid warrior."
        self.damage_min = 4
        self.damage_max = 7
        self.effective.append("wood")

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more effective."
        if self.level == 6:
            self.description = "An axe with the roundest edge ever seen. It's been enchanted as much as possible."
        self.damage_min += 1
        self.damage_max += 3


class SlicingAx(Ax):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.melee = True
        self.name = "Slicing Ax"
        self.description = "Like cutting paper "
        self.can_be_levelled = True

        self.on_hit = (lambda inflictor: Bleed(3, 4, inflictor))
        self.on_hit_description = f"The target starts to bleed."

        self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Rare"

    def attack(self):
        return (super().attack(), self.on_hit)


class Hammer(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Hammer")
        self.melee = True
        self.name = "Hammer"
        self.description = "A hammer that you wish was more spherical. High damage potential but hard to get a solid hit in."
        self.damage_min = 2
        self.damage_max = 4
        self.effective.append("stone")

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to hit harder"
        if self.level == 6:
            self.description = "A hammer with incredible damage potential. Still not the easiest to get a clean hit in. It's been enchanted as much as possible."
        self.damage_min += 3
        self.damage_max += 3


""""
DAGGERS
+ Specialize in fast attack speed (works well with on hit effects and attack move combinations).
- Low damage (does poorly against armor)
- No armor piercing
"""


class Dagger(Weapon):
    def __init__(self, render_tag=321, attack_cost=20):
        super().__init__(-1, -1, 0, render_tag, "Dagger", attack_cost)
        self.melee = True
        self.name = "Dagger"
        self.description = "I swear that tip is getting rounder... Larry!. Enchanting it might make it more pointy and precise."
        self.damage_min = 1
        self.damage_max = 3

    def activate(self, entity):
        self.wearer = entity
        self.diff_action_cost = max(entity.get_action_cost("attack") - self.attack_cost,
                                    (entity.get_action_cost("attack")) / 2)
        entity.character.change_action_cost("attack", entity.get_action_cost("attack") - self.diff_action_cost)

    def deactivate(self, entity):
        self.wearer = None
        entity.character.change_action_cost("attack", entity.get_action_cost("attack") + self.diff_action_cost)
        self.diff_action_cost = 0

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more precise."
        if self.level == 6:
            self.description = "A dagger that always strikes accurately, never dealing less than full damage. It's been enchanted as much as possible."
        self.damage_min += 0
        self.damage_max += 5
        if self.damage_min > self.damage_max:
            self.damage_min = self.damage_max


class ScreamingDagger(Dagger):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.melee = True
        self.name = "Screaming Dagger"
        self.description = "The sound of thousands dead souls. "
        self.damage_min = 1
        self.damage_max = 1
        self.can_be_levelled = False

        self.on_hit = (lambda inflictor: Tormented(5))
        self.on_hit_description = f"Torments the target for half health damage over."

        self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Legendary"

    def attack(self):
        return (super().attack(), self.on_hit)


"""
SWORDS
 + Specialness lies with armor piercing
 * Average damage
 * Average attack speed
"""


class Sword(Weapon):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Sword", damage_min=4, damage_max=12,
                 armor_piercing=4, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
                         damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.melee = True
        self.description = "Could be rounder honestly."

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more damaging."
        if self.level == 6:
            self.description = "A sword that has been enchanted as much as possible."
        self.damage_min += 1
        self.damage_max += 2


class BroadSword(Sword):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Broadsword", damage_min=4, damage_max=12,
                 armor_piercing=6, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
                         damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.required = 1


class LongSword(Sword):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Longsword", damage_min=4, damage_max=12,
                 armor_piercing=8, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
                         damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.required_strength = 3


class Claymore(Sword):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Claymore", damage_min=8, damage_max=20,
                 armor_piercing=8, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
                         damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.required_strength = 5


class TwoHandedSword(Sword):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Two Handed Sword", damage_min=4, damage_max=12,
                 armor_piercing=10, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
                         damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.slots_taken = 2
        self.required_strength = 5


class GreatSword(TwoHandedSword):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=340, name="Greatsword", damage_min=8, damage_max=20,
                 armor_piercing=15, attack_cost=80):
        super().__init__(x=x, y=y, id_tag=id_tag, render_tag=render_tag, name=name, damage_min=damage_min,
                         damage_max=damage_max, armor_piercing=armor_piercing, attack_cost=attack_cost)
        self.required_strength = 8


################################################
class SleepingSword(Sword):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.melee = True
        self.name = "Sleeping Sword"
        self.description = "...on the treetops. When the wind blows"
        self.can_be_levelled = False

        self.on_hit = (lambda inflictor: Asleep(8))
        self.change_to_hit = 25
        self.on_hit_description = f"The target is sleeping."

        self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Legendary"

    def attack(self):
        hit = random.randint(1, 100)
        if hit < self.change_to_hit:
            return (super().attack(), self.on_hit)
        else:
            return (super().attack(), None)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " the cradle will rock."
        if self.level == 6:
            self.description = "Death is the greatest sleep of all."
            self.damage_min = 1
            self.damage_max = 100
        self.damage_min += 2
        self.damage_max += 3
        if self.damage_min > self.damage_max:
            self.damage_min = self.damage_max


class FlamingSword(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Flaming Sword")
        self.melee = True
        self.name = "Flaming Sword"
        self.description = "A sword that is on fire. You can channel its fire to cast a Burning Attack at a distant foe. "
        self.damage_min = 5
        self.damage_max = 8

        self.on_hit_burn = 4
        self.on_hit_burn_duration = 3
        self.on_hit = (lambda inflictor: Burn(self.on_hit_burn, self.on_hit_burn_duration, inflictor))
        self.on_hit_description = f"Burns the target for {self.on_hit_burn} damage over {self.on_hit_burn_duration} turns."

        self.skill_cooldown = 8
        self.skill_cost = 20
        self.skill_damage = 3
        self.skill_burn_damage = 4
        self.skill_burn_duration = 3
        self.skill_range = 4
        self.attached_skill_exists = True

        self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Legendary"

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.BurningAttack(owner, self.skill_cooldown,
                               self.skill_cost,
                               self.skill_damage,
                               self.skill_burn_damage,
                               self.skill_burn_duration,
                               self.skill_range)

    def attack(self):
        return (super().attack(), self.on_hit)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to hit harder and burn stronger."
        if self.level == 6:
            self.description = "A sword that burns intensely. It's burning strike has reached its maximum potency. It's been enchanted as much as possible."
        self.damage_min += 2
        self.damage_max += 3

        self.skill_damage += 2
        self.skill_cooldown -= 1
        if self.skill_cooldown < 5:
            self.skill_cooldown = 5

        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))


"""
HAMMERS
+ Specializes in high damage
+ Solid armor piercing
- High required strength
- Low attack speed
"""


class CrushingHammer(Hammer):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.melee = True
        self.name = "Crushing Hammer"
        self.description = "Player smash. "
        self.can_be_levelled = True

        self.on_hit = (lambda inflictor: ArmorShredding(5))
        self.on_hit_description = f"Shreds the targets armor."

        self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Rare"

    def attack(self):
        return (super().attack(), self.on_hit)


class MagicWand(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Magic Wand")
        self.melee = True
        self.name = "Magic Wand"
        self.description = "A wand that you can use to cast magic missile. You can also use it in melee but why would you?"
        self.damage_min = 1
        self.damage_max = 5
        self.magic_missile_damage = 6
        self.magic_missile_range = 6
        self.magic_missile_cost = 10
        self.magic_missile_cooldown = 3
        self.attached_skill_exists = True

        self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Common"

        self.attached_skill_exists = True

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return MagicMissile(owner, self.magic_missile_cooldown,
                              self.magic_missile_cost,
                              self.magic_missile_damage,
                              self.magic_missile_range,
                              action_cost=100)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted cast a stronger magic missile"
        if self.level == 6:
            self.description = "A wand that you can use to cast an immensely powerful magic missile. It's been enchanted as much as possible."

        # level up improves magic missile
        self.magic_missile_damage += 2
        self.magic_missile_range += 1
        self.magic_missile_cooldown -= 1
        if self.magic_missile_cooldown < 0:
            self.magic_missile_cooldown = 0

        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))



