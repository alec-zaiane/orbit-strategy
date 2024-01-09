"""Player and Game configuration classes"""
from dataclasses import dataclass
from game.config_classes.ship_configuration import ship_config

@dataclass
class player_config:
    """Configuration of a player
    """
    initial_direction: float # radians
    initial_velocity: float # m/s
    budget: int
    fleet: list[ship_config]

@dataclass
class game_config:
    """Stores configuration data for an instance of the game
    """
    # general configuration
    num_players: int

    # one player config per player
    player_configs: list[player_config]

    # world generation configuration
    world_radius: float
    asteroid_amount: int
    asteroid_size_mean: float
    asteroid_size_stddev: float
