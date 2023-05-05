import pygame, math
import Game, World
from Maths import Vector2, Matrix3x3

class NodeBase:
    game: Game = None
    world: World = None
    
    def __init__(self, world: World):
        self.world = world
        self.game = world.game

        self.name: str = "No Name"
        self.position: Vector2 = Vector2()
        self.rotation: float = 0
        self.scale: Vector2 = Vector2(1, 1)

        self.cached_matrix: Matrix3x3 = None
        self.cached_matrix_update_id = -1

        self.parent_node = None

        self.can_draw = True

    def handle_events(self):
        pass

    def update(self, deltaTime: float):
        pass

    def draw(self, surface: pygame.Surface):
        pass

    def load(self, data):
        self.name = data.get("name") or self.name
        self.position = data.get("position") or self.position
        self.rotation = data.get("rotation") or self.rotation
        self.scale = data.get("scale") or self.scale

    def construct_matrix(self):
        trans_mat = Matrix3x3([[1, 0, self.position.x], [0, 1, self.position.y], [0, 0, 1]])
        rot_mat = Matrix3x3([[math.cos(self.rotation), -math.sin(self.rotation), 0], [math.sin(self.rotation), math.cos(self.rotation), 0], [0, 0, 1]])
        scale_mat = Matrix3x3([[self.scale.x, 0, 0], [0, self.scale.y, 0], [0, 0, 1]])

        return trans_mat @ rot_mat @ scale_mat
    
    def get_matrix(self):

        #if self.cached_matrix_update_id == self.world.game.update_count:
        #    return self.cached_matrix

        matrix = self.construct_matrix()

        parent_node = self.parent_node
        while parent_node is not None:
            matrix = parent_node.construct_matrix() @ matrix
            parent_node = parent_node.parent_node

        self.cached_matrix = matrix
        self.cached_matrix_update_id = self.world.game.update_count

        return self.cached_matrix
        
        



