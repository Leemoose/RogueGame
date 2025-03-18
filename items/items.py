
from objects import Objects
from spell_implementation import *
import skills as S

# not equippable or consumable

class Item(Objects):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name=-1):
        super().__init__(x, y, id_tag, render_tag, name)
        self.equipable = False
        self.dropable = True
        self.consumeable = False
        self.equipped = False
        self.destroy = False
        self.description = "Its a " + name + "."
        self.stackable = False
        self.yendorb = False
        self.can_be_levelled = True
        self.level = 1
        self.attached_skill_exists = False
        self.equipment_type = None
        self.traits["item"] = True
        self.rarity = "Common"

    def get_string_description(self):
        description = []
        description.append(self.get_name())
        description.append("Equipment Type " + str(self.equipment_type))
        return description


class Gold(Item):
    def __init__(self, amount, x=-1, y=-1, id_tag = -1, render_tag = 210, name = "Gold"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.traits["gold"] = True
        self.amount = amount

class DestroyedDummy(Item):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 125, name = "Destroyed Dummy"):
        super().__init__(x,y, id_tag, render_tag, name)

"""
GLOVES
"""

"""
PANTS
"""



"""
POTIONS
"""

class Potion(Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Potiorb"
        self.consumeable = True
        self.stackable = True
        self.stacks = 1
        self.equipable = False
        self.can_be_levelled = False
        self.attached_skill_exists = False
        self.description = "A potiorb that does something."
        self.action_description = "Something flows through your body"
        self.rarity = "Common"
        self.yendorb = False
        self.traits["potion"] = True

    def can_be_equipped(self, entity):
        return False
    
    def can_be_unequipped(self, entity):
        return False

    def activate_once(self, entity):
        pass

    def activate(self, entity):
        self.activate_once(entity)
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True
            entity.inventory.remove_item(self)

class Scroll(Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Scrorb"
        self.consumeable = True
        self.stackable = True
        self.equipable = False
        self.can_be_levelled = False
        self.stacks = 1
        self.attached_skill_exists = False
        self.description = "A scrorb that does something."
        self.yendorb = False
        self.traits["scroll"] = True

        self.rarity = "Common"

    def can_be_equipped(self, entity):
        return False
    
    def can_be_unequipped(self, entity):
        return False

    def activate_once(self, entity, loop):
        pass

    def activate(self, entity, loop):
        self.activate_once(entity, loop)
        entity.inventory.ready_scroll = self

    def consume_scroll(self, entity):
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True
            entity.inventory.remove_item(self)

class TeleportScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Teleport Scrorb")
        self.description = "Let's go for a ride."
        self.rarity = "Common"
        self.skill = S.Teleport(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(entity, loop.generator, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop("inventory")

class MassTormentScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mass Torment Scrorb")
        self.description = "Must kill everything."
        self.rarity = "Rare"
        self.skill = S.MassTorment(None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop("inventory")

class InvincibilityScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Invincibility Scrorb")
        self.description = "Death cannot hold me back."
        self.rarity = "Legendary"
        self.skill = S.Invinciblity(self, 0, 5, 0)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop("inventory")

class CallingScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "The Scrorb of Calling")
        self.description = "Read at your own peril."
        self.rarity = "Rare"
        self.skill = S.Awaken_Monsters(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop("inventory")

class SleepScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Sleeping Scrorb")
        self.description = "A guide to monster lullabies."
        self.rarity = "Rare"
        self.skill = S.Monster_Lullaby(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop("inventory")

class ExperienceScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Experience Scrorb")
        self.description = "Orb you glad you picked this up."
        self.rarity = "Legendary"
        self.experience = 50

    def activate_once(self, entity, loop):
        entity.experience += entity.experience_to_next_level
        entity.check_for_levelup()
        self.consume_scroll(entity)
        loop.change_loop("inventory")

class HealthPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Health Potiorb")
        self.description = "A potiorb that heals you."
        self.action_description = "Heal by 20 + 10% max health."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.character.change_health(20 + (entity.character.get_max_health() // 10))

class MightPotion(Potion):
    def __init__(self, render_tag = 404):
        super().__init__(render_tag, "Might Potiorb")
        self.description = "A potiorb that makes you stronger for a few turns."
        self.rarity = "Rare"
        self.action_description = "Gain 5 strength temporarily."

    def activate_once(self, entity):
        effect = Might(5, 5)
        entity.character.add_status_effect(effect)

class DexterityPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Dexterity Potiorb")
        self.description = "A potiorb that makes you more dexterous for a few turns."
        self.action_description = "Gain 5 dexterity temporarily."
        self.rarity = "Rare"

    def activate_once(self, entity):
        effect = Haste(5, 5)
        entity.character.add_status_effect(effect)

class PermanentDexterityPotion(Potion):
    def __init__(self, render_tag, dexterity = 1):
        super().__init__(render_tag, "Permanent Dex Potiorb")
        self.description = "Speed in a bottle"
        self.action_description = "Gain 1 dexterity."
        self.rarity = "Rare"
        self.dexterity_addition = dexterity

    def activate_once(self, entity):
        entity.character.change_attribute("Dexterity", self.dexterity_addition)

class PermanentStrengthPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Permanent Str Potiorb")
        self.description = "Strength in a bottle"
        self.action_description = "Gain 1 strength."
        self.rarity = "Rare"

    def activate_once(self, entity):
        entity.character.change_attribute("Strength", 1)

class CurePotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Cure Potiorb")
        self.description = "A potiorb that cures you of all status effects."
        self.action_description = "Remove all status effects."
        self.rarity = "Rare"

    def activate_once(self, entity):
        for effect in entity.character.status_effects:
            if not effect.positive:
                effect.remove(entity)
        entity.status_effects = []

class ManaPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mana Potiorb")
        self.description = "A potiorb that restores your mana."
        self.action_description = "Gain 20 + 10% max mana."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.character.change_mana(20 + (entity.character.max_mana // 10))

class EnchantScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Enchant Scrorb")
        self.description = "A scrorb that enchants an item."
        self.rarity = "Extra Common"

    def activate_once(self, entity, loop):
        loop.limit_inventory = "equipment"
        loop.change_loop("enchant")
        # print("read enchant")

class BurningAttackScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Flame Scrorb")
        self.description = "A scrorb that lets you cast burning attack once."
        self.rarity = "Common"

    def activate_once(self, entity, loop):
        entity.character.ready_skill = S.BurningAttack(entity, 0, 0, 5, 4, 6, 7)
        loop.start_targetting()
        loop.targets.store_skill(0, entity.character.ready_skill, entity, temp_cast=True)

class BlinkScrorb(Scroll):
    def __init__(self, render_tag=450):
        super().__init__(render_tag, "Blink Scrorb")
        self.description = "A scrorb that lets you cast blink once."
        self.rarity = "Rare"

    def activate_once(self, entity, loop):
        entity.character.ready_skill = Blink(entity)
        loop.start_targetting(start_on_player=True)
        loop.targets.store_skill(0, entity.character.ready_skill, entity, temp_cast=True)

class MassHealScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mass Heal Scrorb")
        self.description = "A scrorb that lets you cast mass heal once."
        self.rarity = "Rare"
        self.skill = S.MassHeal(None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop("inventory")


class Book(Item):
    def __init__(self, render_tag, skill, name = "Book"):
        super().__init__(-1, -1, 0, render_tag, name = name)
        self.name = "Book"
        self.equipment_type = "Book"
        self.traits["book"] = True
        self.consumeable = True
        self.stackable = False
        self.equipable = False
        self.can_be_levelled = False
        self.stacks = 1
        self.attached_skill_exists = True
        self.description = "A book that does something."
        self.yendorb = False
        self.rarity = "Rare"

        self.skill = skill
        self.attached_skill = None

    def can_be_equipped(self, entity):
        return False

    def can_be_unequipped(self, entity):
        return False

    def mark_owner(self, entity):
        self.attached_skill = self.skill(entity)

    def activate(self, entity, loop):
        if self.attached_skill.can_learn(entity):
            new_skill = self.skill(entity)
            entity.character.add_skill(new_skill)
            self.destroy = True
            entity.inventory.remove_item(self)
            loop.change_loop("inventory")
        else:
            loop.add_message("You do not have enough intelligence to learn this spell.")

    def get_attached_skill_description(self):
        if self.attached_skill_exists:
            return self.attached_skill.description() # temporarily attach skill to nothing to get name
        else:
            return None

#class BookofSummoning(Book):
#    def __init__(self, render_tag = 480):
#        self.school = spell.SummonSchool()
#        self.skill = self.school.random_spell()
#        super().__init__(render_tag, skill = self.skill, name = "Book of Summoning")
#        self.name = "Book of Summoning"

class BookofSpace(Book):
    def __init__(self, render_tag = 480):
        self.school = SpaceSchool()
        self.skill = self.school.random_spell()
        super().__init__(render_tag, skill = self.skill, name = "Book of Space")
        self.name = "Book of Space"

class BookofFire(Book):
    def __init__(self, render_tag = 480):
        self.school = FireSchool()
        self.skill = self.school.random_spell()
        super().__init__(render_tag, skill = self.skill, name = "Book of Fire")
        self.name = "Book of Fire"

class BookofHypnosis(Book):
    def __init__(self, render_tag = 480):
        self.school = MindSchool()
        self.skill = self.school.random_spell()
        super().__init__(render_tag, skill = self.skill, name = "Book of Hypnosis")
        self.name = "Book of Hypnosis"

class OrbOfYendorb(Item):
    def __init__(self):
        super().__init__(-1, -1, 0, 161, "Orb of Yendorb")
        self.equipable = False
        self.equipment_type = "Orb of Yendorb"
        self.description = "Its the all-powerful orb of yendorb. The magic animating it has deactivated"
        self.stackable = False
        self.level = 1
        self.can_be_levelled = False
        self.ped = False
        self.wearer = None
        self.rarity = "YENDORB"
        self.required_strength = 0
        self.attached_skill_exists = False
        self.yendorb = True

class Orb(Item):
    def __init__(self, x = -1, y=-1, id_tag = 0, render_tag = 0, name = "Orb"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.equipable = False
        self.rarity = "Mythic"
        self.traits['orb'] = True

class ForestOrb(Orb):
    def __init__(self, x = -1, y=-1, id_tag = 4000, render_tag = 0, name = "Forest Orb"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.traits["forest_orb"] = True

class OceanOrb(Orb):
    def __init__(self, x = -1, y=-1, id_tag = 4010, render_tag = 0, name = "Ocean Orb"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.traits["ocean_orb"] = True


####################################
class Consumeable(Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.consumeable = True
        self.stackable = True
        self.stacks = 1
        self.equipable = False
        self.can_be_levelled = False
        self.attached_skill_exists = False
        self.description = "A consumeable item."
        self.action_description = "Something flows through your body"
        self.rarity = "Common"
        self.yendorb = False
        self.traits["consumeable"] = True

    def can_be_equipped(self, entity):
        return False

    def can_be_unequipped(self, entity):
        return False

    def activate_once(self, entity):
        pass

    def activate(self, entity):
        self.activate_once(entity)
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True
            entity.inventory.remove_item(self)


class YellowFlowerPetal(Consumeable):
    def __init__(self, render_tag = 4200):
        super().__init__(render_tag, "Yellow Flower Petal")
        self.description = "A yellow flower petal."
        self.action_description = "Heal by 5."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.character.change_health(5 + (entity.character.get_max_health() // 50))



