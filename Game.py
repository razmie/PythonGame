import pygame
import time
from Level import Level

class Game:
    # How many frames per second should we update the game.
    FPS = 60

    # Set up variables needed to calculate delta time.
    lastFrameTime = 0
    lastFrameTime = time.time()

    screen: pygame.Surface = None

    has_level_to_load: bool = False
    level: Level = None

    cached_events: list = None

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([800, 600])

        self.load_level("Assets/Levels/Frontend/Frontend.json")
        #self.load_level("Assets/Levels/world.json")

        while self.has_level_to_load:
            self.check_level_load()
            self.update_level()

        pygame.quit()

    def update_level(self):
        self.level_running = True
        while self.level_running and self.level:
            # Calculate delta time.
            self.currentTime = time.time()
            deltaTime = self.currentTime - self.lastFrameTime
            self.lastFrameTime = self.currentTime

            self.clock.tick(self.FPS)

            self.cached_events = pygame.event.get()

            for event in self.cached_events:
                if event.type == pygame.QUIT:
                    self.level_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.level_running = False

            self.screen.fill((255, 255, 255))

            self.level.update(deltaTime)

            pygame.display.flip()

    def load_level(self, level_path: str):
        self.level_path = level_path
        self.has_level_to_load = True
        self.level_running = False

    def check_level_load(self):
        if self.has_level_to_load == True:
            if self.level != None:
                del self.level

            self.level = Level(self, self.level_path)
            self.has_level_to_load = False