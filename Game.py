import pygame
import time
import sys
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

        self.screen_color = (255, 255, 255)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([800, 600])
        self.update_count = 0
        self.delta_time = 0

        level_name = Game.find_in_argument_variable("level")

        self.load_level(level_name)

        while self.has_level_to_load:
            self.check_level_load()
            self.update_level()

        pygame.quit()

    def update_level(self):
        self.level_running = True
        while self.level_running and self.level:
            # Calculate delta time.
            self.currentTime = time.time()
            self.delta_time = self.currentTime - self.lastFrameTime
            self.lastFrameTime = self.currentTime

            if self.is_debugging() == False:
                print("FALSE")

            self.clock.tick(self.FPS)

            self.cached_events = pygame.event.get()

            for event in self.cached_events:
                if event.type == pygame.QUIT:
                    self.level_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.level_running = False

            self.screen.fill(self.screen_color)

            self.level.update(self.delta_time)

            self.update_count += 1

            pygame.display.flip()

            # Check if the time passed since the last frame is too long.
            currentTime = time.time()
            diff_time = currentTime - self.lastFrameTime
            if diff_time > 1:
                # The time difference is big. Fake the last delta time so that the next frame is not too big.
                self.delta_time = 1 / self.FPS
                self.currentTime = time.time() - self.delta_time
                self.lastFrameTime = self.currentTime

    def load_level(self, level_path: str):
        self.level_path = level_path
        self.has_level_to_load = True
        self.level_running = False

    def load_frontend(self):
        self.load_level("Assets/Levels/Frontend/Frontend.json")

    def check_level_load(self):
        if self.has_level_to_load == True:
            if self.level != None:
                del self.level

            self.level = Level(self, self.level_path)
            self.has_level_to_load = False

    @staticmethod
    def find_in_argument_variable(argument_name: str):
        for arg in sys.argv:
            if argument_name + "=" in arg:
                return arg.split("=")[1]
        return None
    
    def is_debugging(self):
        return sys.gettrace() is not None