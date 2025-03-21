

def rank_burning_hands(ai, loop):
    if ai.get_mana() > 5 and ai.parent.get_distance(loop.player.get_x(), loop.player.get_y() < 1.5):
        return ai.randomize_action("burning_hands")
    else:
        return -1

def do_burning_hands(ai, loop):
    return

# def rank_reposition(ai, loop):
#     options = []
#     if ai.parent.get_distance(loop.player.get_x(), loop.player.get_y() < 1.5):
#         diffx, diffy = ai.parent.get_x() - loop.player.get_x(), ai.parent.get_y() - loop.player.get_y()
#         if abs(diffx) + abs(diffy) == 1:
#             for x in range(-abs(diffy),abs(diffy)):
#                 if loop.generator.get_passable(x, diffy):
#                     options.append((x, diffy))
#             for y in range(-abs(diffx), abs(diffx)):
#                 if loop.generator.get_passable(diffx, y):
#                     options.append((diffx, y))
#         else:
#
#
#
#
#         -1, 0: (-1,1)(-1,0)(-1,-1)
#         -1,1: (-2,2)(-2,1)(-1,2)