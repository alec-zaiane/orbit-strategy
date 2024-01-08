from game.game_objects.ship import ship
class player:
    def __init__(self, player_id:int, budget:int):
        self.id = player_id
        self.budget:float = budget
        self.ships:list[ship] = []

    def add_ship(self, ship_to_add:ship):
        self.ships.append(ship_to_add)
        self.budget -= ship_to_add.config.get_ship_cost()