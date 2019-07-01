from random import randint

import tcod as libtcod

from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()


    def create_split_bsp(self, max_rooms, room_min_size, max_ratio):
        # depth is the number of recursive splits to do: higher number,
        #    more nodes -> more rooms
        # min_wd, min_ht: minimum width/height for a node
        # max_h_ratio, max_v_ratio: maximum horizontal/vertical ratio
        
        # the 0 here is to use the default random number generator
        libtcod.bsp_split_recursive(self.bsp, 0, max_rooms,
                room_min_size, room_min_size, max_ratio, max_ratio)

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.bsp = libtcod.bsp_new_with_size(0, 0, self.width, self.height)
        self.rooms = []
        #libtcod.bsp_split_once(self.bsp, False, 30)
        self.create_split_bsp(max_rooms, room_min_size, 1.5)
        
        # Traverse the tree from leafs up:
        libtcod.bsp_traverse_inverted_level_order(self.bsp, self.dig_node)

        player.x, player.y = self.rooms[0].center()

    
    def dig_node(self, node, dat):
        # dat is a dummy param in this case
        if libtcod.bsp_is_leaf(node):
            # If it's a bottom level split, let's make a room.

            node.w = randint(self.room_min_size, self.room_max_size)
            node.h = randint(self.room_min_size, self.room_max_size)
            node.x = randint(node.x, node.x + node.w)
            node.y = randint(node.y, node.y + node.h)
            
            # if we're making an out of bounds room, pare it down
            if node.x + node.w > self.width:
                node.w = self.width - node.x - 1
            if node.y + node.h > self.height:
                node.h = self.height - node.y - 1

            new_room = Rect(node.x, node.y, node.w, node.h)
            self.create_room(new_room)
            self.rooms.append(new_room)
        else:
            # This is a node that contains two nodes (either another tree,
            # or a leaf (ie room), and we want to connect the two with a
            # tunnel
            # These are the left and right of the tree, not position
            left = libtcod.bsp_left(node)
            right = libtcod.bsp_right(node)
            node.x = min(left.x, right.x)
            node.y = min(left.x, right.x)
            node.w = max(left.x + left.w, right.x + right.w) - node.x
            node.h = max(left.y + left.h, right.y + right.h) - node.y
          
            if len(self.rooms) > 1:
                left_center, right_center = None, None
                for room in self.rooms:
                    if libtcod.bsp_contains(left, *room.center()):
                        left_center = room.center()
                    if libtcod.bsp_contains(right, *room.center()):
                        right_center = room.center()
                if left_center and right_center:
                    self.connect_rooms(left_center, right_center)








    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def XXmake_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # Random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # Rect class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # Run through the other rooms to see if they intersect
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # No intersections, so the room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # Center coordinates of new room, will be useful later:
                new_x, new_y = new_room.center()

                if num_rooms == 0:
                    # This is the first room, where the player starts
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # Center coordinates of prev room
                    prev_x, prev_y = rooms[num_rooms - 1].center()

                    # flip a coin
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # Finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1


    def create_room(self, room):
        # Go through the tiles in the rectangle and make them passable
        # Keep the walls on the exterior edge of th room.
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def connect_rooms(self, c1, c2):
        c1x, c1y = c1
        c2x, c2y = c2
        if randint(0, 1):
            self.create_h_tunnel(c1x, c2x, c1y)
            self.create_v_tunnel(c1y, c2y, c2x)
        else:
            self.create_v_tunnel(c1y, c2y, c1x)
            self.create_h_tunnel(c1x, c2x, c2y)



    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            try:
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
            except IndexError:
                print("h_tunnel index error")

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            try:
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
            except IndexError:
                print("v_tunnel index error")

    def is_blocked(self, x, y):
        # Left as such because of a promise of further additions
        if self.tiles[x][y].blocked:
            return True
        return False
