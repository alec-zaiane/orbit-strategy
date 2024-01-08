from src.game.game_objects.ship import ship
class player:
    def __init__(self, player_id:int, budget:int):
        self.id = player_id
        self.budget = budget
        self.ships:list[ship] = []