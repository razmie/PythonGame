import pygame
import Game
import numpy

class Camera:
    game: Game = None

    width = 0
    height = 0
    zoom = 1.0

    position = [0, 0]
    last_position = [0, 0]
    zoom_centre = [0, 0]

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
                    self.position[0] -= event.pos[0] - self.last_position[0]
                    self.position[1] += event.pos[1] - self.last_position[1]
                    
                    self.last_position = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                self.zoom += event.y * 1.0 * deltaTime
                self.zoom = numpy.clip(self.zoom, 0.1, 3)

                # zoom_amount = event.y * 1.0 * deltaTime
                # self.zoom += zoom_amount#numpy.exp(zoom_amount / 10)

                #print("self.zoom ", self.zoom)

                # mouse_pos = pygame.mouse.get_pos()
                # norm_mouse_pos = (mouse_pos[0] / self.width, mouse_pos[1] / self.height)

                # self.zoom_centre[0] = norm_mouse_pos[0] * self.width
                # self.zoom_centre[1] = norm_mouse_pos[1] * self.height

    def get_projection_matrix(self):
        scale = numpy.array([[self.zoom, 0, 0], [0, self.zoom, 0], [0, 0, 1]])
        translation = numpy.array([[1, 0, -self.position[0]/self.zoom], [0, 1, -self.position[1]/self.zoom], [0, 0, 1]])
        screen_translation = numpy.array([[1, 0, 0.5*self.width], [0, 1, 0.5*self.height], [0, 0, 1]])

        projection_matrix =  screen_translation @ scale @ translation

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