from monsters.monster import Monster
from .skeleton_ai import Skeleton_AI

class Skeleton(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1050, name="Skeleton", experience_given = 10):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name, experience_given=experience_given)
        self.description = ""
        self.traits["skeleton"] = True
        self.brain = Skeleton_AI


