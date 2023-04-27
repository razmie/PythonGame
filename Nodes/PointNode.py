import numpy as np
import pygame
import World
from Nodes.NodeBase import NodeBase
from Renderer import Renderer

class PointNode(NodeBase):
    def __init__(self, new_world: World, new_position = np.array([0, 0]), new_size = 10, new_color = (0, 0, 255)):
        super().__init__(new_world)
        self.position = new_position
        self.size = new_size
        self.color = new_color

    def update(self, deltaTime: float):
        pass

    def draw(self):
        Renderer.draw_point(self.world, self.position, self.size, self.color)