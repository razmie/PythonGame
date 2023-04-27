import numpy as np
import pygame
import World

class Renderer:
    @staticmethod
    def draw_point(world: World, position, size, color: pygame.color):
        screen_pos = world.camera.world_to_screen(position)
        screen_size = world.camera.world_to_screen_size(size)

        # Draw circle on seperate surface to fix bug with draw circle.
        circle_surface = pygame.Surface((screen_size*2, screen_size*2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, color, (screen_size, screen_size), screen_size)

        world.game.screen.blit(circle_surface, (screen_pos[0] - screen_size, screen_pos[1] - screen_size))