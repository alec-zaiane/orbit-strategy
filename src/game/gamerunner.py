"""`game` object actually handles running the game loop and holds the game state."""
import random
import math
from math_lib.vector2 import vector2
from .config_classes.game_configuration import game_config
from .game_world import game_world
from . import game_objects

class game: # pylint: disable=too-few-public-methods
    """A class to hold the game state and process the game loop
    """
    def __init__(self, game_configuration: game_config):
        self.game_config = game_configuration
        # setup the game world
        self.game_world = game_world(
            world_size=game_configuration.world_radius,
            asteroid_amount=game_configuration.asteroid_amount,
            asteroid_size_mean=game_configuration.asteroid_size_mean,
            asteroid_size_stddev=game_configuration.asteroid_size_stddev,
        )
        # setup the players
        assert len(game_configuration.player_configs) == game_configuration.num_players
        self.players:list[game_objects.player] = []
        for i, player_config in enumerate(game_configuration.player_configs):
            newplayer = game_objects.player(
                     player_id = i,
                     budget=player_config.budget,
                 )
            around_location = vector2(
                math.cos(player_config.initial_direction),
                math.sin(player_config.initial_direction)
            ) * game_configuration.world_radius * 0.9

            random_offset_range = game_configuration.world_radius * 0.1

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
                new_ship = game_objects.ship(
                        config=ship_config,
                        initial_position=around_location + random_offset,
                        initial_velocity=start_velocity,
                        owned_by=newplayer.id
                )
                new_ship.rotation = player_config.initial_direction + (math.pi / 2)
                newplayer.ships.append(new_ship)
            self.players.append(newplayer)

        # add the players to the game world
        for player in self.players:
            for ship in player.ships:
                self.game_world.physics_objects.append(ship)

    def update(self, time_delta:float):
        """Update the game state

        Args:
            time_delta (float): time since last update
        """
        self.game_world.update(time_delta)