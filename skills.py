import random
from spell_implementation import effect as E
from navigation_utility import pathfinding


class Skill():
    def __init__(self, name, parent, cooldown=0, cost=0, range=-1, action_cost=100):
        self.parent = parent
        self.cooldown = cooldown
        self.cost = cost
        self.ready = 0 # keeps track of how long before we can cast, ready = 0 means we can cast
        self.name = name
        self.range = range
        self.targetted = False
        self.targets_monster = True 
        self.action_cost = action_cost
        self.threshold = 0.0
        self.render_tag = 902 # placeholder icon, skill assets are fixed so not given in user input

    def activate(self, target, generator):
        self.parent.character.mana -= self.cost

    def try_to_activate(self, target, loop):
        # check cooldowns and costs
        if self.castable(target):
            self.ready = self.cooldown
            return self.activate(target, loop)
        return False
    
    def tick_cooldown(self):
        if self.ready > 0:
            self.ready -= 1

    def castable(self, target):
        return self.basic_requirements()
    
    def basic_requirements(self):
        if self.ready == 0 and self.parent.character.get_mana() >= self.cost:
            return True
        return False
    
    def health_cost_requirements(self):
        if self.ready == 0 and self.parent.character.get_health() > self.cost:
            return True
        return False
    
    def below_threshold(self):
        return self.parent.character.get_health() < self.threshold * self.parent.character.get_max_health()
    
    def in_range(self, target):
        targetx, targety = target.get_location()
        distance = self.parent.get_distance(targetx, targety)
        if distance < self.range:
            return True

    def __str__(self):
        return self.name
    
    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown"
    
    def full_description(self):
        return self.description()

class MassTorment(Skill):
    def __init__(self, parent):
        self.cooldown = 10
        self.cost = 1
        super().__init__("MassTorment", parent, self.cooldown, self.cost)

    def activate(self, target, loop, bypass = "False"):
        generator = loop.generator
        player = loop.player
        tile_map = generator.tile_map
        monster_map = generator.monster_map
        monster_dict = generator.monster_dict
        for monster_key in monster_dict.subjects:
            monster = monster_dict.get_subject(monster_key)
            if tile_map.track_map[monster.x][monster.y].visible:
                monster.character.health /= 2
        player.character.health /= 2

    def full_description(self):
        desc = "Channel dark magic to half the health of all targets in line of sight.\n\n"
        desc += "Hits both enemies and allies\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"
        return desc

class MassHeal(Skill):
    def __init__(self, parent):
        self.cooldown = 30
        self.cost = 25
        super().__init__("Mass Heal", parent, self.cooldown, self.cost)

    def activate(self, target, loop, bypass = "False"):
        generator = loop.generator
        player = loop.player
        tile_map = generator.tile_map
        monster_map = generator.monster_map
        monster_dict = generator.monster_dict
        for monster_key in monster_dict.subjects:
            monster = monster_dict.get_subject(monster_key)
            if tile_map.track_map[monster.x][monster.y].visible:
                monster.character.health = monster.character.max_health
        player.character.health = player.character.max_health

    def full_description(self):
        desc = "Channel holy magic to heal all targets in line of sight.\n\n"
        desc += "Affects both enemies and allies\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"
        return desc

class Invinciblity(Skill):
    def __init__(self, parent, cost, cooldown, duration, activation_threshold=1.1, by_scroll=True):
        super().__init__("Invincibility", parent, cooldown, cost)
        self.effect = E.Invincible(duration)
        self.dur = duration
        self.by_scroll = by_scroll
        self.threshold = activation_threshold
        self.render_tag = 915

    def activate(self, loop, bypass = False):
        if self.by_scroll:
            loop.player.character.add_status_effect(self.effect)
            self.effect.apply_effect(loop.player.character)
        else:
            self.parent.character.mana -= self.cost
            self.parent.character.add_status_effect(self.effect)
        

    def castable(self, target):
        return self.basic_requirements() and self.below_threshold()
    
    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", invincible for " + str(self.dur) + ", castable below " + str(int(self.threshold * 100)) + "% health)"

    def full_description(self):
        desc = f"Ignore the call of death for {self.dur} turns.\n\n"
        if self.threshold <= 1.0:
            desc += "Can only be cast below " + str(int(self.threshold * 100)) + "% health\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"
        return desc

class Awaken_Monsters(Skill):
    def __init__(self, parent, cooldown, cost):
        super().__init__("Awaken Monsters", parent, cooldown, cost)

    def activate(self, loop, bypass = False):
        monster_dict = loop.generator.monster_dict
        for monster_key in monster_dict.subjects:
            monster = monster_dict.get_subject(monster_key)
            monster.brain.is_awake = True

    # pretty sure this is scroll only but implemented this function just in case
    def full_description(self):
        desc = "Wake up all monsters on the map.\n\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"
        return desc


# !!! keep monster exclusive for now, pathing breaks if a player tries to use it !!!
class BlinkStrike(Skill):
    def __init__(self, parent, cooldown, cost, damage, range, action_cost):
        super().__init__("Blink Strike", parent, cooldown, cost, range, action_cost)
        self.damage = damage
        self.targetted = True
    
    def activate(self, defender, loop):
        self.parent.character.mana -= self.cost
        defender.character.take_damage(self.parent, self.damage + self.parent.character.skill_damage_increase())
        
        path = pathfinding.astar(loop.generator.tile_map.track_map, self.parent.get_location(), defender.get_location(), loop.generator.monster_map, defender, monster_blocks=True)
        if len(path) > 1:
            monster_map = loop.generator.monster_map
            x, y = self.parent.x, self.parent.y
            monster_map.clear_location(x, y)
            self.parent.x, self.parent.y = path[-2] # blink to second last part of path
            monster_map.place_thing(self.parent)
            
        return True

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target)
    
    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(self.damage) + " damage and blink at range " + str(self.range) + ")"


# player exclusive skill
class MagicMissile(Skill):
    def __init__(self, parent, cooldown, cost, damage, range, action_cost):
        super().__init__("Magic missile", parent, cooldown, cost, range, action_cost)
        self.damage = damage
        self.targetted = True
        self.render_tag = 905

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        defender.character.take_damage(self.parent, self.damage + self.parent.character.skill_damage_increase())
        return True

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target)
    
    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(self.damage) + " damage at range " + str(self.range) + ")"
    
    def full_description(self):
        desc = "Blast the target with a bolt of arcane energy.\n\n"
        desc += f"Deals {self.damage} at range {self.range}\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"
        return desc

class BurningAttack(Skill):
    def __init__(self, parent, cooldown, cost, damage, burn_damage, burn_duration, range):
        super().__init__("Burning attack", parent, cooldown, cost, range)
        self.damage = damage
        self.burn_damage = burn_damage
        self.targetted = True
        self.burn_duration = burn_duration
        self.render_tag = 904

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        defender.character.take_damage(self.parent, self.damage + self.parent.character.skill_damage_increase())
        effect = E.Burn(self.burn_duration + self.parent.character.skill_duration_increase(), 
                        self.burn_damage + self.parent.character.skill_damage_increase(), self.parent)
        defender.character.add_status_effect(effect)
        return True # return true if successfully cast, burningAttack cannot fail

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target)
    
    def description(self):
        if self.burn_duration == -100:
            return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(self.damage) + " damage at range " + str(self.range) + ", " + str(self.burn_damage) + " burn damage permanently)"
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(self.damage) + " damage at range " + str(self.range) + ", " + str(self.burn_damage) + " burn damage for " + str(self.burn_duration) + " turns)"
    
    def full_description(self):
        desc = "Throw a small bolt of fire at a target that sets the target ablaze.\n\n"
        desc += f"Deals {self.damage} at range {self.range}\n"
        desc += f"Burns target for {self.burn_damage} burn damage every turn for {self.burn_duration} turns\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc


class Petrify(Skill):
    def __init__(self, parent, cooldown, cost, duration, activation_chance, range):
        super().__init__("Petrify", parent, cooldown, cost, range)
        self.duration = duration
        self.targetted = True
        self.activation_chance = activation_chance
        self.render_tag = 906

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        if random.random() < self.activation_chance:
            if self.duration != -100:
                duration = self.duration + self.parent.character.skill_duration_increase()
            else:
                duration = -100
            effect = E.Petrify(duration)
            defender.character.add_status_effect(effect)
            return True
        return False

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target) and not target.character.has_effect("Petrify")
    
    def description(self):
        if self.duration == -100:
            return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(int(self.activation_chance * 100)) + "% chance to petrify at range " + str(self.range) + ")"
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(int(100 * self.activation_chance)) + "% chance to petrify at range " + str(self.range) + "for " + str(self.duration) + " turns)"
    
    def full_description(self):
        desc = f"Turn the targets body to stone, preventing them from acting for {self.duration} turns.\n\n"
        desc += f"Has a {int(100 * self.activation_chance)}% chance of succeeding.\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc

class ShrugOff(Skill):
    def __init__(self, parent, cooldown, cost, activation_chance, action_cost):
        super().__init__("Shrug off", parent, cooldown, cost, -1, action_cost)
        self.activation_chance = activation_chance
        self.render_tag = 907

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        if self.parent.character.has_negative_effects():
            if random.random() < self.activation_chance:
                negative_effects = [effect for effect in self.parent.character.status_effects if not effect.positive]
                random_effect = random.choice(negative_effects)
                random_effect.active = False
                self.parent.character.remove_status_effect(random_effect)
                return True
        return False

    def castable(self, target):
        return self.basic_requirements() and self.parent.character.has_negative_effects()
    
    def description(self):
        
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(self.activation_chance * 100) + "% chance to remove a negative effect)"
    
    def full_description(self):
        desc = "Shrug off and end a random negative status effect\n\n"
        desc += f"Has a {int(100 * self.activation_chance)}% chance of succeeding.\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc

class Berserk(Skill):
    # self-might if below certain health percent
    def __init__(self, parent, cooldown, cost, duration, activation_threshold, strength_increase, action_cost):
        super().__init__("Berserk", parent, cooldown, cost, -1, action_cost)
        self.threshold = activation_threshold
        self.duration = duration
        self.strength_increase = strength_increase
        self.render_tag = 908
    
    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        if self.duration != -100:
            duration = self.duration + self.parent.character.skill_duration_increase()
        else:
            duration = -100
        effect = E.Might(duration, self.strength_increase)
        self.parent.character.add_status_effect(effect)
        return True

    def castable(self, target):
        return self.basic_requirements and self.below_threshold() and not self.parent.character.has_effect("Might")
    
    def description(self):
        if self.duration == -100:
            return self.name + "(" + str(self.cost) + " health cost, " + str(self.cooldown) + " turn cooldown" + ", +" + str(self.strength_increase) + " strength if below " + str(int(self.threshold * 100)) + "% health)"
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", +" + str(self.strength_increase) + " strength for " + str(self.duration) + " turns if below " + str(int(self.threshold * 100)) + "% health)"

    def full_description(self):
        desc = f"Give into your anger and gain {self.strength_increase} increased strength for {self.duration} turns\n\n"
        desc += f"Only castable below {int(100 * self.threshold)}% health.\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc

class BloodPact(Skill):
    def __init__(self, parent, cooldown, cost, strength_increase, duration, action_cost):
        super().__init__("Blood pact", parent, cooldown, cost, -1, action_cost)
        self.strength_increase = strength_increase
        self.duration = duration
        self.render_tag = 909

    def activate(self, defender, generator):
        self.parent.character.take_damage(self.parent, self.cost)
        effect = E.Might(self.duration + self.parent.character.skill_duration_increase(), self.strength_increase)
        self.parent.character.add_status_effect(effect)
        return True

    def castable(self, target):
        return self.health_cost_requirements() and not self.parent.character.has_effect("Might")
    
    def description(self):
        if self.duration == -100:
            return self.name + "(" + str(self.cost) + " health cost, " + str(self.cooldown) + " turn cooldown" + ", +" + str(self.strength_increase) + " strength)"
        return self.name + "(" + str(self.cost) + " health cost, " + str(self.cooldown) + " turn cooldown" + ", +" + str(self.strength_increase) + " strength for " + str(self.duration) + " turns)"

    def full_description(self):
        desc = f"Pay the price in blood to gain {self.strength_increase} increased strength for {self.duration} turns\n\n"
        desc += f"Costs {self.cost} health on a {self.cooldown} turn cooldown"

        return desc

# I only want this for playtesting, it's not a real skill
class Gun(Skill):
    def __init__(self, parent):
        super().__init__("Gun", parent, 0, 0, 10000)
        self.damage = 10000
        self.targetted = True
        self.render_tag = 903

    def activate(self, defender, generator):
        self.parent.character.change_mana(-self.cost)
        defender.character.take_damage(self.parent, self.damage)
        return True

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target)
    
    def description(self):
        return "Gun (Pew Pew)"
    
    def full_description(self):
        desc = "It's a gun. It goes Pew Pew. It has no real numbers"
        return desc
    
class Terrify(Skill):
    def __init__(self, parent, cooldown, cost, duration, activation_chance, range):
        super().__init__("Terrify", parent, cooldown, cost, range)
        self.duration = duration
        self.activation_chance = activation_chance
        self.targetted = True
        self.render_tag = 910

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        if random.random() < self.activation_chance:
            if self.duration != -100:
                duration = self.duration + self.parent.character.skill_duration_increase()
            else:
                duration = -100
            effect = E.Fear(duration, self.parent)
            defender.character.add_status_effect(effect)
            return True
        return False

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target) and not target.character.has_effect("Fear")
    
    def description(self):
        if self.duration == -100:
            return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(int(self.activation_chance * 100)) + "% chance to terrify at range " + str(self.range) + ")"
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(int(self.activation_chance * 100)) + "% chance to terrify at range " + str(self.range) + "for " + str(self.duration) + " turns)"

    def full_description(self):
        desc = f"Emanates a terrifying aura, forcing a target in range {self.range} to flee for {self.duration} turns.\n\n"
        desc += f"Has a {int(100 * self.activation_chance)}% chance of succeeding.\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc

class Escape(Skill):
    def __init__(self, parent, cooldown, cost, self_fear, dex_buff, str_debuff, int_debuff, haste_duration, activation_threshold, action_cost):
        super().__init__("Escape", parent, cooldown, cost, -1, action_cost)
        self.threshold = activation_threshold
        self.self_fear = self_fear
        self.dex_buff = dex_buff
        self.str_debuff = str_debuff
        self.int_debuff = int_debuff
        self.duration = haste_duration
        self.render_tag = 911

    def activate(self, target, generator):
        self.parent.character.mana -= self.cost
        if self.duration != -100:
            duration = self.duration + self.parent.character.skill_duration_increase()
        else:
            duration = -100
        # haste = E.Haste(duration, self.dex_buff)
        # weak = E.Weak(duration, self.str_debuff)
        # dumb = E.Dumb(duration, self.int_debuff)
        # self.parent.character.add_status_effect(haste)
        # self.parent.character.add_status_effect(weak)
        # self.parent.character.add_status_effect(dumb)
        effect = E.Escaping(duration, self.dex_buff, self.str_debuff, self.int_debuff)
        self.parent.character.add_status_effect(effect)
        if self.self_fear:
            effect = E.Fear(-100, self.parent)
            self.parent.character.add_status_effect(effect)

    def castable(self, target):
        return self.basic_requirements() and self.below_threshold()
    
    def description(self):
        if self.duration == -100:
            addition = " permanently"
        else:
            addition = " for " + str(self.duration) + " turns"
        if self.threshold >= 1:
            return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown, gain " + str(self.dex_buff) + " dexterity, lose " + str(self.str_debuff) + " strength, lose " + str(self.int_debuff) + " intelligence)" + addition
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", castable below " + str(self.threshold * 100) + "% health), gain " + str(self.dex_buff) + " dexterity, lose " + str(self.str_debuff) + " strength, lose " + str(self.int_debuff) + " intelligence)" + addition
    
    def full_description(self):
        desc = f"Sacrifice your other stats to gain a {self.dex_buff} gain in dexterity for {self.duration} turns. \n\n"
        desc += f"Costs {self.cost} mana, {self.str_debuff} strength and {self.int_debuff} intelligence on a {self.cooldown} turn cooldown"

        return desc

class Heal(Skill):
    def __init__(self, parent, cooldown, cost, heal_amount, activation_threshold, action_cost):
        super().__init__("Heal", parent, cooldown, cost, -1, action_cost)
        self.heal_amount = heal_amount
        self.render_tag = 912
        self.threshold = activation_threshold

    def activate(self, target, generator):
        self.parent.character.mana -= self.cost
        target.character.change_health(self.heal_amount + self.parent.character.skill_damage_increase())
        return True

    def castable(self, target):
        return self.basic_requirements() and (self.parent.character.health < self.parent.character.max_health * self.threshold)
    
    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(self.heal_amount) + " health restored when below " + str(int(self.threshold * 100)) + "% health"
    
    def full_description(self):
        desc = "Call on holy magic to heal yourself.\n\n"
        desc += f"Only castable below {int(100 * self.threshold)}% health.\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"
        return desc

class Torment(Skill):
    def __init__(self, parent, cooldown, cost, slow_duration, damage_percent, slow_amount, range, action_cost):
        super().__init__("Torment", parent, cooldown, cost, range, action_cost)
        self.duration = slow_duration
        self.slow_amount = slow_amount
        self.damage_percent = damage_percent
        self.render_tag = 913
    
    def activate(self, target, generator):
        self.parent.character.mana -= self.cost
        damage = int(target.character.health * self.damage_percent)
        target.character.take_damage(self.parent, damage)
        if self.duration != -100:
            duration = self.duration + self.parent.character.skill_duration_increase()
        else:
            duration = -100
        effect = E.Slow(duration, self.slow_amount + self.parent.character.skill_damage_increase())
        target.character.add_status_effect(effect)
        return True
    
    def castable(self, target):
        return self.basic_requirements() and self.in_range(target)
    
    def description(self):
        if self.duration == -100:
            return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(int(self.damage_percent * 100)) + "% of target's health as damage, " + str(self.slow_amount) + " strength slow permanently)"
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(int(self.damage_percent * 100)) + "% of target's health as damage, " + str(self.slow_amount) + " strength slow for " + str(self.duration) + " turns)"
    
    def full_description(self):
        desc = f"Call on dark magic to half the health of and slow down a target in range {self.range}\n\n"
        desc += f"Slows the target by {self.slow_amount} dexterity for {self.duration} turns \n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"
        return desc


