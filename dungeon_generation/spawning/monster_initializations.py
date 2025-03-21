from monsters import Ooze, Goblin, Kobold

from .spawn_params import MonsterSpawnParams

MonsterSpawns = []

# all branches
# MonsterSpawns.append(MonsterSpawnParams(M.Slime(), group="slime", minFloor=1, maxFloor=4))

# early floors dungeon only
MonsterSpawns.append(MonsterSpawnParams(Ooze(-1, -1), minFloor=2, maxFloor=10))

# goblin type monsters dungeon only
MonsterSpawns.append(MonsterSpawnParams(Goblin(-1, -1), group="goblin", minFloor=2, maxFloor=10))
MonsterSpawns.append(MonsterSpawnParams(Kobold(-1, -1), group="kobold", minFloor=1, maxFloor=10))
# MonsterSpawns.append(MonsterSpawnParams(M.Hobgoblin(-1, -1), minFloor=1, maxFloor=4, rarity="Rare", group="goblin"))
# MonsterSpawns.append(MonsterSpawnParams(M.Looter(), group="goblin", minFloor=1, maxFloor=4))
# #MonsterSpawns.append(MonsterSpawnParams(M.GoblinShaman(-1, -1), group="goblin"))
#
#
# # middle floors
# MonsterSpawns.append(MonsterSpawnParams(M.Gargoyle(-1, -1), group="gargoyle", minFloor=5, maxFloor=7))
# MonsterSpawns.append(MonsterSpawnParams(M.Minotaur(-1, -1), minFloor=5, maxFloor=7))
# MonsterSpawns.append(MonsterSpawnParams(M.Orc(-1, -1), group="orc", minFloor=5, maxFloor=7))
# MonsterSpawns.append(MonsterSpawnParams(M.Bobby(), group="orc", rarity="rare", minFloor=5, maxFloor=7))
#
# # forest branch
# MonsterSpawns.append(MonsterSpawnParams(M.Twiggy(), minFloor=1, maxFloor=3, branch="Forest")) # maybe move to forest branch
# MonsterSpawns.append(MonsterSpawnParams(M.Stumpy(), minFloor=2, maxFloor=4, branch="Forest")) # maybe move to forest branch
# MonsterSpawns.append(MonsterSpawnParams(M.Treant(), minFloor=3, maxFloor=5, branch="Forest")) # maybe move to forest branch
# MonsterSpawns.append(MonsterSpawnParams(M.MetallicBear(), minFloor=3, maxFloor=5, branch="Forest")) # maybe move to forest branch
# MonsterSpawns.append(MonsterSpawnParams(M.Spider(), minFloor=1, maxFloor=5, branch="Forest")) # maybe move to forest branch
# MonsterSpawns.append(MonsterSpawnParams(M.InsectNest(), minFloor=1, maxFloor=5, branch="Forest")) # maybe move to forest branch
# MonsterSpawns.append(MonsterSpawnParams(M.Vinecrasher(), minFloor=1, maxFloor=5, branch="Forest")) # maybe move to forest branch
#
#
# # late floors
# MonsterSpawns.append(MonsterSpawnParams(M.Raptor(-1, -1), minFloor=8, maxFloor=10, group="dinosaur")) # maybe move to forest branch
# MonsterSpawns.append(MonsterSpawnParams(M.Tormentorb(-1, -1), minFloor=8, maxFloor=10))
# MonsterSpawns.append(MonsterSpawnParams(M.Golem(-1, -1), minFloor=8, maxFloor=10))
#
# # TEMPORARY CHANGE TO TEST TILE RESTRICTED MONSTERS
# MonsterSpawns.append(MonsterSpawnParams(M.Squid(), minFloor=1, maxFloor=1, branch="Ocean"))
# MonsterSpawns.append(MonsterSpawnParams(M.Leviathon(), minFloor=1, maxFloor=1, branch="Ocean"))
# MonsterSpawns.append(MonsterSpawnParams(M.ChasmCrawler(), minFloor=1, maxFloor=1, branch="Ocean"))
#
#
# # boss spawning
# MonsterSpawns.append(BossSpawnParams(M.BossOrb(-1, -1), depth=10))