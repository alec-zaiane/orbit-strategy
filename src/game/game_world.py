"""The game world holds all the physics objects and simulates them"""
import math
import random
from physics.physics_object import physics_object, collider
from math_lib.vector2 import vector2

class game_world: # pylint: disable=too-few-public-methods
    """Holds the game world and any physics objects to simulate
    """
    def __init__(self,
                 world_size: float,
                 asteroid_amount: int,
                 asteroid_size_mean: float,
                 asteroid_size_stddev: float,
                 ):
        self.physics_objects: list[physics_object] = []
        self.world_size = world_size
        self.asteroid_amount = asteroid_amount
        for _ in range(asteroid_amount):
            self._add_asteroid(
                size=random.gauss(asteroid_size_mean, asteroid_size_stddev),
                position=vector2(
                    random.uniform(-world_size, world_size),
                    random.uniform(-world_size, world_size)
                ),
                velocity=vector2(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                )
            )

    def _add_asteroid(self, size:float, position:vector2, velocity:vector2):
        """add an asteroid to the game world

        Args:
            size (float): radius of the asteroid
            position (vector2): position of the asteroid in the game world
            velocity (vector2): velocity of the asteroid in the game world
        """
        self.physics_objects.append(
            physics_object(
                position=position,
                velocity=velocity,
                mass=math.pi * math.pow(size, 2),
                phys_collider=collider(
                    radius=size
                )
            )
        )
    def update(self, time_delta:float):
        """Update the game world and all physics objects in it

        Args:
            time_delta (float): time since last update in seconds
        """
        for phys_obj in self.physics_objects:
            phys_obj.update(time_delta)
