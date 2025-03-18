import random
def get_random_direction():
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    return random.choice(directions)

def place_spawn_monsters(dungeongenerator, monster_spawner):
    monsterSpawns = monster_spawner.spawnMonsters(dungeongenerator.get_depth(), dungeongenerator.get_branch())
    for monster in monsterSpawns:
        if type(monster) == list:
            place_pack(dungeongenerator, monster)
        else:
            place_spawn_monster(dungeongenerator, monster)

def place_spawn_monster(dungeongenerator, creature):
    # if dungeongenerator.spawn_params.check_monster_restrictions != None:
    #     def monster_restriction(location):
    #         return dungeongenerator.spawn_params.check_monster_restrictions(creature, dungeongenerator.tile_map, location, dungeongenerator)
    # else:
    x, y = dungeongenerator.get_random_location(condition=None)
    dungeongenerator.place_monster_at_location(creature, x, y)

def place_pack(dungeongenerator, pack):
    pack_size = len(pack)
    count = 0
    iters = 0

    area_to_check = 2 # check all tiles in radius 2 (this technically caps pack size at 25, up this area if any dungeon has a higher max pack size)
    directions = [(dx, dy) for dx in range(-1 * area_to_check, area_to_check + 1) for dy in range(-1 * area_to_check, area_to_check + 1)]

    while count < pack_size:
        x, y = dungeongenerator.get_random_location()
        locations = []
        count = 0
        random.shuffle(directions) # varies the arangement of packs

        for (dx, dy) in directions:
            if dungeongenerator.get_passable((x + dx, y + dy)):
                locations.append((x + dx, y + dy))
                count += 1
                # break early as soon as we find a location that can fit the full pack
                if count >= pack_size:
                    break

    for i, monster in enumerate(pack):
        if i >= len(locations):
            import pdb; pdb.set_trace()
        x, y = locations[i]
        dungeongenerator.place_monster_at_location(monster, x, y)

def place_spawn_statics(dungeongenerator):
    for x in range(dungeongenerator.get_width()):
        for y in range(dungeongenerator.get_height()):
            if dungeongenerator.tile_map.get_entity(x,y).has_trait("npc_spawn"):
                dungeongenerator.interact_map.place_thing(dungeongenerator.tile_map.get_entity(x,y).spawn_entity())
            elif dungeongenerator.tile_map.get_entity(x,y).has_trait("monster_spawn"): # this is used for static monster spawns
                dungeongenerator.place_monster_at_location(dungeongenerator.tile_map.get_entity(x,y).spawn_entity(), x, y)
            elif dungeongenerator.tile_map.get_entity(x,y).has_trait("item_spawn"): # this is used for static monster spawns
                dungeongenerator.place_item_at_location(dungeongenerator.tile_map.get_entity(x,y).spawn_entity(), x, y)

def place_spawn_interactables(dungeongenerator, interactable_spawner):
    interactable_spawns = interactable_spawner.spawn_interactables(dungeongenerator.get_depth(), dungeongenerator.get_branch())
    first = True
    force_near_stairs = False
    for interactable in interactable_spawns:
        dungeongenerator.place_interactable(interactable)

def place_spawn_interactable(dungeongenerator, interactable, force_near_stairs=False):
    startx = random.randint(0, dungeongenerator.get_width() - 1)
    starty = random.randint(0, dungeongenerator.get_height() - 1)
    map = dungeongenerator.interact_map

    # make sure the item is placed on a passable tile that is not stairs or in a corridor
    check_on_stairs = dungeongenerator.get_is_on_stairs(startx, starty)
    check_in_corridor = dungeongenerator.get_is_in_corridor(startx, starty)
    while ((not dungeongenerator.tile_map.get_has_no_entity(startx, starty)) or
               (not map.get_has_no_entity(startx, starty)) or
               check_on_stairs or check_in_corridor):
            startx = random.randint(0, dungeongenerator.get_width() - 1)
            starty = random.randint(0, dungeongenerator.get_height() - 1)
            check_on_stairs = dungeongenerator.on_stairs(startx, starty)
            check_in_corridor = dungeongenerator.get_is_in_corridor(startx, starty)

    dungeongenerator.place_interactable_at_location(interactable, startx, starty)

def place_spawn_items(dungeongenerator, item_spawner ):
    itemSpawns = item_spawner.spawnItems(dungeongenerator.get_depth(), dungeongenerator.get_branch())
    first = True
    force_near_stairs = False
    for item in itemSpawns:
        if first and dungeongenerator.get_depth() == 2:
            # manually force a weapon to spawn near the stairs on the second floor
            force_near_stairs = True
            first = False # only do so for first item
        place_spawn_item(dungeongenerator, item, force_near_stairs)
        force_near_stairs = False

def place_spawn_item(dungeongenerator, item, force_near_stairs=False):
    startx = random.randint(0, dungeongenerator.get_width() - 1)
    starty = random.randint(0, dungeongenerator.get_height() - 1)

    # make sure the item is placed on a passable tile that does not already have an item and is not stairs
    check_on_stairs = dungeongenerator.get_is_on_stairs(startx, starty)
    if force_near_stairs:
        while ((dungeongenerator.get_passable((startx, starty)) == False) or
               (dungeongenerator.item_map.get_has_no_entity(startx, starty) == False)):
            random_direction = get_random_direction()
            startx = dungeongenerator.tile_map.stairs[1].x + random_direction[0]
            starty = dungeongenerator.tile_map.stairs[1].y + random_direction[1]
    else:
        while (not dungeongenerator.get_passable((startx, starty)) or dungeongenerator.get_is_on_stairs(startx, starty)):
            startx = random.randint(0, dungeongenerator.get_width() - 1)
            starty = random.randint(0, dungeongenerator.get_height() - 1)

    dungeongenerator.place_item_at_location(item, startx, starty)

