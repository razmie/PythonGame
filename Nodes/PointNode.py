import pygame
import World
from Maths import Vector2
from Nodes.NodeBase import NodeBase

class PointNode(NodeBase):
    def __init__(self, world: World):
        super().__init__(world)
        self.position = Vector2(0,0)
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
        position = Vector2(0, 0)
        position = self.get_matrix() @ position
        return position
