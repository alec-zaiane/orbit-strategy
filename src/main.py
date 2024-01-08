import pygame
import game.config_classes as config_classes
from game.gamerunner import game

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    game_cfg = config_classes.game_config(
        num_players=2,
        player_configs=[
            config_classes.player_config(
                initial_direction=0,
                initial_velocity=5,
                fleet=[
                    config_classes.ship_presets.large_ship(),
                    config_classes.ship_presets.small_ship(),
                    config_classes.ship_presets.tiny_drone(),
                ],
                budget=10000
            ),
            config_classes.player_config(
                initial_direction=3.14,
                initial_velocity=5,
                fleet=[
                    config_classes.ship_presets.large_ship(),
                    config_classes.ship_presets.small_ship(),
                    config_classes.ship_presets.tiny_drone(),
                ],
                budget=10000
            )

        ],
        world_radius=1e5,
        asteroid_amount=100,
        asteroid_size_mean=100,
        asteroid_size_stddev=50,
    )
    game_instance = game(game_cfg)
    
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
        # update game
        #game_instance.update(time_delta=0.001)
        
        # draw game
        screen.fill((0, 0, 0))
        scale:float = 0.1
        offset = (400, 300)
        all_objects = game_instance.game_world.physics_objects
        to_draw:list[tuple[tuple[float,float],float]] = []
        for obj in all_objects:
            draw_position = (obj.position * scale + offset).to_tuple()
            to_draw.append((draw_position, obj.collider.radius * scale))
            
        for (x, y), r in to_draw:
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), int(r))
        
        pygame.display.flip()