"""Class to display the game state on a pygame surface"""
from typing import Callable
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

    def _find_bounding_box(self, obj_filter:Callable[[physics_object],bool]) -> tuple[float,float,float,float]:
        """Find the bounding box of all objects in the game world that pass the filter

        Args:
            obj_filter (Callable[[physics_object],bool]): Function that takes a physics_object and returns whether it should be considered in the bounding box calculation

        Returns:
            tuple[float,float,float,float]: (minx, maxx, miny, maxy) of the bounding box, or (0,0,0,0) if there are no objects
        """
        objects_of_interest = list(filter(obj_filter, self.game.game_world.physics_objects))
        if len(objects_of_interest) == 0:
            return (0,0,0,0)
        minx = min(obj.position.x for obj in objects_of_interest)
        maxx = max(obj.position.x for obj in objects_of_interest)
        miny = min(obj.position.y for obj in objects_of_interest)
        maxy = max(obj.position.y for obj in objects_of_interest)
        return (minx, maxx, miny, maxy)

    def find_scale_offset(self,                 # pylint: disable=too-many-locals
                          view_whole_world:bool =False,
                          padding_percent:float = 20,
                          smoothness:float = 0.9):
        """Find an optimal camera scale and offset for the current game state,
        updates self._camera to match

        Args:
            view_whole_world (bool, optional): whether to view the whole game world. Defaults to False.
            padding_percent (float, optional): add this percent of the screen as blank space on either side of the active area. Defaults to 20%.
            smoothness (float, optional): how much to smooth the camera movement, **must** be <1 Defaults to 0.9.
        """
        # find the bounding box of all objects, then find the scale and offset to fit that box on the screen
        padding_percent /= 100 # convert to decimal
        def filter_objects(obj:physics_object) -> bool:
            """return true if and only if this object should be considered in the camera calculation"""
            if isinstance(obj, ship):
                return True
            return False
        if view_whole_world:
            bounding_box = (
                (-self.game.game_world.world_size / 2)*((1+padding_percent)/2),
                (self.game.game_world.world_size / 2)*((1+padding_percent)/2),
                (-self.game.game_world.world_size / 2)*((1+padding_percent)/2),
                (self.game.game_world.world_size / 2)*((1+padding_percent)/2)
            )
        else:
            bounding_box = self._find_bounding_box(filter_objects)
            bounding_box = (
                bounding_box[0] * (1+padding_percent),
                bounding_box[1] * (1+padding_percent),
                bounding_box[2] * (1+padding_percent),
                bounding_box[3] * (1+padding_percent)
            )
            # ^ add padding, could probably be done more efficiently

        # now, find the scale and offset
        minx, maxx, miny, maxy = bounding_box
        bb_width = maxx - minx
        bb_height = maxy - miny

        # find the scale and offset
        # the correct scale will make the largest dimension of the bounding box fit the screen along that dimension
        screen_width, screen_height = self.screen.get_size()
        if bb_height / screen_height > bb_width / screen_width:
            # height is the limiting dimension
            scale = screen_height / bb_height
        else:
            # width is the limiting dimension
            scale = screen_width / bb_width

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
