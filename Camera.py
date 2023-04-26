import pygame
import Game
import numpy

class Camera:
    game: Game = None

    width = 0
    height = 0
    zoom = 1.0

    zoom_limit = [0.1, 3]
    zoom_vel = [1, 50]

    position = [0, 0]
    last_position = [0, 0]

    panning = False

    def __init__(self, inGame: Game):
        self.game = inGame

        self.width, self.height = self.game.screen.get_size()

    def update(self, deltaTime: float):
        for event in self.game.cached_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.panning = True
                    self.last_position = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.panning = False
            elif event.type == pygame.MOUSEMOTION:
                if self.panning:
                    self.position[0] -= (event.pos[0] - self.last_position[0])/self.zoom
                    self.position[1] += (event.pos[1] - self.last_position[1])/self.zoom
                    
                    self.last_position = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                zoom_range = self.zoom_limit[1] - self.zoom_limit[0]
                zoom_norm = (self.zoom - self.zoom_limit[0]) / zoom_range

                zoom_vel_range = self.zoom_vel[1] - self.zoom_vel[0]
                zoom_velocity = (zoom_vel_range * zoom_norm) + self.zoom_vel[0]

                self.zoom += event.y * zoom_velocity * deltaTime
                self.zoom = numpy.clip(self.zoom, self.zoom_limit[0], self.zoom_limit[1])

    def get_projection_matrix(self):
        scale = numpy.array([[self.zoom, 0, 0], [0, self.zoom, 0], [0, 0, 1]])
        translation = numpy.array([[1, 0, -self.position[0]], [0, 1, -self.position[1]], [0, 0, 1]])

        mid_screen_translation = numpy.array([[1, 0, 0.5*self.width], [0, 1, 0.5*self.height], [0, 0, 1]])

        projection_matrix = mid_screen_translation @ scale @ translation

        return projection_matrix
    
    def world_to_screen(self, point):
        projection_matrix = self.get_projection_matrix()
        point = numpy.append(point, [1])
        point = projection_matrix @ point
        point = point[:2] / point[2]
        point[1] = self.height - point[1]
        return point.astype(int)

    def screen_to_world(self, point):
        projection_matrix = self.get_projection_matrix()
        inverse_projection_matrix = numpy.linalg.inv(projection_matrix)
        point = numpy.append(point, [1])
        point = inverse_projection_matrix @ point
        point = point[:2] / point[2]
        return point
    
    def world_to_screen_size(self, size):
        return size * self.zoom