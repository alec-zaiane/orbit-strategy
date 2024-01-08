from .config_classes.game_configuration import game_config
from .game_world import game_world
from math_lib.vector2 import vector2
from . import game_objects
import random, math

class game:
    """A class to hold the game state and process the game loop
    """    
    def __init__(self, game_config: game_config):
        self.game_config = game_config
        # setup the game world
        self.game_world = game_world(
            world_size=game_config.world_radius,
            asteroid_amount=game_config.asteroid_amount,
            asteroid_size_mean=game_config.asteroid_size_mean,
            asteroid_size_stddev=game_config.asteroid_size_stddev,
        )
        # setup the players
        assert len(game_config.player_configs) == game_config.num_players
        self.players:list[game_objects.player] = []
        for i, player_config in enumerate(game_config.player_configs):
            newplayer = game_objects.player(
                     player_id = i,
                     budget=player_config.budget,
                 )
            around_location = vector2(
                math.cos(player_config.initial_direction),
                math.sin(player_config.initial_direction)
            ) * game_config.world_radius * 0.9
            
            random_offset_range = game_config.world_radius * 0.1
            
            start_velocity = vector2(
                math.cos(player_config.initial_direction + math.pi / 2),
                math.sin(player_config.initial_direction + math.pi / 2)
            ) * player_config.initial_velocity
            for ship_config in player_config.fleet:
                # add a random offset to the spawn location
                random_offset = vector2(
                    random.uniform(-random_offset_range, random_offset_range),
                    random.uniform(-random_offset_range, random_offset_range)
                )
                newplayer.add_ship(
                    game_objects.ship(
                        config=ship_config,
                        initial_position=around_location + random_offset,
                        initial_velocity=start_velocity,
                        owned_by=newplayer.id
                    )
                )
            self.players.append(newplayer)
        
        # add the players to the game world
        for player in self.players:
            for ship in player.ships:
                self.game_world.physics_objects.append(ship)
