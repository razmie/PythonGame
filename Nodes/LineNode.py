import numpy as np
import pygame
import World
from Nodes.NodeBase import NodeBase
from Renderer import Renderer

class LineNode(NodeBase):
    def __init__(self, new_world: World, new_start = np.array([0, 0]), new_end = np.array([100, 100]), new_width = 1, new_color = (0, 0, 255)):
        super().__init__(new_world)
        self.position = new_start
        self.end_position = new_end
        self.width = new_width
        self.color = new_color

    def load(self, data):
        self.position = data.get("position") or self.position
        self.end_position = data.get("end_position") or self.end_position
        self.scale = data.get("scale") or self.scale
        self.rotation = data.get("rotation") or self.rotation
        self.width = data.get("width'") or self.width
        self.color = data.get("color") or self.color

    def update(self, deltaTime: float):
        pass

    def draw(self):
        mat_position = np.array([0, 0, 1])
        mat_position = self.get_matrix() @ mat_position
        start = np.array([mat_position[0], mat_position[1]])
        mat_position = np.array([self.end_position[0], self.end_position[1], 1])
        mat_position = self.get_matrix() @ mat_position
        end = np.array([mat_position[0], mat_position[1]])

        Renderer.draw_line(self.world, start, end, self.width, self.color)