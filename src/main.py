import pygame
import game.config_classes as config_classes
from game.gamerunner import game
from graphics_display.game_viewer import game_viewer

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    game_cfg = config_classes.game_config(
        num_players=1,
        player_configs=[
            config_classes.player_config(
                initial_direction=0,
                initial_velocity=5,
                fleet=[
                    config_classes.ship_presets.large_ship(),
                    config_classes.ship_presets.small_ship(),
                    config_classes.ship_presets.tiny_drone(),
                ],
                budget=10000000000
            ),
            # config_classes.player_config(
            #     initial_direction=3.14,
            #     initial_velocity=5,
            #     fleet=[
            #         config_classes.ship_presets.large_ship(),
            #         config_classes.ship_presets.small_ship(),
            #         config_classes.ship_presets.tiny_drone(),
            #     ],
            #     budget=10000000000
            # )

        ],
        world_radius=1e5,
        asteroid_amount=100,
        asteroid_size_mean=100,
        asteroid_size_stddev=50,
    )
    game_instance = game(game_cfg)
    viewer = game_viewer(game_instance, screen.get_size())
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
        # update game
        #game_instance.update(time_delta=0.001)
        
        # draw game
        screen.fill((0, 0, 0))
        viewer.find_scale_offset(padding_percent=100)
        viewer.render_to_self()
        screen.blit(viewer.screen,(0,0))
        print(viewer._camera)
        
        pygame.display.flip()