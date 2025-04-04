from dungeon_generation.terrain import Web

def rank_spin_web(ai, loop):
    return ai.randomize_action("spin_web")

def do_spin_web(ai, loop):
    #need to remove energy
    x, y = ai.parent.get_location()
    loop.generator.tile_map.get_entity(x,y).add_terrain(Web())
    ai.parent.character.change_energy(-ai.parent.character.action_costs["spin_web"])
    loop.add_message(f"{ai.parent.name} spins a web at {x}, {y}")
    ai.set_tendency("spin_web", (-1,0))