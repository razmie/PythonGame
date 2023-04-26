import pygame
import numpy
import Game
from Camera import Camera

class World:
    game: Game = None
    camera: Camera = None

    points = [(10, 10), (150, 200), (200, 400)]

    def __init__(self, inGame: Game):
        self.game = inGame
        self.camera = Camera(inGame)

    def update(self, deltaTime: float):
        self.camera.update(deltaTime)

        for point in self.points:
            p = self.camera.world_to_screen(point)

            pygame.draw.circle(self.game.screen, (0, 0, 255), p, 10)

        #pygame.draw.rect(self.game.screen, (255,0,0), (0,0,100,100), 1)

