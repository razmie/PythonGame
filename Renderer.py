import numpy as np
import pygame
import World

class RenderUtil:
    @staticmethod
    def draw_point(world: World, position, size: int, color: pygame.color):
        screen_pos = world.camera.world_to_screen(position)
        screen_size = world.camera.world_to_screen_size(size)

        # Draw circle on seperate surface to fix bug with draw circle.
        circle_surface = pygame.Surface((screen_size*2, screen_size*2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, color, (screen_size, screen_size), screen_size)

        world.game.screen.blit(circle_surface, (screen_pos[0] - screen_size, screen_pos[1] - screen_size))

    def draw_line(world: World, start_position, end_position, width: int, color: pygame.color):
        screen_start = world.camera.world_to_screen(start_position)
        screen_end = world.camera.world_to_screen(end_position)
        screen_width = int(world.camera.world_to_screen_size(width))
        screen_width = max(screen_width, 1)

        pygame.draw.line(world.game.screen, color, screen_start, screen_end, screen_width)