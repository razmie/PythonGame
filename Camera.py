import pygame
import Game, World
from Input import Input
from Maths import Maths, Vector2, Matrix3x3

class Camera:
    game: Game = None
    world: World = None

    def __init__(self, new_world: World):
        self.world = new_world
        self.game = self.world.game

        self.width, self.height = self.game.screen.get_size()

        self.zoom = 1.0

        self.zoom_limit_range = [0.5, 3]
        self.zoom_vel_range = [1, 100]

        self.position = Vector2(0, 0)
        self.last_position = Vector2(0, 0)

        self.panning = False

        self.interpolating = False
        self.interp_time = 0.1
        self.interp_accum_time = 0.0
        self.interp_position = Vector2(0, 0)
        self.interp_zoom = 1.0

    def update(self, deltaTime: float):
        mouse_pos = Input.get_mouse_position()
        world_mouse_pos = self.screen_to_world(mouse_pos)

        for event in self.game.cached_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.panning = True
                    self.last_position = Vector2(event.pos[0], event.pos[1])

                    # Cancel interpolation.
                    self.interpolating = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.panning = False

                    #mouse_pos = pygame.mouse.get_pos()
                    #mouse_pos = self.screen_to_world(mouse_pos)
                    #self.interpolate(mouse_pos, self.zoom+0.1)

            elif event.type == pygame.MOUSEMOTION:
                if self.panning:
                    self.position.x -= (event.pos[0] - self.last_position.x)/self.zoom
                    self.position.y -= (event.pos[1] - self.last_position.y )/self.zoom
                    
                    self.last_position = Vector2(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEWHEEL:
                zoom_range = self.zoom_limit_range[1] - self.zoom_limit_range[0]
                zoom_norm = (self.zoom - self.zoom_limit_range[0]) / zoom_range

                zoom_vel_range = self.zoom_vel_range[1] - self.zoom_vel_range[0]
                zoom_velocity = (zoom_vel_range * zoom_norm) + self.zoom_vel_range[0]

                new_zoom = self.zoom + (event.y * zoom_velocity * deltaTime)

                if new_zoom >= self.zoom_limit_range[0] and new_zoom <= self.zoom_limit_range[1]:
                    new_pos = self.position + ((world_mouse_pos - self.position) * deltaTime * 10 * event.y)

                    self.interpolate(new_pos, new_zoom)

        if self.interpolating:
            self.interp_accum_time += deltaTime
            if self.interp_accum_time >= self.interp_time:
                self.interp_accum_time = self.interp_time

                self.interpolating = False

            t = self.interp_accum_time / self.interp_time
            self.position = self.position + (self.interp_position - self.position) * t

            self.zoom = self.zoom + (self.interp_zoom - self.zoom) * t
            self.zoom = Maths.clip(self.zoom, self.zoom_limit_range[0], self.zoom_limit_range[1])

        #RenderUtil.draw_point(self.world, world_mouse_pos, 10, (0,255,0))

    def get_projection_matrix(self):
        scale = Matrix3x3([[self.zoom, 0, 0], [0, self.zoom, 0], [0, 0, 1]])
        translation = Matrix3x3([[1, 0, -self.position.x], [0, 1, -self.position.y], [0, 0, 1]])

        mid_screen_translation = Matrix3x3([[1, 0, 0.5*self.width], [0, 1, 0.5*self.height], [0, 0, 1]])

        projection_matrix = mid_screen_translation @ scale @ translation

        return projection_matrix
    
    def world_to_screen(self, point: Vector2):
        projection_matrix = self.get_projection_matrix()
        point = projection_matrix @ point
        return point

    def screen_to_world(self, point: Vector2):
        projection_matrix = self.get_projection_matrix()
        inverse_projection_matrix = projection_matrix.inverse()
        point = inverse_projection_matrix @ point
        return point
    
    def world_to_screen_size(self, size: Vector2):
        return size * self.zoom
    
    def interpolate(self, new_position: Vector2, new_zoom: float):
        self.interpolating = True
        self.interp_accum_time = 0.0
        self.interp_position = new_position
        self.interp_zoom = new_zoom