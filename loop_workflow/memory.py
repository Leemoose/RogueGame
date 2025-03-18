import dill

class Memory():
    """
    Used to save the game
    """
    def __init__(self):
        self.explored_levels = 0
        self.floor_level = 0
        self.branch = ""
        self.generators = {}
        self.player = None
        self.keyboard = None

    def get_saved_floor(self, branch, depth):
        return self.generators[branch][depth]

    def get_current_saved_floor(self):
        return self.generators[self.branch][self.floor_level]

    def set_floor(self, branch, depth, generator):
        if branch not in self.generators:
            self.generators[branch] = {}
        self.generators[branch][depth] = generator

    def set_memory(self, explored_levels, floor_level, branch, player, keyboard):
        self.explored_levels = explored_levels
        self.floor_level = floor_level
        self.branch= branch
        self.player = player
        self.keyboard = keyboard

    def save_objects(self):
        save = [self.explored_levels, self.floor_level, self.generators, self.player, self.branch, self.keyboard]
        try:
            with open("data.dill", "wb") as f:
                print("Saved the game")
                dill.dump(save, f)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

    def load_objects(self):
        with open('data.dill', 'rb') as f:
            # Call load method to deserialze
            print("Loaded the game")
            save = dill.load(f)
        self.explored_levels = save[0]
        self.floor_level = save[1]
        self.generators = save[2]
        self.player = save[3]
        self.branch = save[4]
        self.keyboard = save[5]
