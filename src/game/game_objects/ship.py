"""A ship in the game"""
from game.config_classes import ship_config
from math_lib.vector2 import vector2
from physics.physics_object import physics_object, rect_collider
class ship(physics_object):
    """A ship in the game"""    
    def __init__(self,
                 config:ship_config,
                 initial_position:vector2,
                 initial_velocity:vector2,
                 owned_by:int
                 ):
        """Ship class

        Args:
            config (ship_config): config for this ship
            initial_position (vector2): initial position
            initial_velocity (vector2): initial velocity
            owned_by (int): player ID of who owns this ship
        """
        super().__init__(
            position=initial_position,
            velocity=initial_velocity,
            mass=config.mass,
            phys_collider=rect_collider(
                width=config.width,
                height=config.length
            )
        )
        self.config = config
        self.position = initial_position
        self.velocity = initial_velocity
        self.owned_by = owned_by
