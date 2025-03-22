class Body():
    def __init__(self, parent):
        self.equipment_slots = {"body_armor_slot": [None],
                                "helmet_slot": [None],
                                "gloves_slot": [None],
                                "boots_slot": [None],
                                "ring_slot": [None, None],
                                "pants_slot": [None],
                                "amulet_slot": [None],
                                "hand_slot": [None, None]
                                }
        self.parent = parent


    def can_equip(self, item):
        return True

    def can_unequip(self, item):
        return True

    def num_total_equipment_slots(self, slot):
        return len(self.equipment_slots[slot])

    def get_num_free_equipment_slots(self, slot):
        if slot not in self.equipment_slots:
            raise Exception("You are trying to find a {} in {}'s equipment slot".format(slot, self.parent.name))
        free_slots = 0
        for item in self.equipment_slots[slot]:
            if item is None:
                free_slots += 1
        return free_slots

    def add_item_to_equipment_slot(self, item, slot, num_slots):
        i = 0
        for item_slot in range(len(self.equipment_slots[slot])):
            if self.equipment_slots[slot][item_slot] is None:
                self.equipment_slots[slot][item_slot] = item
                return True
        raise Exception("You failed to equip an item to an equipment slot")

    def remove_item_from_equipment_slot(self, item, slot, num_slots):
        i = 0
        for item_slot in range(len(self.equipment_slots[slot])):
            if self.equipment_slots[slot][item_slot] is item:
                self.equipment_slots[slot][item_slot] = None
                i += 1
            if i >= num_slots:
                break
        if i >= num_slots:
            return True
        else:
            print("Something has probably gone wrong with unequipping if you reached this")
            return False

    def remove_equipment_slot(self, slot):
        if slot not in self.equipment_slots:
            raise Exception("You are trying to find a {} in {}'s equipment slot".format(slot, self.parent.name))
        try:
            self.equipment_slots[slot].remove(None)
        except:
            Exception("You tried to remove a {} in {}'s equipment slot but there was nothing that could be removed".format(slot, self.parent.name))
        return False

    def add_equipment_slot(self, slot):
        if slot not in self.equipment_slots:
            raise Exception("You are trying to find a {} in {}'s equipment slot".format(slot, self.parent.name))
        self.equipment_slots[slot].append(None)
        return True

    def get_items_in_equipment_slot(self, slot):
        carried = []
        if slot not in self.equipment_slots:
            raise Exception("You are trying to find a {} in {}'s equipment slot".format(slot, self.parent.name))
        else:
            for item in self.equipment_slots[slot]:
                if item != None:
                    carried.append(item)
        return carried

    def get_nth_item_in_equipment_slot(self, slot, n):
        items = self.get_items_in_equipment_slot(slot)
        if len(items) > n:
            return items[n]


    def equip(self, item, strength):
        slot = item.get_slot()
        if strength >= item.required_strength:
            self.unequip_current(item) # frees slots for current item
            self.add_item_to_equipment_slot(item, slot, item.slots_taken)
            item.equipped = True
            item.dropable = False
            if item.attached_skill_exists:
                self.parent.character.add_skill(item.attached_skill(self.parent))
            # item.activate(self.parent)


    def unequip_current(self, item):
        if item.has_trait("weapon"):
            self.unequip(self.get_weapon()) # if a weapon is already equipped, unequip it
            if item.slots_taken > 1: # two handed weapon 
                self.unequip(self.get_shield()) # if a shield is equipped in offhand, unequip it
        elif item.has_trait("shield"):
            self.unequip(self.get_shield())
            weapon = self.get_weapon()
            if weapon and weapon.slots_taken > 1: # two handed weapon must be unequipped for a shield
                self.unequip(weapon)
        elif item.has_trait("ring"):
            if self.get_num_free_equipment_slots("ring_slot") == 0:
                self.unequip(self.get_items_in_equipment_slot("ring_slot")[0])
                for slot in range(self.num_total_equipment_slots("ring_slot") - 1):
                    self.equipment_slots["ring_slot"][slot] = self.equipment_slots["ring_slot"][slot + 1]
                self.equipment_slots["ring_slot"][-1] = None
            

    def unequip(self, item):
        if item == None: # lets us call unequip with get_weapon
            return False
        slot = item.get_slot()
        self.remove_item_from_equipment_slot(item, slot, item.slots_taken)
        item.dropable = True
        item.equipped = False
        if item.attached_skill_exists:
            self.parent.character.remove_skill(item.attached_skill(self.parent))
        item.deactivate(self.parent)

    def get_weapon(self):
        carried_items = self.equipment_slots["hand_slot"]
        for item in carried_items:
            if item is not None and item.has_trait("weapon"):
                return item
        return None
    
    def get_shield(self):
        carried_items = self.equipment_slots["hand_slot"]
        for item in carried_items:
            if item is not None and item.has_trait("shield"):
                return item
        return None
    
    def get_in_slot(self, slot):
        carried_items = self.equipment_slots[slot]
        for item in carried_items:
            if item is not None:
                return item
        return None
