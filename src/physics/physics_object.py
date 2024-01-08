from __future__ import annotations
from math_lib.vector2 import vector2

class collider:
    """Simple collider, for now
    """
    def __init__(self, radius:float):
        self.radius = radius
        
    def check_collision(self, 
                        other:collider,
                        self_transform:tuple[vector2, float],
                        other_transform:tuple[vector2, float]) -> bool:
        """Check if this collider is colliding with another collider

        Args:
            other (collider): the other collider to check against
            self_transform (tuple[vector2, float]): the position and rotation of this collider
            other_transform (tuple[vector2, float]): the position and rotation of the other collider

        Returns:
            bool: whether their colliders are overlapping
        """
        if not type(self) == collider:
            raise TypeError("self must be a collider, "+
                            "likely that a child class did not override check_collision")
        if not (self_transform[0] - other_transform[0]).length < (self.radius + other.radius):
            # shortcut, if the distance between the two colliders is greater 
            #   than the sum of their radii, they can't be colliding
            return False
        if isinstance(other, rect_collider):
            # if the other one is a rectangular collider, 
            # we need to check if we're colliding with any of its edges, including rotation :(
            # first, unrotate the circle with respect to the rotated rectangle
            if other_transform[1] != 0:
                # other is rotated, so we need to unrotate the circle with respect to the rectangle
                # also, center all coordinates around the
                #   rectangle's center to make the math easier
                unrotated_circle_pos = self_transform[0] - other_transform[0]
                unrotated_circle_pos.rotate_rad(-other_transform[1])
                # now, check if the unrotated circle is colliding with the unrotated rectangle
                return self.check_collision(rect_collider(other.width, other.height), 
                                            (unrotated_circle_pos, 0), 
                                            (vector2(0, 0), 0))      
            else:
                # other is not rotated :)
                # check AABB first
                if abs(self_transform[0].x - other_transform[0].x) > (self.radius + other.width / 2):
                    return False
                if abs(self_transform[0].y - other_transform[0].y) > (self.radius + other.height / 2):
                    return False
                # now, find the closest point on the circle to the rectangle's center
                angle_from_circle_to_rect = (self_transform[0] - other_transform[0]).angle_rad
                closest_point_on_circle = self_transform[0].copy()
                unit = vector2(1, 0)
                unit.rotate_rad(angle_from_circle_to_rect)
                unit *= self.radius
                closest_point_on_circle += unit
                # now, check if that point is inside the rectangle
                if abs(closest_point_on_circle.x - other_transform[0].x) > other.width / 2:
                    return False
                if abs(closest_point_on_circle.y - other_transform[0].y) > other.height / 2:
                    return False    
                # if we got here, we're colliding
                return True
        else:
            return True
        
        
class rect_collider(collider):
    def __init__(self, width:float, height:float):
        # find a nice bounding circle
        rad = vector2(width, height).length
        
        super().__init__(radius=rad)
        self.width = width
        self.height = height
        
    def find_aabb(self, transform:tuple[vector2, float]) -> tuple[rect_collider, vector2]:
        """find the axis-aligned bounding box of this collider, with respect to a transform

        Args:
            transform (tuple[vector2, float]): the position and rotation in radians

        Returns:
            tuple[rect_collider, vector2]: a new collider and its position
        """
        # position doesn't really matter,
        #   we just need to find a new width and height based on the rotation
        four_corers = [
            vector2(self.width / 2, self.height / 2),
            vector2(self.width / 2, -self.height / 2),
            vector2(-self.width / 2, self.height / 2),
            vector2(-self.width / 2, -self.height / 2),
        ]
        for i in range(len(four_corers)):
            four_corers[i].rotate_rad(transform[1])
        
        # find the min and max x and y values
        min_x = min([corner.x for corner in four_corers])
        max_x = max([corner.x for corner in four_corers])
        min_y = min([corner.y for corner in four_corers])
        max_y = max([corner.y for corner in four_corers])
        
        new_collider = rect_collider(max_x - min_x, max_y - min_y)
        return (new_collider, transform[0])
        
        
    
    def check_collision(self,
                        other:collider, 
                        self_transform:tuple[vector2, float], 
                        other_transform:tuple[vector2, float]) -> bool:
        """Check if this collider is colliding with another collider

        Args:
            other (collider): the other collider to check against
            self_transform (tuple[vector2, float]): the position and rotation of this collider
            other_transform (tuple[vector2, float]): the position and rotation of the other collider

        Returns:
            bool: whether their colliders are overlapping
        """       
        if type(other) == collider:
            return other.check_collision(self, other_transform, self_transform) # flip it around, the code already exists for circle <-> rect collision
        elif isinstance(other, rect_collider):
            # check if the two AABBs are overlapping
            self_aabb, self_pos = self.find_aabb(self_transform)
            other_aabb, other_pos = other.find_aabb(other_transform)
            if abs(self_pos.x - other_pos.x) > (self_aabb.width + other_aabb.width) / 2:
                return False
            if abs(self_pos.y - other_pos.y) > (self_aabb.height + other_aabb.height) / 2:
                return False
            # if we got here, the AABBs are overlapping, we need to check if the actual colliders are overlapping
            # TODO: actually do it, for now just return True, I wonder what sort of strategy this might influence
            return True
        raise TypeError("other must be a collider, likely that a child class did not override check_collision")
             

class physics_object:
    """An object that has physical properties and can be simulated
    """    
    def __init__(self, mass:float, position: vector2, velocity: vector2, collider: collider):
        """Create a new physics object

        Args:
            mass (float): mass in kg
            position (vector2): position in meters from the origin
            velocity (vector2): velocity in meters per second
            collision_mode (collision_mode): collision mode for this object
        """        
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.rotation = 0 # radians
        self.collider = collider
        
    def check_collision(self, other:physics_object) -> bool:
        """Check if this object is colliding with another object

        Args:
            other (physics_object): the other object to check against

        Returns:
            bool: whether their colliders are overlapping
        """
        return self.collider.check_collision(other.collider, (self.position, self.rotation), (other.position, other.rotation))

    def update(self, time_delta:float = 1.0):
        """Update the object's physics state

        Args:
            time_delta (float, optional): timescale out of 1. Defaults to 1.0.
        """                    
        self.position.scaled_add(self.velocity, time_delta)
        
    def apply_force(self, force:vector2):
        """Apply a force to the object in newtons

        Args:
            force (vector2): force to apply
        """        
        acceleration = force / self.mass
        self.velocity += acceleration
        
    def __repr__(self) -> str:
        return f"physics_object @ x:{self.position.x} y:{self.position.y} with mass {self.mass} and velocity {self.velocity}"