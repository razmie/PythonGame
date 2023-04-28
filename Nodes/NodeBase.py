import numpy as np
import Game
import World

class NodeBase:
    game: Game = None
    world: World = None
    position = np.array([0, 0])
    rotation = 0
    scale = np.array([1, 1])
    parent_node = None

    def __init__(self, new_world: World):
        self.world = new_world
        self.game = new_world.game

    def update(self, deltaTime: float):
        pass

    def draw(self):
        pass

    def construct_matrix(self):
        trans_mat = np.array([[1, 0, self.position[0]], [0, 1, self.position[1]], [0, 0, 1]])
        rot_mat = np.array([[np.cos(self.rotation), -np.sin(self.rotation), 0], [np.sin(self.rotation), np.cos(self.rotation), 0], [0, 0, 1]])
        scale_mat = np.array([[self.scale[0], 0, 0], [0, self.scale[1], 0], [0, 0, 1]])

        return trans_mat @ rot_mat @ scale_mat
    
    def get_matrix(self):
        matrix = self.construct_matrix()

        parent_node = self.parent_node
        while parent_node is not None:
            matrix = parent_node.construct_matrix() @ matrix
            parent_node = parent_node.parent_node

        return matrix
        
        



