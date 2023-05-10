import World
from Maths import Vector2
from Nodes.PolygonNode import PolygonNode

class PolygonPhsxBody(PolygonNode):
    def __init__(self, world: World):
        super().__init__(world)
        self.new_position = Vector2(0, 0)
        self.force = Vector2(0, 0)
        self.mass = 100
        self.static = False
        self.velocity = Vector2(0, 0)
        self.impulse = Vector2(0, 0)

    def set(self, position: Vector2, vertices: list[Vector2], pivot: tuple, color: tuple):
        self.new_position = position
        self.color = color
        super().set(position, vertices, pivot, color)

    def apply_impulse(self, impulse: Vector2, ignore_mass: bool = False):
        if ignore_mass:
            self.impulse = self.impulse + impulse * self.mass
        else:
            self.impulse = self.impulse + impulse
