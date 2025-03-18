from navigation_utility import pathfinding

def do_nothing(ai, loop):
    # print("doing nothing")
    pass

def do_flee(ai, loop):
    # print("Fleeing")
    tile_map = loop.generator.tile_map
    monster = ai.parent
    monster_map = loop.generator.monster_map
    player = loop.player

    if not monster.character.can_take_action():
        monster.character.energy -= ai.parent.character.action_costs[
            "move"]  # (monster.character.move_cost - monster.character.dexterity)
        loop.add_message(f"{monster} is petrified and cannot move.")
        return

    update_target = False
    if loop.screen_focus == (monster.x, monster.y):
        update_target = True

    start = (monster.x, monster.y)
    end = (player.x, player.y)
    moves = pathfinding.astar(tile_map.get_map(), start, end, monster_map, loop.player)
    if len(moves) > 1:
        xmove, ymove = moves.pop(1)
        # if one direciton is blocked, still move in the other
        opposite_move = (-xmove + monster.x, -ymove + monster.y)
        if tile_map.get_passable(monster.x + opposite_move[0], monster.y + opposite_move[1]):
            monster.move(opposite_move[0], opposite_move[1], loop)
        elif tile_map.get_passable(monster.x, monster.y + opposite_move[1]):
            monster.move(0, opposite_move[1], loop)
        elif tile_map.get_passable(monster.x + opposite_move[0], monster.y):
            monster.move(opposite_move[0], 0, loop)
        else:
            monster.character.energy -= ai.parent.character.action_costs[
                "move"]  # (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} cowers in a corner since it can't run further.")
    if update_target:
        loop.add_target((monster.x, monster.y))
        loop.screen_focus = (monster.x, monster.y)

def do_ungroup(ai, loop):
    tile_map = loop.generator.tile_map
    monster = ai.parent
    monster_map = loop.generator.monster_map
    player = loop.player
    x, y = ai.parent.x, ai.parent.y

    if not monster.character.can_take_action():
        monster.character.energy -= ai.parent.character.action_costs[
            "move"]  # (monster.character.move_cost - monster.character.dexterity)
        loop.add_message(f"{monster} is petrified and cannot move.")
        return

    update_target = False
    if loop.target_to_display == (monster.x, monster.y):
        update_target = True

    if player.get_distance(monster.x, monster.y) <= 2.5:
        moves = ai.move_path
    if len(moves) > 1:
        xmove, ymove = moves.pop(1)
        monster.move(xmove - monster.x, ymove - monster.y, loop)
        ai.grouped = False
    if update_target:
        loop.add_target((monster.x, monster.y))

def do_item_pickup(ai, loop):
    # print("Picking up item")
    item = loop.generator.item_map.get_entity(ai.parent.get_x(), ai.parent.get_y())
    ai.parent.inventory.do_grab(item, loop)

def do_combat(ai, loop):
    # print("Attacking player")
    monster = ai.parent
    if not monster.character.can_take_action():
        monster.character.energy -= ai.parent.character.action_costs[
            "move"]  # (monster.character.move_cost - monster.character.dexterity)
        loop.add_message(f"{monster} is petrified and cannot attack.")
        return
    monster.character.energy -= ai.parent.character.action_costs["attack"]
    if ai.target != None:
        damage = monster.do_attack(ai.target, loop)
        loop.add_message(f"{monster} attacked {ai.target.name} for {damage} damage")
    else:
        loop.add_message(f"{monster.name} can find no suitable target to attack.")

# def do_use_consumeable(ai, loop):
#     # print("Using consumeable")
#     monster = ai.parent
#     if monster.inventory.get_inventory_size() != 0:
#         stuff = monster.get_inventory()
#         for i, item in enumerate(stuff):
#             if item.consumeable and item.equipment_type == "Potiorb":  # monster's can't read so no scrolls
#                 item.activate(monster.character)

def do_move(ai, loop):
    # print("Moving")
    tile_map = loop.generator.tile_map
    monster = ai.parent
    monster_map = loop.generator.monster_map
    player = loop.player

    if not monster.character.can_take_action():
        monster.character.energy -= ai.parent.character.action_costs[
            "move"]  # (monster.character.move_cost - monster.character.dexterity)
        loop.add_message(f"{monster} is petrified and cannot move.")
        return

    update_target = False
    if loop.screen_focus == (monster.x, monster.y):
        update_target = True
    if ai.target is not None:
        start = (ai.target.x, ai.target.y)
    else:
        start = (monster.x, monster.y)
    end = (player.x, player.y)
    if player.get_distance(monster.x, monster.y) <= 2.5:
        moves = pathfinding.astar(tile_map.get_map(), start, end, monster_map, loop.player, monster_blocks=True)
    else:
        moves = pathfinding.astar(tile_map.get_map(), start, end, monster_map, loop.player)
    if len(moves) > 1:
        try:
            xmove, ymove = moves.pop(1)
            #print(ai.parent.get_location(), "-->", end, "with", xmove - monster.x, ymove - monster.y)
            if loop.generator.get_passable((xmove, ymove)):
                monster.move(xmove - monster.x, ymove - monster.y, loop)
        except:
            print("There was an exception thrown due to monster trying to move but there was only 1 move left...")

    if update_target:
        loop.add_target((monster.x, monster.y))
        loop.screen_focus = (monster.x, monster.y)



def do_stairs(ai, loop):
    stairs = loop.generator.tile_map.get_entity(ai.stairs_location[0], ai.stairs_location[1])
    new_level = loop.generator.get_depth() + stairs.get_level_change()

    new_generator = loop.memory.get_saved_floor(loop.generator.get_branch(), new_level)
    new_stairs = stairs.get_paired_stairs()
    empty_tile = new_generator.get_nearest_empty_tile(new_stairs.get_location(), move=True)
    if empty_tile != None:
        loop.generator.monster_map.remove_thing(ai.parent)
        ai.parent.x = empty_tile[0]
        ai.parent.y = empty_tile[1]
        new_generator.monster_map.place_thing(ai.parent)
        ai.parent.character.energy = 0
        loop.add_message("The monster follows you on the stairs")


def do_find_item(ai, loop):
    monster = ai.parent
    distance = 1000
    item = None
    for temp_item in loop.generator.item_map.get_all_entities():
        temp_distance = monster.get_distance(temp_item.get_x(), temp_item.get_y())
        if temp_distance < distance:
            distance = temp_distance
            item = temp_item
    if item == None:
        return
    else:
        moves = pathfinding.astar(loop.generator.tile_map.get_map(), monster.get_location(), item.get_location(),
                                  loop.generator.monster_map.entity_map, loop.player)
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            monster.move(xmove - monster.x, ymove - monster.y, loop)
