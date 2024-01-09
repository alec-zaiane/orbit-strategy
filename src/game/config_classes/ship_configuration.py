"""Configuration classes for ships and ship modules"""
import math
from dataclasses import dataclass
@dataclass
class ship_config: # pylint: disable=too-many-instance-attributes
    """a ship configuration, holds all the data needed to create a ship
    """
    # physical properties
    mass:float = 1e5
    '''mass of the ship in kg'''
    rotation_acceleration:float = 1e-3
    '''how fast the ship can accelerate its rotation in radians per second squared'''
    max_rotation_speed:float = 1e-1
    '''maximum rotation speed in radians per second, 
    this is a cap due to g-forces or something similar'''
    width:float = 1e2
    '''width of the ship in meters'''
    length:float = 1e2
    '''length of the ship in meters'''

    # thruster properties
    forward_thrust:float = 1e6
    '''maximum forward thrust in newtons'''
    backward_thrust:float = 1e5
    '''maximum backward thrust in newtons'''
    right_strafe_thrust:float = 1e2
    '''maximum right strafe thrust in newtons'''
    left_strafe_thrust:float = 1e2
    '''maximum left strafe thrust in newtons'''

    # gameplay properties
    max_health:float = 100
    '''maximum health of the ship, in arbitrary units'''
    heat_dissipation:float = 1
    '''how fast the ship dissipates heat passively, in arbitrary units per second'''
    heat_capacity:float = 1e2
    '''how much heat the ship can store before it starts taking damage, in arbitrary units'''

    module_capacity:float = 100
    '''how many points worth of modules the ship can hold,
    each module has a cost proportional to its use/efficiency'''

    def get_ship_cost(self) -> float:
        """returns the 'cost' of the ship, in arbitrary units based on all of the properties, 
        module cost must be added separately

        Returns:
            float: the cost of the ship, in arbitrary units
        """
        cost = 0
        # physical properties
        # mass should be relatively cheap
        cost += self.mass / 1e3
        # rotation acceleration should be relatively expensive, scale exponentially
        cost += math.pow(self.rotation_acceleration, 1.5) * 1e3
        # max rotation speed should be relatively expensive, and scale exponentially
        cost += math.pow(self.max_rotation_speed, 1.5) * 1e3
        # it should also be weighed against the longest side of the ship,
        # sort of a "tensile strength cost",
        # the faster it spins and longer it is, the more expensive it is
        cost += math.pow(self.max_rotation_speed, 1.5) \
             * math.pow(max(self.width, self.length), 1.5) * 1e3
        # a larger ship should be more expensive
        cost += self.width * self.length / 1e3

        # thruster properties
        # forward thrust shouldn't be too expensive, but should scale exponentially
        cost += math.pow(self.forward_thrust, 1.2) / 10
        # backward thrust should be more expensive than forward thrust
        # (otherwise, driving the ship backwards is cheaper)
        cost += math.pow(self.backward_thrust, 1.4) / 5
        # strafe thrust should be even more expensive than backward thrust
        cost += math.pow(self.right_strafe_thrust, 1.6) / 2
        cost += math.pow(self.left_strafe_thrust, 1.6) / 2

        # gameplay properties
        # max health should be expensive, but diminished by the mass and size of the ship
        cost += self.max_health * 1e3 / (self.mass * math.pow(max(self.width, self.length), 1.5))
        # heat dissipation needs to be weighed against surface area
        heat_dissipation_per_square_meter = self.heat_dissipation / (self.width * self.length)
        cost += heat_dissipation_per_square_meter * 1e3
        # heat capacity needs to be weighed against max health and mass
        cost += self.heat_capacity * 1e3 / (self.max_health * self.mass)
        # module capacity should be weighed against mass and size
        cost += self.module_capacity / (self.mass * math.pow(max(self.width, self.length), 1.5))
        return cost

class module_config: # pylint: disable=too-few-public-methods
    """_summary_
    """
    def __init__(self):
        self.name = "module"
        self.points_cost = 1
        """how many arbitrary points this module costs"""
        self.capacity_usage = 1
        """How many points of ship module capacity this module uses"""
