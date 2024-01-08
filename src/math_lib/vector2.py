from __future__ import annotations
import math

# make a type alias for vector2 or a tuple of floats

class vector2:
    """2d vector class
    """    
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
        
    @property
    def length(self) -> float:
        """Returns the length of the vector
        """        
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def angle_rad(self) -> float:
        """Returns the angle of the vector in radians
        """        
        return math.atan2(self.y, self.x)
        
    def normalize(self):
        """Normalizes the vector
        """        
        length = self.length
        self.x /= length
        self.y /= length
        
    def rotate_rad(self, angle:float):
        """Rotates the vector by a given angle in radians

        Args:
            angle (float): angle in radians (clockwise)
        """        
        x = self.x
        y = self.y
        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = x * math.sin(angle) + y * math.cos(angle)

    def copy(self) -> vector2:
        """Returns a copy of this vector

        Returns:
            vector2: copy of this vector
        """        
        return vector2(self.x, self.y)
        
    def __add__(self, other:vector2|tuple[float,float]):
        if isinstance(other, tuple):
            other = vector2(other[0],other[1])
        return vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other:vector2|tuple[float,float]):
        if isinstance(other, tuple):
            other = vector2(other[0],other[1])
        return vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other:float):
        return vector2(self.x * other, self.y * other)
    
    def __truediv__(self, other:float):
        return vector2(self.x / other, self.y / other)
    
    def scaled_add(self, other:vector2, influence:float):
        """Scales the other vector by the influence and adds it to this vector

        Args:
            other (vector2): vector to add
            influence (float): how much to scale the other vector before adding
        """
        scaledVec = other * influence
        self.x += scaledVec.x
        self.y += scaledVec.y
        
    def to_tuple(self) -> tuple[float, float]:
        """return a tuple representation of this vector

        Returns:
            tuple[float, float]: tuple containing the x and y values of this vector
        """        
        return (self.x, self.y)
        
    @staticmethod
    def from_angle(angle:float, length:float = 1.0) -> vector2:
        """Returns a vector from an angle

        Args:
            angle (float): angle in radians
            length (float, optional): length of the vector. Defaults to 1.0.

        Returns:
            vector2: vector from the angle
        """        
        return vector2(math.cos(angle) * length, math.sin(angle) * length)
    
    def __repr__(self) -> str:
        return f"vector2({self.x}, {self.y})"