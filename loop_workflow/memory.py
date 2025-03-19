import dill

class Memory():
    """
    Used to save the game
    """
    def __init__(self):
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

    def set_memory(self, floor_level, branch, player, keyboard):
        self.floor_level = floor_level
        self.branch= branch
        self.player = player
        self.keyboard = keyboard

    def update_memory(self, floor_level, branch):
        self.floor_level = floor_level
        self.branch = branch
        self.save_objects()

    def save_objects(self):
        save = [self.floor_level, self.generators, self.player, self.branch, self.keyboard]
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
        self.floor_level = save[0]
        self.generators = save[1]
        self.player = save[2]
        self.branch = save[3]
        self.keyboard = save[4]
        print("Floor: {}, Branch: {}".format( self.floor_level, self.branch))
