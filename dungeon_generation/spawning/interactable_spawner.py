from .interact_init import InteractableSpawns

class InteractableSpawner():
    def __init__(self, InteractableSpawns):
        self.interact_spawn = InteractableSpawns

    def spawn_interactables(self, branch, depth):
        interacts = []
        for interact in self.interact_spawn:
            interact_new = interact.GetFreshCopy()
            interacts.append(interact_new)
        return interacts



interactable_spawner = InteractableSpawner(InteractableSpawns)