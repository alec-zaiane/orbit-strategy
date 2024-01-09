"""A player in the game, most likely a computer playing"""
from game.game_objects.ship import ship
class player: # pylint: disable=too-few-public-methods
    """A player in the game, most likely a computer playing"""
    def __init__(self, player_id:int, budget:int):
        self.id = player_id
        self.budget:float = budget
        self.ships:list[ship] = []

    def add_ship(self, ship_to_add:ship):
        """adds a ship to the player's fleet,
        also subtracts the cost of the ship from the player's budget

        Args:
            ship_to_add (ship): ship to add
        """
        self.ships.append(ship_to_add)
        self.budget -= ship_to_add.config.get_ship_cost()
