import pygame
import World
from Maths import Vector2
from Nodes.NodeBase import NodeBase

class LineNode(NodeBase):
    def __init__(self, new_world: World):
        super().__init__(new_world)
        self.position = Vector2(0,0)
        self.end_position = Vector2(100,100)
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
        start= Vector2(0, 0)
        start = self.get_matrix() @ start

        end = Vector2(self.end_position[0], self.end_position[1])
        end = self.get_matrix() @ end

        self.world.draw_line(self.world, start, end, self.width, self.color)