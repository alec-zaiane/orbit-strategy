from game.config_classes import ship_config
from math_lib.vector2 import vector2
from physics.physics_object import physics_object, rect_collider
class ship(physics_object):
    def __init__(self, 
                 config:ship_config, 
                 initial_position:vector2, 
                 initial_velocity:vector2
                 ):
        super().__init__(
            position=initial_position,
            velocity=initial_velocity,
            mass=config.mass,
            collider=rect_collider(
                width=config.width,
                height=config.length
            )
        )
        self.config = config
        self.position = initial_position
        self.velocity = initial_velocity