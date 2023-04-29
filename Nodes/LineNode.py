import numpy as np
import pygame
import World
from Nodes.NodeBase import NodeBase
from Renderer import RenderUtil

class LineNode(NodeBase):
    def __init__(self, new_world: World):
        super().__init__(new_world)
        self.position = np.array([0,0])
        self.end_position = np.array([100,100])
        self.width = 1
        self.color = (0, 0, 255)

    def load(self, data):
        super.load(data)
        self.end_position = data.get("end_position") or self.end_position
        self.width = data.get("width'") or self.width
        self.color = data.get("color") or self.color

    def update(self, deltaTime: float):
        pass

    def draw(self, surface: pygame.Surface):
        mat_position = np.array([0, 0, 1])
        mat_position = self.get_matrix() @ mat_position
        start = np.array([mat_position[0], mat_position[1]])
        mat_position = np.array([self.end_position[0], self.end_position[1], 1])
        mat_position = self.get_matrix() @ mat_position
        end = np.array([mat_position[0], mat_position[1]])

        RenderUtil.draw_line(self.world, start, end, self.width, self.color)