"""Class to display the game state on a pygame surface"""
import pygame
import pygame.gfxdraw
from game.gamerunner import game
from math_lib.vector2 import vector2
from physics.physics_object import physics_object, rect_collider
# stuff for drawing
from game.game_objects.ship import ship


class game_viewer:
    """Class to display the game state on a pygame surface"""
    def __init__(self, game_to_view:game, screen_size:tuple[int,int]):
        """Class to display the game state on a pygame surface

        Args:
            game_to_view (game): the game to display
            screen_size (tuple[int,int]): the size of the screen to display on (width, height)
        """
        self.game = game_to_view
        self.screen = pygame.Surface(screen_size)

        #camera parameters
        self._camera:tuple[float,tuple[float,float]] = (1.0, (0.0, 0.0))
        # ^ (scale, (x_offset, y_offset))
        # "Camera" is sort of inverted, as in object are offset and scaled by the `camera`

        # find random-ish colours for the players
        # white is reserved for non-player things
        self.playercols:list[tuple[int,int,int]] = [
            (255,255,128),
            (255,128,255),
            (128,255,255),
            (128,128,255),
            (128,255,128),
            (255,128,128)
        ]
        assert len(self.game.players) < len(self.playercols), \
            "Not enough playercolours, maybe make it generated now instead of hardcoded"

    def find_scale_offset(self,                 # pylint: disable=too-many-locals
                          view_whole_world:bool =False,
                          padding_percent:float = 0.2,
                          smoothness:float = 0.9):
        """Find an optimal camera scale and offset for the current game state,
        updates self._camera to match

        Args:
            view_whole_world (bool, optional): whether to view the whole game world. Defaults to False.
            padding_percent (float, optional): add this percent of the screen as blank space on either side of the active area. Defaults to 0.2.
            smoothness (float, optional): how much to smooth the camera movement, **must** be <1 Defaults to 0.9.
        """
        # find the bounding box of all objects, then find the scale and offset to fit that box on the screen
        def filter_objects(obj:physics_object) -> bool:
            """return true if and only if this object should be considered in the camera calculation

            Args:
                obj (physics_object): object to be checked for consideration

            Returns:
                bool: whether it should influence the camera
            """
            if isinstance(obj, ship):
                return True
            return False

        desired_objects = [obj for obj in self.game.game_world.physics_objects \
                            if filter_objects(obj)]
        if view_whole_world or len(desired_objects) == 0:
            # if there's nothing, just show the whole world
            minx = -self.game.game_world.world_size / 2
            maxx = self.game.game_world.world_size / 2
            miny = -self.game.game_world.world_size / 2
            maxy = self.game.game_world.world_size / 2

        minx = desired_objects[0].position.x
        maxx = desired_objects[0].position.x
        miny = desired_objects[0].position.y
        maxy = desired_objects[0].position.y

        for obj in desired_objects[1:]:
            minx = min(minx, obj.position.x)
            maxx = max(maxx, obj.position.x)
            miny = min(miny, obj.position.y)
            maxy = max(maxy, obj.position.y)

        # now, add the padding
        height = maxy - miny
        width = maxx - minx
        minx -= width * padding_percent/2
        maxx += width * padding_percent/2
        miny -= height * padding_percent/2
        maxy += height * padding_percent/2

        # find the scale and offset
        # the correct scale will make the largest dimension of the bounding box fit the screen along that dimension
        screen_width, screen_height = self.screen.get_size()
        if height / screen_height > width / screen_width:
            # height is the limiting dimension
            scale = screen_height / height
        else:
            # width is the limiting dimension
            scale = screen_width / width

        # the correct offset will center the bounding box on the screen
        offset = (-(maxx + minx) / 2, -(maxy + miny) / 2)

        # now interpolate with smoothness
        final_scale = self._camera[0] * smoothness + scale * (1-smoothness)
        final_offset = (vector2(*self._camera[1]) * smoothness) + (vector2(*offset) * (1-smoothness))
        self._camera = (final_scale, final_offset.to_tuple())

    def render_to_self(self):
        """renders the game data to self.screen
        """
        self.screen.fill((0,0,0)) # reset the screen
        for obj in self.game.game_world.physics_objects:
            draw_coords = (((obj.position - vector2(*self._camera[1])) *self._camera[0]) \
                + vector2(*self.screen.get_size()) / 2).to_tuple()

            col_to_draw = (255,255,255)
            if isinstance(obj, ship):
                col_to_draw = self.playercols[obj.owned_by]

            render_size = obj.collider.radius * self._camera[0]
            # if it's too far out of bounds, skip the draw
            if draw_coords[0] + render_size < 0 or draw_coords[0] - render_size > self.screen.get_width():
                continue
            if draw_coords[1] + render_size < 0 or draw_coords[1] - render_size > self.screen.get_height():
                continue

            if render_size < 8:
                # the object will be too small to make out at this scale, draw it as a hollow circle instead
                pygame.gfxdraw.aacircle( # pylint: disable=c-extension-no-member
                    self.screen,
                    int(draw_coords[0]),
                    int(draw_coords[1]),
                    5,
                    col_to_draw
                )
            else:
                if isinstance(obj.collider, rect_collider) and False: # pylint: disable=condition-evals-to-constant
                    # have to take rotation and all of that into account
                    # which means blitting with an alpha'd surface?
                    ...
                    # for now just skip
                else:
                    # circle collider, much easier
                    pygame.draw.circle(
                        surface=self.screen,
                        color=col_to_draw,
                        center=draw_coords,
                        radius=obj.collider.radius * self._camera[0],
                        )
