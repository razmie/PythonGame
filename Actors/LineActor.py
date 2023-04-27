import numpy as np
import pygame
import World
from Actors.ActorBase import ActorBase

class LineActor(ActorBase):
    def __init__(self, new_world: World, new_start = np.array([0, 0]), new_end = np.array([100, 100]), new_width = 5, new_color = (0, 0, 255)):
        super().__init__(new_world)
        self.position = new_start
        self.end_position = new_end
        self.width = new_width
        self.color = new_color

    def update(self, deltaTime: float):
        pass

    def draw(self):
        screen_start = self.world.camera.world_to_screen(self.position)
        screen_end = self.world.camera.world_to_screen(self.end_position)
        screen_width = int(self.world.camera.world_to_screen_size(self.width))

        pygame.draw.line(self.game.screen, self.color, screen_start, screen_end, screen_width)