'''Configuration classes for the game.'''
from .game_configuration import game_config, player_config
from .ship_configuration import ship_config
from . import ship_presets

__all__ = [
    "game_config",
    "player_config",
    "ship_config",
    "ship_presets",
]
