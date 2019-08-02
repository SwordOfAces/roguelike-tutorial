import tcod as libtcod


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with over 26 options')

    # Calculate total height for the header (after auto-wrap)
    # and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # Print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # Print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ')' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # Show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append(f'{item.name} on main hand')
            elif player.equipment.off_hand == item:
                options.append(f'{item.name} on off hand') 
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, 'TOMB OF THE ANCIENT KINGS')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER, 'By RJ')

    menu(con, '', ['Play new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = [f'Constitution (+20 HP {player.fighter.max_hp})',
               f'Strength (+1 attack, from {player.fighter.power})',
               f'Agility (+1 defense, from {player.fighter.defense})']
    menu(con, header, options, menu_width, screen_width, screen_height)


def character_screen(player, char_screen_width, char_screen_height,
        screen_width, screen_height):
    window = libtcod.console_new(char_screen_width, char_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    texts = ['Character Information',
            f'Level: {player.level.current_level}',
            f'Experience: {player.level.current_xp}',
            f'Experience to level: {player.level.experience_to_next_level}',
            f'Maximum HP: {player.fighter.max_hp}',
            f'Attack: {player.fighter.power}',
            f'Defense: {player.fighter.defense}']
    for i, text in enumerate(texts):
        libtcod.console_print_rect_ex(window, 0, i+1,
                char_screen_width, char_screen_height, libtcod.BKGND_NONE,
                libtcod.LEFT, text)
        x = screen_width // 2 - char_screen_width // 2
        y = screen_height // 2 - char_screen_height // 2
        libtcod.console_blit(window, 0, 0, char_screen_width, char_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
