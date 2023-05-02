import numpy as np
import World
from Nodes.PointNode import PointNode

class PointPhsxBody(PointNode):
    def __init__(self, world: World):
        super().__init__(world)

        self.old_position = np.array([0, 0])
        self.new_position = np.array([0, 0])
        self.mass = 1
        self.acceleration = np.array([0, 0])

    def set(self, position: np.array, size: float, color: tuple):
        self.position = position
        self.old_position = position
        self.new_position = position
        self.size = size
        self.color = color

