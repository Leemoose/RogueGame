import random
from navigation_utility import pathfinding

def rank_ungroup(ai, loop):
    player = loop.player
    x, y = ai.parent.x, ai.parent.y
    tile_map = loop.generator.tile_map
    monster_map = loop.generator.monster_map
    if player.get_distance(x, y) < 1.5:
        xplayer, yplayer = player.get_location()
        xdiff = xplayer - x
        ydiff = yplayer - y
        grouped = False
        goals = []
        if xdiff != 0:
            if (not tile_map.get_has_no_entity(x, y + 1) and not tile_map.get_has_no_entity(x,
                                                                                  y - 1) and not monster_map.get_has_no_entity(
                    x - xdiff, y)):
                ai.grouped = True
                goals = [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer + ydiff)]
            for position in [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer + ydiff)]:
                xposition, yposition = position
                if not monster_map.get_has_no_entity(xposition, yposition):
                    try:
                        monster = loop.generator.monster_dict.get_subject(
                            monster_map.track_map[xposition][yposition])
                        if monster.brain.grouped:
                            ai.grouped = True
                            xdiff = xplayer - monster.x
                            ydiff = yplayer - monster.y
                            goals = [(xplayer + xdiff, yplayer + ydiff)]
                            break
                    except:
                        return -1
        elif ydiff != 0:
            if not tile_map.get_has_no_entity(x - 1, y) and not tile_map.get_has_no_entity(x + 1,
                                                                                 y) and not monster_map.get_has_no_entity(
                    x, y - ydiff):
                ai.grouped = True
                goals = [(xplayer + 1, yplayer), (xplayer - 1, yplayer), (xplayer + xdiff, yplayer + ydiff)]
            for position in [(xplayer + 1, yplayer), (xplayer - 1, yplayer), (xplayer + xdiff, yplayer + ydiff)]:
                xposition, yposition = position
                if not monster_map.get_has_no_entity(xposition, yposition):
                    try:
                        monster = loop.generator.monster_dict.get_subject(
                            monster_map.track_map[xposition][yposition])
                        if monster.brain.grouped:
                            ai.grouped = True
                            xdiff = xplayer - monster.x
                            ydiff = yplayer - monster.y
                            goals = [(xplayer + xdiff, yplayer + ydiff)]
                            break
                    except:
                        return -1
        if (ai.grouped == True):
            ai.move_path = (pathfinding.astar_multi_goal(tile_map.get_map(), (x, y), goals,
                                                           monster_map, player, True, True))
            if len(ai.move_path) > 0:
                return random.randint(60, 100)
    return -1

def rank_combat(ai, loop):
    ai.target = None
    player = loop.player
    if ai.parent.get_distance(player.get_x(), player.get_y()) <= ai.parent.fighter.get_range() and loop.generator.tile_map.get_visible(ai.parent.get_x(), ai.parent.get_y()):
        ai.target = player
        return ai.randomize_action("combat")
    else:
        return -1

def rank_pickup(ai, loop):
    item_map = loop.generator.item_map
    monster = ai.parent
    if not item_map.get_has_no_entity(monster.x, monster.y):
        return ai.randomize_action("pickup")
    else:
        return -1

def rank_move(ai, loop):
    if ai.parent.get_distance(loop.player.get_x(), loop.player.get_y()) > 1.5:
        return ai.randomize_action("move")
    else:
        return -1

# def rank_stairs(ai, loop):
#     if loop.taking_stairs == True:
#         playerx, playery = loop.player.get_location()
#         monsterx, monstery = ai.parent.get_location()
#         if ai.parent.get_distance(playerx, playery) < 1.5 and loop.generator.tile_map.get_entity(playerx, playery).has_trait("stairs"):
#             ai.stairs_location = (playerx, playery)
#             return ai.randomize_action("stairs")
#     return -1

def rank_flee(ai, loop):
    # print("Does this monster have the flee condition? {}".format(ai.parent.flee))
    if ai.parent.character.get_flee() or ai.parent.character.get_health() / ai.parent.character.get_max_health() < .25:
        return ai.randomize_action("flee")  # must flee if flag is set
    return -1

def rank_find_item(ai, loop):
    if loop.generator.item_map.get_num_entities() > 0:
        return ai.randomize_action("find_item")
    return -1

def rank_wait(ai, loop):
    return ai.randomize_action("wait")


