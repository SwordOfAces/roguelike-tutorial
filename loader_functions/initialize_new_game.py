import tcod as libtcod


def get_constants():
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall':libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # Why the constants (except colors) weren't defined inside the dict is
    # an odd part of the tutorial. Just to allow the copy paste?
    constants = {
            'window_title': window_title,
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
            'fov_radius': 10 # how far can we see?,

            'max_monsters_per_room': 3,
            'max_items_per_room': 6,
            'colors': colors
        }

    return constants
