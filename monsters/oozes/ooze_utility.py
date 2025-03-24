from navigation_utility import pathfinding

# def rank_destroy_items_in_inventory(ai, loop):
#     if ai.parent.inventory.get_inventory_size() > 0:
#         return ai.randomize_action("destroy_items")
#     else:
#         return -1
#
# def do_destroy_items_in_inventory(ai, loop):
#     if ai.parent.inventory.get_inventory_size() > 0:
#         destroy_items = []
#         for item in ai.parent.get_inventory():
#             item.set_destroy(True)
#             destroy_items.append(item)
#             loop.add_message(f"{item.name} consumed by {ai.parent.name}")
#         for item in destroy_items:
#             ai.parent.inventory.remove_item(item)

def do_ooze_move(ai, loop):
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
                if loop.generator.item_map.get_has_entity(monster.get_x(), monster.get_y()):
                    item = loop.generator.item_map.get_entity(monster.get_x(), monster.get_y())
                    item.set_destroy(True)
                    loop.add_message(f"{item.name} consumed by {monster.name}")
        except:
            print("There was an exception thrown due to monster trying to move but there was only 1 move left...")
