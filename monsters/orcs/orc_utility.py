from spell_implementation.effects.berserk import Berserk
def rank_berserk(ai, loop):
    if ai.parent.character.get_health() / ai.parent.character.get_max_health() < .25:
        return ai.randomize_action("berserk")
    return -1

def do_berserk(ai, loop):
    ai.parent.character.status.add_status_effect(Berserk(5))
    ai.tendencies["berserk"] = (-1,0)