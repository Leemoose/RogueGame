import random


def rank_burning_hands(ai, loop):
    if ai.parent.character.get_mana() > 5 and ai.parent.get_distance(loop.player.get_x(), loop.player.get_y() < 1.5):
        return ai.randomize_action("burning_hands")
    else:
        return -1

def do_burning_hands(ai, loop):
    ai.parent.mage.cast_spell(0, loop.player, loop)

def rank_combat(ai, loop):
    return -1

def rank_reposition(ai, loop):
    #Lots of complicated math, please don't change!
    if ai.parent.get_distance(loop.player.get_x(), loop.player.get_y() < 1.5):
        diffx, diffy = ai.parent.get_x() - loop.player.get_x(), ai.parent.get_y() - loop.player.get_y()
        if abs(diffx) + abs(diffy) == 1:
            for x in range(-abs(diffy),abs(diffy) * 2):
                if loop.generator.get_passable((x + ai.parent.get_x(), ai.parent.get_y() + diffy)):
                    return ai.randomize_action("reposition")
            for y in range(-abs(diffx), abs(diffx) * 2):
                if loop.generator.get_passable((diffx + ai.parent.get_x(), y + ai.parent.get_y())):
                    return ai.randomize_action("reposition")
        elif abs(diffx) + abs(diffy) == 2 and abs(diffx) == abs(diffy):
            if loop.generator.get_passable((diffx  + ai.parent.get_x(), diffy + ai.parent.get_y())):
                return ai.randomize_action("reposition")
            elif loop.generator.get_passable((diffx  + ai.parent.get_x(), (diffy + diffx) + ai.parent.get_y())):
                return ai.randomize_action("reposition")
            elif loop.generator.get_passable((diffx + diffy + ai.parent.get_x(), diffy + ai.parent.get_y())):
                return ai.randomize_action("reposition")
    return -1

def do_reposition(ai, loop):
    #Please don't change!
    if ai.parent.get_distance(loop.player.get_x(), loop.player.get_y() < 1.5):
        options = []
        diffx, diffy = ai.parent.get_x() - loop.player.get_x(), ai.parent.get_y() - loop.player.get_y()
        if abs(diffx) + abs(diffy) == 1:
            for x in range(-abs(diffy),abs(diffy) * 2):
                if loop.generator.get_passable((x + ai.parent.get_x(), ai.parent.get_y() + diffy)):
                    options.append((x,diffy))
            for y in range(-abs(diffx), abs(diffx) * 2):
                if loop.generator.get_passable((diffx + ai.parent.get_x(), y + ai.parent.get_y())):
                    options.append((diffx , y))
        elif abs(diffx) + abs(diffy) == 2 and abs(diffx) == abs(diffy):
            if loop.generator.get_passable((diffx + ai.parent.get_x(), diffy + ai.parent.get_y())):
                options.append((diffx, diffy))
            elif loop.generator.get_passable((diffx + ai.parent.get_x(), (diffy + diffx) + ai.parent.get_y())):
                options.append((diffx, diffy + diffx))
            elif loop.generator.get_passable((diffx + diffy + ai.parent.get_x(), diffy + ai.parent.get_y())):
                options.append((diffx + diffy, diffy))
        if len(options) > 0:
            move = random.choice(options)
            ai.parent.move(move[0], move[1], loop)


#
#
#
#         -1, 0: (-1,1)(-1,0)(-1,-1)
#         -1,1: (-2,2)(-2,1)(-1,2)