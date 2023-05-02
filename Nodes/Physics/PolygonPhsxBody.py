import numpy as np
import World
from Nodes.PolygonNode import PolygonNode

class PolygonPhsxBody(PolygonNode):
    def __init__(self, world: World):
        super().__init__(world)

        self.old_position = np.array([0, 0])
        self.new_position = np.array([0, 0])
        self.mass = 1
        self.acceleration = np.array([0, 0])
        self.apply_gravity = True

    def set(self, position: np.array, vertices: list, pivot: tuple, color: tuple):
        self.old_position = position
        self.new_position = position
        self.color = color
        super().set(position, vertices, pivot, color)

