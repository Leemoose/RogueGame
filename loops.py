
import item_implementation
from dungeon_generation import mapping as M
import player
from navigation_utility import shadowcasting
from loop_workflow.loop_utility import *
from loop_workflow import MessageHandler, targets as T

from display_generation import *

"""
Theme: Loops is the central brain of which part of the program it is choosing.
Classes: 
    ColorDict --> Maps english to RGB colors
    ID --> Tags each unique entity (item, monster,etc) with an ID and puts subject in dict
    Memory --> Dictionary of everything important for saving
    Loops --> After input, controls what the game should do
"""


class Loops():
    """
    This is the brains of the game and after accepting an input from keyboard, will decide what needs to be done
    """

    def __init__(self, tileDict, display, keyboard, dungeon_data):
        self.display = display
        self.update_screen = True
        self.currentLoop = LoopType.none

        self.memory = Memory()
        self.tileDict = tileDict
        self.dungeon_data = dungeon_data
        self.keyboard = keyboard

        self.generator = None  # Dungeon Generator
        self.messages = MessageHandler()

        self.player = player.Player(0, 0)
        self.targets = T.Target(self)

        self.current_stat = 0  # index of stat for levelling up
        self.timer = 0

        self.quest_recieved = False
        self.quest_completed = False

        # variables for npc interaction
        self.next_dialogue = False # if true, give next dialogue box
        self.dialogue_options = 0 # number of dialogue options currently presented to player
        self.player_choice = -1 # if > 0, represents the dialogue option chosen by the player

        # variables for pathing
        self.rest_count = 0 # how many turns have you been resting for
        self.pathing_count = 0 # how many turns have you been exploring for
        dummy_function = (lambda x: False)
        self.after_pathing = dummy_function

        self.create_display_options = {LoopType.action: create_display,
                                       LoopType.targeting: create_display,
                                       LoopType.examine: create_display,
                                       LoopType.inventory: create_inventory,
                                       LoopType.enchant: create_inventory,
                                       LoopType.level_up: create_level_up,
                                       LoopType.victory: create_victory_screen,
                                       LoopType.equipment: create_equipment,
                                       LoopType.main: create_main_screen,
                                       LoopType.paused: create_pause_screen,
                                       LoopType.help: create_help_screen,
                                       LoopType.story: create_story_screen,
                                       LoopType.death: create_death_screen,
                                       LoopType.trade: create_trade_screen,
                                       LoopType.quest: create_quest_screen,
                                       LoopType.spell: create_spellcasting,
                                       LoopType.binding: create_binding_screen,
                                       LoopType.classes: create_class_screen,
                                       LoopType.spell_individual: create_spell_window,
                                       LoopType.quickcast: create_quickcast_select
                                       }
        self.update_display_options = {
                                       LoopType.victory: self.display.update_screen,
                                       LoopType.death: self.display.update_screen,
                                       LoopType.help: self.display.update_screen,
                                       LoopType.story: self.display.update_screen,
                                       LoopType.trade: self.display.update_screen_without_fill,
                                       LoopType.level_up: update_level_up,
                                       LoopType.equipment: self.display.update_screen,
                                       LoopType.main: self.display.update_main,
                                       LoopType.quest: self.display.update_screen_without_fill,
                                       LoopType.paused: self.display.update_screen_without_fill,
                                       LoopType.inventory: self.display.update_screen,
                                       LoopType.enchant: self.display.update_screen,
                                       LoopType.spell: self.display.update_screen,
                                       LoopType.binding: self.display.update_screen,
                                       LoopType.classes: self.display.update_screen,
                                       LoopType.spell_individual: update_spell_window,
                                       LoopType.quickcast: update_quickcast_select
                                       }
        self.action_options =          {LoopType.action: key_action,
                                       LoopType.inventory: key_inventory,
                                       LoopType.level_up: key_level_up,
                                       LoopType.victory: key_victory,
                                       LoopType.enchant: key_enchant,
                                       LoopType.equipment: key_equipment,
                                       LoopType.items: key_item_screen,#Need to do self.change_loop if change was made (put in keyboard)
                                       LoopType.examine: key_examine_screen,
                                       LoopType.targeting: key_targeting_screen,
                                       LoopType.specific_examine: key_specific_examine,
                                       LoopType.help: key_help,
                                       LoopType.story: key_help,
                                       LoopType.death: key_death,
                                       LoopType.main: key_main_screen,
                                       LoopType.paused: key_paused,
                                       LoopType.trade: key_trade,
                                       LoopType.quest: key_quest,
                                       LoopType.resting: key_rest,
                                       LoopType.pathing: key_explore,
                                       LoopType.spell: key_spell,
                                       LoopType.binding: key_binding,
                                       LoopType.spell_individual: key_spell_individual,
                                       LoopType.quickcast: key_quickselect
                                       }

        # Start the game by going to the main screen

    # Sets the internal loop type, and does the initialization that it needs.
    # Mostly here to cache UI pieces, which shouldn't be remade every frame.
    def change_loop(self, newLoop):
        if newLoop in get_loop_mapping_from_string():
            newLoop = get_loop_mapping_from_string()[newLoop]
        # self.clear_message()
        self.currentLoop = newLoop
        self.update_screen = True
        if newLoop in self.create_display_options:
            self.create_display_options[newLoop](self.display, self)
        elif newLoop == LoopType.items:
            self.display.update_entity(self, item_screen=True, create=True)

    def action_loop(self, keyboard, display):
        """
        This is responsible for undergoing any inputs when screen is clicked
        :param keyboard:
        :return: None (will do a keyboard action)
        """
        events = pygame.event.get()
        if events:
            for event in events:
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN or (event.type == pygame_gui.UI_BUTTON_PRESSED and hasattr(event.ui_element, "action")):
                    if event.type == pygame.KEYDOWN:
                        if event.mod == pygame.KMOD_NONE:
                            keyboard.set_next_key(keyboard.get_key_binding(event.key, False))
                        elif event.mod & pygame.KMOD_SHIFT and event.key:
                            keyboard.set_next_key(keyboard.get_key_binding(event.key, True))
                    else:
                        if hasattr(event.ui_element, "row"):
                            if event.ui_element.row != None:
                                self.current_stat = event.ui_element.row
                        keyboard.set_next_key(event.ui_element.action)
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    x_tile, y_tile = display.screen_to_tile(self.player, x, y)
                    if (self.currentLoop == LoopType.action):
                        keyboard.set_next_key(keyboard.get_key_from_mouse(self, x_tile, y_tile))
                    elif (self.currentLoop == LoopType.targeting):
                        keyboard.targetting_mouse_to_keyboard(self,x_tile,y_tile)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                elif event.type == pygame.VIDEORESIZE:
                    self.display.update_sizes()
                    self.update_screen = True
                    self.change_loop(self.currentLoop)
                display.uiManager.process_events(event)
        else:
            keys = pygame.key.get_pressed()
            keyboard.set_continous_movement_keys(keys)

        while keyboard.get_has_queue():
            key = keyboard.get_next_key()
            if self.currentLoop in self.action_options:
                if key != None and self.action_options[self.currentLoop](self, key) == False:
                    return False
            self.update_screen = True

        if self.currentLoop == LoopType.action:
            if self.pathing_count != 0:
                # print(f"Explored for {self.pathing_count} turns.")
                self.pathing_count = 0

                # default after pathing behaviour
                dummy_function = (lambda loop: loop.change_loop(LoopType.action))
                self.after_pathing = dummy_function

                # clear path if we go back to action
                self.player.path = []

        elif self.currentLoop == LoopType.resting:
            self.player.character.rest(self, LoopType.action)
        elif self.currentLoop == LoopType.pathing:
            self.player.autopath(self)
            self.pathing_count += 1
            self.time_passes(100)

        if self.player.character.energy < 0:
            self.time_passes(-self.player.character.energy)
            self.monster_loop(-self.player.character.energy)
            self.player.character.energy = 0

        if not self.player.character.is_alive() and not self.player.character.status.get_invincible():
            if (self.currentLoop != LoopType.death):
                self.change_loop(LoopType.death)

        # After everything, update the display clock
        display.update_ui()
        return True

    def monster_loop(self, energy):
        for monster in self.generator.monster_map.get_all_entities():
            if monster.character.is_alive():
                if monster.get_is_awake():
                    monster.character.energy += energy
                    while monster.character.energy > 0:
                        monster.brain.rank_actions(self)
                elif self.generator.tile_map.get_seen(monster.x, monster.y):
                    monster.character.status.set_awake(True)

    def render_screen(self, display):
        if self.currentLoop in self.update_display_options:
            self.update_display_options[self.currentLoop](self)
        else:
            if self.currentLoop == LoopType.action or self.currentLoop == LoopType.resting or self.currentLoop == LoopType.pathing:
                self.clean_up()
                shadowcasting.compute_fov(self)
                mos_x, mos_y = pygame.mouse.get_pos()
                (x, y) = display.screen_to_tile(self.player, mos_x, mos_y)  # Get the tile the mouse is on
                self.targets.set_target((x, y))
                display.update_display(self)
            elif self.currentLoop == LoopType.items:
                display.update_entity(self)
            elif self.currentLoop == LoopType.examine or self.currentLoop == LoopType.targeting:
                display.update_display(self)
                display.update_examine(self.targets.get_target_coordinates(), self)
            elif self.currentLoop == LoopType.specific_examine:
                display.update_entity(self, item_screen=False, create=True)
        if self.player.quest_recieved == True:
            display.update_questpopup_screen(self, "{} Recieved".format(self.player.quests[-1].name))
            self.player.quest_recieved = False

        pygame.display.update()
        self.update_screen = False

    def clean_up(self):
        destroyed_items = []
        for item in self.generator.item_map.get_all_entities():
            if item.destroy:
                destroyed_items.append(item)
        for item in destroyed_items:
            self.generator.item_map.remove_thing(item)

        dead_monsters = []
        for monster in self.generator.monster_map.get_all_entities():
            if not monster.character.is_alive():
                if monster.inventory.get_gold() > 0:
                    gold = item_implementation.Gold(monster.inventory.get_gold(), x = monster.get_x(), y= monster.get_y())
                    self.generator.item_map.place_thing(gold)
                items_copy = monster.get_inventory()
                for item in items_copy:
                    if item.equipped:
                        monster.character.unequip(item)
                    monster.do_drop(item, self.generator.item_map)
                dead_monsters.append(monster)
        for monster in dead_monsters:
            self.generator.monster_map.remove_thing(monster)



    def change_floor(self):
        playerx, playery = self.player.get_location()
        if self.player.character.energy < 0:
            self.time_passes(-self.player.character.energy)
            self.monster_loop(-self.player.character.energy)
            self.player.character.energy = 0

       # print("The stairs you are taking is {}".format(self.generator.tile_map.track_map[playerx][playery]))
        current_stairs = self.generator.tile_map.get_entity(playerx, playery)
        if current_stairs.has_trait("stairs"):
            new_level = self.get_depth() + current_stairs.get_level_change()
            new_generator = self.memory.get_saved_floor(self.get_branch(), new_level)
            if not current_stairs.get_has_paired_stairs():
                for other_stairs in new_generator.tile_map.get_stairs():
                    if (not other_stairs.get_has_paired_stairs() and other_stairs.get_level_change() != current_stairs.get_level_change()):
                        current_stairs.pair_stairs(other_stairs)
                        break
            self.player.x, self.player.y = (current_stairs.get_paired_stairs().get_location())
            self.player.visited_stairs = []
            self.generator = new_generator


    def init_game(self):
        dungeon_data = self.dungeon_data
        for branch in dungeon_data.get_branches():
            for level in range(1, dungeon_data.get_depth(branch) + 1):
                generator = M.DungeonGenerator(level, self.player, branch, dungeon_data)
                self.memory.set_floor("Dungeon",level, generator)

        self.memory.set_memory(1, "Dungeon", self.player, self.keyboard)
        self.generator = self.memory.get_current_saved_floor()

        for stairs in (self.generator.tile_map.get_stairs()):
            if stairs.get_level_change() == -1:
                x, y = stairs.get_location()
                self.player.x = x
                self.player.y = y
                self.targets.set_target((x, y))


    def start_targetting(self, start_on_player=False):
        self.change_loop(LoopType.targeting)
        if start_on_player or (self.targets.get_range() is not None and get_closest_monster(self).get_distance(self.targets.get_origin_range_coordinates()[0],
                                                                                                               self.targets.get_origin_range_coordinates()[1]) > self.targets.get_range()):
            target = self.player
        else:
            target = get_closest_monster(self)
        self.targets.set_target(target.get_location())

    def load_game(self):
        self.memory.load_objects()
        self.update_screen = False
        self.generator = self.memory.get_current_saved_floor()
        self.player = self.memory.player
        self.player.character.energy = 0
        self.change_loop(LoopType.action)
       # self.keyboard = self.memory.keyboard

    def clear_data(self):
        self.change_loop(LoopType.main)
        self.update_screen = True
        self.memory = Memory()
        self.generator = None
        self.messages.clear_message()

    def time_passes(self, time):
        self.timer += time
        for i in range(int(self.timer // 100)):
            self.player.statistics.add_turn_details()
            # do status effect stuff
            self.player.character.tick_all_status_effects(self)
            self.player.mage.tick_cooldowns()
            self.player.character.tick_regen()

            for quest in self.player.quests:
                quest.check_for_progress(self)

            if self.generator.tile_map.get_entity(self.player.x,self.player.y).has_terrain():
                self.generator.tile_map.get_entity(self.player.x,self.player.y).apply_terrain_effects(self.player)

            for monster in self.generator.monster_map.get_all_entities():
                monster.character.tick_all_status_effects(self)
                monster.character.tick_cooldowns()
                monster.character.tick_regen()

                if self.generator.tile_map.get_entity(monster.get_x(), monster.get_y()).has_terrain():
                    self.generator.tile_map.get_entity(monster.get_x(), monster.get_y()).apply_terrain_effects(monster)

        self.timer = self.timer % 100


    """
    These are passthrough functions
    """

    def get_branch(self):
        return self.generator.get_branch()

    def get_depth(self):
        return self.generator.get_depth()

    def get_width(self):
        return self.generator.get_width()

    def get_height(self):
        return self.generator.get_height()

    def add_message(self, message, color = (255,255,255)):
        self.messages.add_message(message, color)

    def clear_message(self):
        self.messages.clear_message()

    def set_target(self, target):
        self.targets.set_target(target)


