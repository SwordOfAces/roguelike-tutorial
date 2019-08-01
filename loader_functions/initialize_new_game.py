import tcod as libtcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder


def get_constants():
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall':libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    screen_width = 80
    screen_height = 50
    bar_width = 20
    panel_height = 7

    # Why the constants (except colors) weren't defined inside the dict is
    # an odd part of the tutorial. Just to allow the copy paste?
    # A: Because some of them are derived from others
    constants = {
            'window_title': "Roguelike Tutorial Revised",
            'screen_width': screen_width,
            'screen_height': screen_height,
            'bar_width': bar_width,
            'panel_height': panel_height,
            'panel_y': screen_height - panel_height,

            'message_x': bar_width + 2,
            'message_width': screen_width - bar_width - 2,
            'message_height': panel_height - 1,

            'map_width': 80,
            'map_height': 43,

            'room_max_size': 10,
            'room_min_size': 6,
            'max_rooms': 30,

            'fov_algorithm': 0, # to indicate the default algorithm,
            'fov_light_walls': True, # brighten the walls we can see,
            'fov_radius': 10, # how far can we see?,

            'max_monsters_per_room': 3,
            'max_items_per_room': 6,
            'colors': colors
        }

    return constants


def get_game_variables(constants):
    # Set up player:
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    level_component = Level()
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True,
            render_order=RenderOrder.ACTOR, fighter=fighter_component,
            inventory=inventory_component, level=level_component)
    entities = [player]

    # Set up game map:
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'])

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
