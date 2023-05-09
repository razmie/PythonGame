import os, pygame
import pymunk, pymunk.pygame_util
import World
from ScriptBase import ScriptBase
from PymunkUtil import PymunkDrawOptions

class PymunkTest(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)
        self.script_file_path = os.path.abspath(__file__)
        self.game.screen_color = (0,0,0)
        
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 981.0)
        self.draw_options = PymunkDrawOptions(self.world)

        self.add_object()

    def handle_events(self):
        super().handle_events()
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.load_frontend()

    def update(self, deltaTime: float):
        super().update(deltaTime)

        self.space.debug_draw(self.draw_options)
        self.space.step(deltaTime)

    def add_object(self):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (300, 300)
        shape = pymunk.Circle(body, 50)
        shape.mass = 10
        self.space.add(body, shape)
        return shape
