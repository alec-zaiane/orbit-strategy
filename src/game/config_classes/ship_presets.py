from . import ship_config

def large_ship():
    return ship_config(
        mass=1e7, # kilograms, converts to 10,000 metric tons
        rotation_acceleration=1e-6, # radians per second squared
        max_rotation_speed=1e-2, # radians per second
        width=20, # meters
        length=100, # meters
        forward_thrust=1e9,
        backward_thrust=1e6,
        right_strafe_thrust=1e5, #prioritize one strafe direction due to cost
        left_strafe_thrust=1e2,
        max_health = 1e5,
        heat_dissipation = 10,
        heat_capacity=1e5,
        module_capacity = 1e5
    )
    
def small_ship():
    return ship_config(
        mass = 5e4, # kilograms, converts to 50 metric tons
        rotation_acceleration=1e-1, # radians per second squared
        max_rotation_speed=2e-1, # radians per second, equivalent to 1 rotation every 5 seconds
        width = 10, # meters
        length=20, # meters
        forward_thrust = 1e7,
        backward_thrust = 1e6,
        right_strafe_thrust = 1e5,
        left_strafe_thrust = 1e5,
        max_health = 1e4,
        heat_dissipation = 1,
        heat_capacity=100,
        module_capacity = 70,
    )
    
def tiny_drone():
    return ship_config(
        mass = 5e2, # kilograms, converts to 500 kg
        rotation_acceleration=1, # radians per second squared
        max_rotation_speed=1, # radians per second, equivalent to 1 rotation every 3 seconds
        width=1, # meters
        length=2, # meters
        forward_thrust=1e4,
        backward_thrust=1e3,
        right_strafe_thrust=1e4,
        left_strafe_thrust=1e2,
        max_health = 60,
        heat_dissipation = 0.1,
        heat_capacity=15,
        module_capacity=25,
    )