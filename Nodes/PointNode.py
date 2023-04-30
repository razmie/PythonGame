import numpy as np
import pygame
import World
from Nodes.NodeBase import NodeBase
from RenderUtil import RenderUtil

class PointNode(NodeBase):
    def __init__(self, world: World):
        super().__init__(world)
        self.position = np.array([0,0])
        self.size = 10
        self.color = (0, 0, 255)

    def load(self, data):
        super().load(data)
        self.size = data.get("size") or self.size
        self.color = data.get("color") or self.color

    def update(self, deltaTime: float):
        #self.rotation += deltaTime
        pass

    def draw(self, surface: pygame.Surface):
        position = self.get_world_position()
        self.world.draw_point(position, self.size, self.color)

    def get_world_position(self):
        mat_position = np.array([0, 0, 1])
        mat_position = self.get_matrix() @ mat_position
        return np.array([mat_position[0], mat_position[1]])
