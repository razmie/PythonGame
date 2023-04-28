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

    def load(self, data):
        self.position = data.get("position") or self.position
        self.scale = data.get("scale") or self.scale
        self.rotation = data.get("rotation") or self.rotation
        self.size = data.get("size") or self.size
        self.color = data.get("color") or self.color

    def update(self, deltaTime: float):
        #self.rotation += deltaTime
        pass

    def draw(self):
        position = self.get_world_position()
        Renderer.draw_point(self.world, position, self.size, self.color)

    def get_world_position(self):
        mat_position = np.array([0, 0, 1])
        mat_position = self.get_matrix() @ mat_position
        return np.array([mat_position[0], mat_position[1]])
