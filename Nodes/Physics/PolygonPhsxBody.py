import World
from Maths import Vector2
from Nodes.PolygonNode import PolygonNode

class PolygonPhsxBody(PolygonNode):
    def __init__(self, world: World):
        super().__init__(world)
        self.force = Vector2(0, 0)
        self.mass = 100
        self.static = False
        self.velocity = Vector2(0, 0)

    def set(self, position: Vector2, vertices: list[Vector2], pivot: tuple, color: tuple):
        self.color = color
        super().set(position, vertices, pivot, color)

    def apply_force(self, force: Vector2):
            self.force = self.force + force
