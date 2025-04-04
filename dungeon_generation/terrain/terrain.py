from objects import Objects
from global_vars import global_bugtesting
class Terrain(Objects):
    def __init__(self, x = -1, y = -1, effect = None, render_tag = -1, duration = 1, name = "Terrain"):
        super().__init__(x = x, y = y, render_tag = render_tag, name = name)
        self.traits["tile_effect"] = True
        self.effect = effect
        self.duration = duration

    def apply_effects(self, target):
        if self.effect is not None:
            target.character.status.add_status_effect(self.effect(self, duration = self.duration))
            if global_bugtesting:
                print(f"The terrain applied {self.effect} to {target.name}")

    def get_terrain_message(self):
        return f"The ground is covered in {self.name}"
