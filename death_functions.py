import tcod as libtcod

from game_states import GameStates

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red
    return 'You died!', GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = '{monster.name.capitalize()} is dead!'
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighhter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name

    return death_message
