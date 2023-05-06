import math
import World
from Maths import Vector2, Matrix3x3, Rect
import Nodes.NodeBase
from RenderUtil import RenderUtil

class PolygonNode(Nodes.NodeBase.NodeBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.vertices = []
        self.world_vertices = []
        self.pivot = Vector2(0,0)
        self.color = (0,0,0)
        self.bounds = Rect(0, 0, 0, 0)

    def construct_matrix(self):
        trans_mat = Matrix3x3([[1, 0, self.position.x], [0, 1, self.position.y], [0, 0, 1]])
        rot_mat = Matrix3x3([[math.cos(self.rotation), -math.sin(self.rotation), 0], [math.sin(self.rotation), math.cos(self.rotation), 0], [0, 0, 1]])
        scale_mat = Matrix3x3([[self.scale.x, 0, 0], [0, self.scale.y, 0], [0, 0, 1]])

        local_bounds = RenderUtil.get_polygon_bounds(self.vertices)
        size = local_bounds.size
        pivot = Vector2(-self.pivot.x * size.x, -self.pivot.x * size.y)
        pivot_mat = Matrix3x3([[1, 0, pivot.x], [0, 1, pivot.y], [0, 0, 1]])

        return trans_mat @ rot_mat @ scale_mat @ pivot_mat
    
    def set(self, position: Vector2, vertices: list[Vector2], pivot: Vector2, color: tuple):
        self.position = position
        self.vertices = vertices
        self.pivot = pivot
        self.color = color

        self.reconstruct_body()
     
    # def update(self, delta_time):
    #     self.rotation += delta_time * 0.1
    #     self.reconstruct_body()
    #     pass

    def draw(self, surface):
        self.world.draw_polygon(self.world_vertices, self.color)

    def reconstruct_body(self):
        self.world_vertices = []
        for i in range(len(self.vertices)):
            position = self.get_matrix() @ self.vertices[i]
            self.world_vertices.append(position)

        self.bounds = RenderUtil.get_polygon_bounds(self.world_vertices)
        pass
