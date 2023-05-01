import pygame
import Game
import Level
import World

class ScriptBase:
    def __init__(self, world: World):
        self.world = world
        self.level = world.level
        self.game = world.game
        pass

    def handle_events(self):
        pass

    def update(self, deltaTime: float):
        pass

    def draw(self, surface: pygame.Surface):
        pass