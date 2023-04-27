import numpy as np
import pygame
import World
from Actors.ActorBase import ActorBase

class PointActor(ActorBase):
    def __init__(self, new_world: World, new_position = np.array([0, 0]), new_size = 10, new_color = (0, 0, 255)):
        super().__init__(new_world)
        self.position = new_position
        self.size = new_size
        self.color = new_color

    def update(self, deltaTime: float):
        pass

    def draw(self):

        screen_pos = self.world.camera.world_to_screen(self.position)
        screen_size = self.world.camera.world_to_screen_size(self.size)

        # Disabled draw circle due to bug. This draws a line if the x position is negative.
        #pygame.draw.circle(self.game.screen, self.color, screen_pos, screen_size)

        # Draw circle on seperate surface to fix bug with draw circle.
        circle_surface = pygame.Surface((screen_size*2, screen_size*2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, self.color, (screen_size, screen_size), screen_size)
        self.game.screen.blit(circle_surface, (screen_pos[0] - screen_size, screen_pos[1] - screen_size))