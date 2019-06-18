class Tile:
    """
    A tile on a map. It can be blocked, or block sight.
    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # By default, a tile blocks sight if it is blocked
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
