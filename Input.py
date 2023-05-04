import pygame
from Maths import Vector2

class Input:
    @staticmethod
    def get_mouse_position():
        mouse_pos = pygame.mouse.get_pos()
        return Vector2(mouse_pos[0], mouse_pos[1])