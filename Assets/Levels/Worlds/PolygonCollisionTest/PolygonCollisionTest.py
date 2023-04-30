from ScriptBase import ScriptBase
import pygame
import numpy as np
import World
from RenderUtil import RenderUtil

class PolygonCollisionTest(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)
        pass

    def draw(self, surface: pygame.Surface):
        RenderUtil.draw_point(self.world, (100,100), 10, (255,0,0))
        pass