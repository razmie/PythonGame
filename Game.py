import pygame
import time
from World import World

class Game:
    # How many frames per second should we update the game.
    FPS = 60

    # Set up variables needed to calculate delta time.
    lastFrameTime = 0
    lastFrameTime = time.time()

    screen: pygame.Surface = None

    world: World = None

    cached_events: list = None

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode([800, 600])

        self.world = World(self)

        clock = pygame.time.Clock()
        running = True

        while running:
            # Calculate delta time.
            self.currentTime = time.time()
            deltaTime = self.currentTime - self.lastFrameTime
            self.lastFrameTime = self.currentTime

            clock.tick(self.FPS)

            self.cached_events = pygame.event.get()

            for event in self.cached_events:
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))

            self.world.update(deltaTime)

            pygame.display.flip()

        pygame.quit()
