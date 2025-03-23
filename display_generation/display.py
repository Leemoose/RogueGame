from .ui import *
import pygame
import pygame_gui
from loop_workflow.loop_utility import LoopType
from pygame import image
import warnings


class Display:
    """
    Display is responsible for put images in the screen. Currently have it set that each function will update a
    seperate part of the game.
    """
    def __init__(self, width, height, textSize, textWidth, textHeight):
        pygame.display.set_caption('Tiles')
        self.win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen_width = width
        self.screen_height = height
        self.textWidth = textWidth
        self.textHeight = textHeight
        self.textSize = textSize

        action_screen_width = self.screen_width * 3 // 4
        action_screen_height = self.screen_height * 5 // 6
        num_tiles_wide = action_screen_width // self.textSize
        num_tiles_height = action_screen_height // self.textSize
        self.r_x = num_tiles_wide // 2
        self.r_y = num_tiles_height // 2

        self.uiManager = pygame_gui.UIManager((width, height), "./assets/theme.json")
        self.windows = []
        self.clock = pygame.time.Clock()
        self.colorDict = None
        self.depth_label = None

        self.quest_number = -1

    def get_tile_screen_center(self):
        return (self.r_x, self.r_y)

    def get_tile_size(self):
        return self.textSize

    def get_pixel_location_from_entity_location(self, entity):
        return (self.textSize*(entity.get_x() - self.x_start), self.textSize*(entity.get_y() - self.y_start))
        

    def screen_to_tile(self, player, x, y):
        xplayerscreen, yplayerscreen = self.r_x * self.textSize + self.textSize // 2, self.r_y * self.textSize + self.textSize // 2
        xdiff = x - xplayerscreen + 10
        ydiff = y - yplayerscreen + 10
        return (player.x + xdiff // self.textSize, player.y + ydiff//self.textSize)

    def update_sizes(self):
        self.screen_width, self.screen_height = self.win.get_size()

    def update_main(self, loop):
        # Main Screen
        self.win.fill((0, 0, 0))
        image_offset_from_left = 0
        image_offset_from_top = 0
        self.win.blit(pygame.transform.scale(pygame.image.load('assets/titlescreen1.jpeg'),
                                             (self.screen_width, self.screen_height)), (image_offset_from_left, image_offset_from_top))
        self.uiManager.draw_ui(self.win)

        font = pygame.font.Font('freesansbold.ttf', 12)

    def draw_player(self, loop):
        tileDict = loop.tileDict
        player = loop.player
        player_pixel_x, player_pixel_y = self.get_pixel_location_from_entity_location(player)
        #Draw base character depending on armor state
        self.win.blit(tileDict.tile_string(player.get_render_tag()), (player_pixel_x, player_pixel_y)) # DONG MODE ENGAGED
        #Draw item_implementation on top
        if player.body.get_num_free_equipment_slots("boots_slot") == 0:
            self.win.blit(tileDict.tile_string(5200), (player_pixel_x, player_pixel_y))
        if player.body.get_num_free_equipment_slots("gloves_slot") == 0:
            self.win.blit(tileDict.tile_string(5100), (player_pixel_x, player_pixel_y))
        if player.body.get_num_free_equipment_slots("helmet_slot") == 0:
            self.win.blit(tileDict.tile_string(5300), (player_pixel_x, player_pixel_y))
        if player.body.get_num_free_equipment_slots("body_armor_slot") == 0:
            self.win.blit(tileDict.tile_string(5400), (player_pixel_x, player_pixel_y))
        if player.body.get_num_free_equipment_slots("pants_slot") == 0:
            self.win.blit(tileDict.tile_string(5500), (player_pixel_x, player_pixel_y))

    def update_display(self, loop):
        self.win.fill((0,0,0))
        tile_map = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        item_map = loop.generator.item_map
        player = loop.player

        action_screen_width = self.screen_width * 4 // 5
        action_screen_height = self.screen_height * 5 // 6
        num_tiles_wide = action_screen_width // self.textSize
        num_tiles_height = action_screen_height // self.textSize

        self.r_x = num_tiles_wide // 2
        self.r_y = num_tiles_height // 2

        self.x_start = player.x - self.r_x
        self.x_end = player.x + self.r_x
        self.y_start = player.y - self.r_y
        self.y_end = player.y + self.r_y

        mini_map_left_offset = action_screen_width
        mini_map_top_offset = self.screen_height // 3
        mini_map_width = self.screen_width - action_screen_width
        mini_map_height = self.screen_height // 3

       #Making all the tiles
        for x in range(self.x_start, self.x_end):
            for y in range(self.y_start, self.y_end):
                tile = tile_map.get_entity(x, y)
                if tile != -1:
                    self.draw_single_tile(loop, tile)
        for item in item_map.get_all_entities():
            self.draw_single_entity(loop, item)
        for monster in monster_map.get_all_entities():
            self.draw_single_entity(loop, monster)

        self.draw_player(loop)
        self.uiManager.draw_ui(self.win)
        self.update_mini_map(loop, mini_map_left_offset, mini_map_top_offset, mini_map_width, mini_map_height, num_tiles_wide, num_tiles_height)
        self.draw_examine_window(loop, loop.targets.get_target_coordinates())
        self.draw_health_and_mana_orbs(loop)

        self.depth_label.update(1)

    def draw_health_and_mana_orbs(self, loop):
        health_orb_size = 128
        health_orb_x = self.screen_width // 3
        health_orb_y = self.screen_height - health_orb_size * 2
        entity_image = pygame.transform.scale(image.load("assets/status_orbs/health_full.png"),(health_orb_size, health_orb_size))
        self.win.blit(entity_image, (health_orb_x, health_orb_y))
        entity_image = pygame.transform.scale(image.load("assets/status_orbs/itsmars_orb_highlight.png"),(health_orb_size, health_orb_size))
        self.win.blit(entity_image, (health_orb_x, health_orb_y))
        entity_image = pygame.transform.scale(image.load("assets/status_orbs/itsmars_orb_shadow.png"),
                                              (health_orb_size, health_orb_size))
        self.win.blit(entity_image, (health_orb_x, health_orb_y))


    def draw_single_entity(self, loop, entity):
        if entity.get_is_in_square(self.x_start, self.x_end, self.y_start, self.y_end):
            if loop.generator.tile_map.get_visible(entity.get_x(), entity.get_y()):
                entity_tile = loop.tileDict.tile_string(entity.get_render_tag())
                self.win.blit(entity_tile,self.get_pixel_location_from_entity_location(entity))

    #HORRIBLE HACK - THIS IS ALSO DEFINED IN UI.PY - KEEP THEM SYNCED!
    def update_mini_map(self, loop, left_offset, top_offset, width, height, num_tiles_wide, num_tiles_height):
        player = loop.player
        map_tile_size = 5
        num_map_tiles_wide = width // map_tile_size
        num_map_tiles_height = height // map_tile_size
        r_map_x = num_map_tiles_wide // 2
        r_map_y = num_map_tiles_height // 2
        x_map_start = player.x - r_map_x
        x_map_end = player.x + r_map_x
        y_map_start = player.y - r_map_y
        y_map_end = player.y + r_map_y

        floormap = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        item_map = loop.generator.item_map

        # Making all map tiles
        for x in range(x_map_start, x_map_end):
            for y in range(y_map_start, y_map_end):
                if floormap.in_map(x, y) and floormap.get_entity(x, y).get_seen():
                    rectangle = pygame.Rect(left_offset + map_tile_size * (x - x_map_start),
                                            top_offset + map_tile_size * (y - y_map_start),
                                            map_tile_size, map_tile_size)
                    if floormap.get_entity(x, y).is_passable():
                        if floormap.get_entity(x, y).get_visible() and monster_map.get_has_entity(x, y):
                            pygame.draw.rect(self.win, (207, 207, 207), rectangle)
                        elif item_map.get_has_entity(x, y):
                            pygame.draw.rect(self.win, (0, 200, 0), rectangle)
                        elif floormap.get_entity(x, y).has_trait("stairs"):
                            pygame.draw.rect(self.win, (0, 0, 200), rectangle)
                        elif floormap.get_entity(x, y).has_trait("gateway"):
                            pygame.draw.rect(self.win, (0, 75, 100), rectangle)
                        else:
                            pygame.draw.rect(self.win, (131, 131, 131), rectangle)
                        #     for interact in interact_map.all_entities():
                        #         if floormap.track_map[interact.x][interact.y].seen:
                        #             pygame.draw.rect(self.win, (200, 100, 0),rectangle)
                    else:
                        pygame.draw.rect(self.win, (100, 100, 100), rectangle)
        pygame.draw.rect(self.win, (150, 100, 50),
                         pygame.Rect(left_offset + r_map_x * map_tile_size,
                                     top_offset + r_map_y * map_tile_size,
                                     map_tile_size, map_tile_size))
        pygame.draw.rect(self.win, (150, 100, 50),
                         pygame.Rect(left_offset + (num_map_tiles_wide - num_tiles_wide) * map_tile_size // 2,
                                     top_offset + (
                                                 num_map_tiles_height - num_tiles_height) * map_tile_size // 2,
                                     num_tiles_wide * map_tile_size, num_tiles_height * map_tile_size), 1)


    def write_messages(self, messages):
        font = pygame.font.Font('freesansbold.ttf', 12)
        for i, message in enumerate(messages):
            text = font.render(message[0], True, message[1])
            self.win.blit(text, (self.screen_width // 100 * 12, self.screen_height // 100 * (85 + i * 3)))

    def draw_examine_window(self, loop, target):
        tileDict = loop.tileDict
        floormap = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        item_map = loop.generator.item_map
        player = loop.player
        examine_offset_from_left = 10
        examine_offset_from_top = 10
        if target is not None:
            x, y = target
            if loop.generator.in_map(x, y) and floormap.get_entity(x,y).visible:
                # black_screen = pygame.transform.scale(pygame.image.load("assets/ui/black_screen.png"), (self.screen_width // 5, self.screen_height // 5))
                # self.win.blit(black_screen, (0, 0))
                font = pygame.font.Font('freesansbold.ttf', 12)

                # find monster at target
                if monster_map.get_has_entity(x,y):
                    monster = monster_map.get_entity(x,y)
                    # draw monster
                    tag = tileDict.tile_string(monster.get_render_tag())
                    self.win.blit(tag, (examine_offset_from_left, examine_offset_from_top))

                    for i, descriptor in enumerate(monster.get_string_description()):
                        text = font.render(descriptor, True, (255, 255, 255))
                        self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 50 + i * 15))

                elif item_map.get_has_entity(x,y):
                    # find item at target
                    top_offset_item = 0
                    for item in item_map.get_all_entities():
                        count = 0
                        if item.get_distance(x, y) == 0 and count < 6:
                            # draw item
                            tag = tileDict.tile_string(item.get_render_tag())
                            self.win.blit(tag, (examine_offset_from_left, examine_offset_from_top + top_offset_item + 20))

                            for descriptor in item.get_string_description():
                                text = font.render(descriptor, True, (255, 255, 255))
                                self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 50 + top_offset_item))
                                top_offset_item += 15
                            top_offset_item += 30

                elif player.get_distance(x, y) == 0:
                    tag = tileDict.tile_string(player.get_render_tag())
                    self.win.blit(tag, (examine_offset_from_left, examine_offset_from_top))

                    # random flavor text since detailed player info is elsewhere
                    text = font.render("You", True, (255, 255, 255))
                    self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 50))
                else:
                    return False
                return True
        return False

    def draw_on_button(self, button, img, letter="", button_size=None, shrink=False, offset_factor = 10, text_offset = (15, 0.8)):
        offset = (0, 0)
        if shrink:# shrink weapon image a bit
            img = pygame.transform.scale(img, (button_size[0] // 5 * 4, button_size[1] // 5 * 4))
            offset = (button_size[0] // offset_factor, button_size[1] // offset_factor)
        button.drawable_shape.states['normal'].surface.blit(img, offset)
        button.drawable_shape.states['hovered'].surface.blit(img, offset)
        button.drawable_shape.states['disabled'].surface.blit(img, offset)
        button.drawable_shape.states['selected'].surface.blit(img, offset)
        button.drawable_shape.states['active'].surface.blit(img, offset)
        if button_size:
            font_size = 20
            font = pygame.font.Font('freesansbold.ttf', font_size)
            text = font.render(letter, True, (255, 255, 255))
            button.drawable_shape.states['normal'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['hovered'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['disabled'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['selected'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['active'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
        button.drawable_shape.active_state.has_fresh_surface = True
        # button.drawable_shape.redraw_all_states()


    def refresh_screen(self):
        self.uiManager.clear_and_reset()

    def stat_text(self, entity, stat):
        return str(stat)

    def stat_modifier(self, entity, stat):
        if stat >= 0:
            return "+" + str(stat)
        else:
            return str(stat)


    def draw_character_stats(self, player, margin_from_left, margin_from_top, width, height):
        if player.character.get_strength() >= 0:
            strength_modifier = "+" + str(player.character.get_strength())
        else:
            strength_modifier = str(player.character.get_strength())
        weapon = player.body.get_weapon()
        
        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((margin_from_left, margin_from_top), (width, height)),
            
            html_text = "Player<br><br>"
                        "Stats<br>"
                        "Strength: " + self.stat_text(player, player.character.get_strength()) + "<br>"
                        "Dexterity: " + self.stat_text(player, player.character.get_dexterity()) + "<br>"
                        "Endurance: " + self.stat_text(player, player.character.get_endurance()) + "<br>"
                        "Intelligence: " + self.stat_text(player, player.character.get_intelligence()) + "<br>" +
                        "Health: " + str(player.character.get_health()) + " / " + str(player.character.get_max_health()) + "<br>"
                        "Mana: " + str(player.character.get_mana()) + " / " + str(player.character.get_max_mana()) + "<br>"
                        "<br>"
                        "Damage: " + str(player.fighter.get_damage_min()) + " - " + str(player.fighter.get_damage_max()) + " (" + strength_modifier + ") <br>"
                        "Defense: " + str(player.fighter.get_armor()) + " (+" + str(player.character.get_endurance() // 3) + ") <br>"
                        "Movement Delay: " + str(player.character.action_costs["move"]) + "<br>"
                        "Skill Damage Bonus: " + str(player.character.skill_damage_increase()) + "<br>"
                        "Effect Duration Bonus: " + str(player.character.skill_duration_increase()) + "<br>"
                        "<br>Known Skills:<br>"
                        + "<br>".join([str(i + 1) + ". " + skill.description() for i, skill in enumerate(player.mage.known_spells)])
                        ,
            manager=self.uiManager
        )

    def draw_empty_box(self, margin_from_left, margin_from_top, width, height):
        box = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((margin_from_left, margin_from_top), (width, height)),
            manager=self.uiManager
        )

    def draw_escape_button(self, windowX, windowY, window_width, window_height):
        buttonWidth = 40
        buttonHeight = 40

        buttonX = windowX + window_width - buttonWidth
        buttonY = windowY

        esc_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((buttonX, buttonY), (buttonWidth, buttonHeight)),
            text="X",
            manager=self.uiManager,
            starting_height=1000)
        esc_button.action = "esc"


    def update_entity(self, loop, item_screen = True, create = False):
        entity = loop.targets.get_target()
        tileDict = loop.tileDict
        player = loop.player
        if create == True:
            self.uiManager.clear_and_reset()
        self.win.fill((0,0,0))
        entity_screen_width = self.screen_width // 2
        entity_screen_height = self.screen_height // 2
        entity_offset_from_left = self.screen_width // 4
        entity_offset_from_top = self.screen_height // 4

        entity_message_width = self.screen_width // 2
        entity_message_height = self.screen_height // 10
        entity_message_offset_from_left = self.screen_width // 4
        entity_message_offset_from_top = self.screen_height  // 4

        entity_image_width = self.screen_width // 20
        entity_image_height = self.screen_width // 20
        entity_image_offset_from_left = self.screen_width // 4 + self.screen_width // 50
        entity_image_offset_from_top = self.screen_height // 4

        entity_button_width = self.screen_width // 10
        entity_button_height = self.screen_height // 30
        entity_button_offset_from_left = (self.screen_width) // 2 - entity_button_width * 3 //2
        entity_button_offset_from_top = entity_screen_height + entity_offset_from_top - entity_button_height - self.screen_height // 50
        entity_button_offset_from_each_other =  entity_button_width // 2

        entity_text_offset_from_left = entity_offset_from_left + entity_screen_width // 20
        entity_text_offset_from_top = entity_image_offset_from_top + entity_message_height
        entity_text_width = entity_screen_width * 11 // 12
        entity_text_height = entity_screen_height * 3 // 5

        buttons_drawn = 0

        entity_image = pygame.transform.scale(tileDict.tiles[entity.render_tag],
                                     (entity_image_width, entity_image_height))

        pygame.draw.rect(self.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))

        self.win.blit(entity_image, (entity_image_offset_from_left, entity_image_offset_from_top))

        if (create == True):
            self.draw_escape_button(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height)

        entity_name = entity.name
        if create == True:
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                          (entity_message_width, entity_message_height)),
                text=entity_name,
                manager=self.uiManager,
                object_id='#title_small')

        if item_screen:
            item = entity
            show = False
            if item.can_be_levelled:
                item_level = item.level
                if item_level > 1:
                    addition = " (+" + str(item_level - 1) + ")"
                    #
                    if create == True:
                        pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect((entity_message_offset_from_left + entity_message_width * 4// 5, entity_message_offset_from_top),
                                                (entity_message_width // 4, entity_message_height)),
                        text=addition,
                        manager=self.uiManager,
                        object_id='#title_addition')
            pretext = ""
            action = ""
            if item.equipable:
                if item.equipped:
                    pretext = "Unequip"
                    action = "u"
                    show = True
                    if item.cursed:
                        show = False
                else:
                    pretext = "Equip"
                    action = "e"
                    show = True
            elif item.consumeable and item.equipment_type == "Potiorb":
                pretext = "Quaff"
                action = "q"
                show = True
            elif item.consumeable and item.equipment_type == "Scrorb" or item.equipment_type == "Book":
                pretext = "Read"
                action = "r"
                show = True
            elif item.consumeable and item.has_trait("consumeable"):
                pretext = "Activate"
                action = "a"
                show = True
            if create == True:
                if show:
                    button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((entity_button_offset_from_left, entity_button_offset_from_top),
                                                  (entity_button_width, entity_button_height)),
                        text=pretext,
                        manager=self.uiManager)
                    button.action = action

                buttons_drawn += 1

                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((entity_button_offset_from_left + (entity_button_width + entity_button_offset_from_each_other) * buttons_drawn, entity_button_offset_from_top),
                                              (entity_button_width, entity_button_height)),
                    text='Drop',
                    manager=self.uiManager)
                button.action = "d"

                buttons_drawn += 1


        entity_text = ""
        if entity.has_trait("item"):
            item = entity
            if entity.has_trait("equipment"):
                if item.equipped:
                    entity_text += "Currently equipped<br>"
                if item.cursed:
                    entity_text += "<shadow size=1 offset=0,0 color=#901010><font color=#E0F0FF>" + "Once equipped, it cannot be taken off" +  "</font></shadow><br>"
                entity_text += "Equipment type: " + item.equipment_type + "<br>"
                if item.required_strength >= 0:
                    if player.character.get_strength() < item.required_strength:
                        req_str_text = "<shadow size=1 offset=0,0 color=#901010><font color=#E0F0FF>Required Strength: " + str(item.required_strength) + "(Unequippable) </font></shadow><br>"
                    else:
                        req_str_text = "Required Strength: " + str(item.required_strength) + "<br>"
                    entity_text += req_str_text
                if item.has_trait("weapon"):
                    entity_text += "Damage: " + str(item.damage_min + player.fighter.get_base_damage()) + " - " + str(item.damage_max + player.fighter.get_base_damage()) + "<br>"
                    if item.on_hit:
                        entity_text += "On hit: " + item.on_hit_description + "<br>"

                stats = item.stats.GetStatsForLevel(item.level)
                if stats[2]> 0:
                    entity_text += "Intelligence: +" + str(stats[2]) + "<br>"
                elif stats[2]<0:
                    entity_text += "Intelligence: " + str(stats[2]) + "<br>"
                if stats[0] > 0:
                    entity_text += "Strength: +" + str(stats[0]) + "<br>"
                elif stats[0]<0:
                    entity_text += "Strength: " + str(stats[0]) + "<br>"
                if stats[1] > 0:
                    entity_text += "Dexterity: +" + str(stats[1]) + "<br>"
                elif stats[1]<0:
                    entity_text += "Dexterity: " + str(stats[1]) + "<br>"
                if stats[3] > 0:
                    entity_text += "Endurance: +" + str(stats[3]) + "<br>"
                elif stats[3]<0:
                    entity_text += "Endurance: " + str(stats[3]) + "<br>"
                if stats[4] > 0:
                    entity_text += "Armor: +" + str(stats[4]) + "<br>"
                elif stats[4]<0:
                    entity_text += "Armor: " + str(stats[4]) + "<br>"
            elif entity.has_trait("potion") or entity.has_trait("ring"):
                entity_text += "Effect: " + str(entity.action_description) + "<br>"
            if item.attached_skill_exists:
                entity_text += "Grants skill: " + item.get_attached_skill_description() + "<br>"

        elif entity.has_trait("monster"):
            entity_text += "Health: " + str(entity.character.get_health()) + " / " + str(entity.character.get_max_health()) + "<br>"
            entity_text += "Attack: " + str(entity.fighter.get_damage_min()) + " - " + str(entity.fighter.get_damage_max()) + "<br>"
            entity_text += "Armor: " + str(entity.fighter.get_armor()) + "<br>"
            for skill in entity.character.skills:
                entity_text += "Has skill: " + str(skill.name)+ "<br>"
            if entity.has_trait("orb"):
                entity_text += "It's very round.<br>"
                for i, skill in enumerate(entity.character.skills):
                    if i == 0:
                        entity_text += "Skills: "
                    entity_text += skill.description()
                    if i < len(entity.character.skills) - 1:
                        entity_text += ", "

        elif entity.has_trait("interactable"):
            pass

        entity_text += "<br>" + entity.description

        if create == True:
            text_box = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((entity_text_offset_from_left, entity_text_offset_from_top), (entity_text_width, entity_text_height)),
                html_text = entity_text,
                manager=self.uiManager)

        self.uiManager.draw_ui(self.win)

    def update_questpopup_screen(self, loop, message):
        pygame.draw.rect(self.win, (0, 0, 0),
                         pygame.Rect(0, 0, 300,
                                     100))
        font = pygame.font.SysFont("Ariel", 25)
        text = font.render(message, True, (255, 255, 255))
        self.win.blit(text, (25, 25))

    #First draws the tiles, then darkens the ones that are out of range
    def draw_single_tile(self, loop, tile):
        if tile.get_visible() or tile.get_seen():
            tag = loop.tileDict.tile_string(tile.get_render_tag())
            self.win.blit(tag, (self.textSize * (tile.get_x() - self.x_start), self.textSize * (tile.get_y() - self.y_start)))
        if tile.get_seen() and not tile.get_visible() or (loop.currentLoop == LoopType.targeting and
                                                                loop.targets.get_range() is not None and
                                                                tile.get_distance(
                                                                    loop.targets.get_origin_range_coordinates()[0],
                                                                    loop.targets.get_origin_range_coordinates()[
                                                                        1]) > loop.targets.get_range()):
            black_img = pygame.Surface((32, 32))
            black_img.fill([int(100)] * 3)
            self.win.blit(black_img, (
            self.textSize * (tile.get_x() - self.x_start), self.textSize * (tile.get_y() - self.y_start)),
                          special_flags=pygame.BLEND_RGB_MULT)

    def update_examine(self, target, loop):
        x, y = target
        tag = loop.tileDict.tile_string(901)
        self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))

    def update_ui(self):
        deltaTime = self.clock.tick() / 1000
        self.uiManager.update(deltaTime)

    def update_screen(self, loop):
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)

    def update_screen_without_fill(self, loop):
        self.uiManager.draw_ui(self.win)



