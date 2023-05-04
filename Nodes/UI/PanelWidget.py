import pygame, math
import pygame.gfxdraw
import World
from Maths import Maths, Vector2, Matrix3x3
from Nodes.NodeBase import NodeBase

class PanelWidget(NodeBase):
    def __init__(self, world: World, name: str = None):
        super().__init__(world)
        self.name = name
        self.position = Vector2(0,0)

        self.size = Vector2(100,100)
        self.color = (255,0,0)
        self.pivot = Vector2(0,0)

        self.vertices = self.create_polygon_vertices()
        self.rotated_vertices = []

        self.draw_border: bool = False
        self.border_color: tuple = (0,0,0)

    def load(self, data):
        super.load(data)
        self.size.set(data.get("size") or self.size)
        self.color = data.get("color") or self.color
        self.pivot.set(data.get("pivot") or self.pivot)
        self.vertices = data.get("vertices") or self.vertices
       
    def create_polygon_vertices(self):
        vertices = []
        origin = Vector2(0,0)
        vertices.append(Vector2(origin.x,                origin.y))
        vertices.append(Vector2(origin.x + self.size.x,  origin.y))
        vertices.append(Vector2(origin.x + self.size.x,  origin.y + self.size.y))
        vertices.append(Vector2(origin.x,                origin.y + self.size.y))
        return vertices
        
    # def create_polygon_surface(self, polygon_bounds, vertices):
    #     surface_size = (polygon_bounds[2] - polygon_bounds[0], polygon_bounds[3] - polygon_bounds[1])

    #     surface = pygame.Surface(surface_size, pygame.SRCALPHA)
    #     pygame.gfxdraw.filled_polygon(surface, vertices, self.color)
    #     pygame.gfxdraw.aapolygon(surface, vertices, (0, 0, 0))
    #     return surface

    def construct_matrix(self):
        trans_mat = Matrix3x3([[1, 0, self.position.x], [0, 1, self.position.y], [0, 0, 1]])
        rot_mat = Matrix3x3([[math.cos(self.rotation), -math.sin(self.rotation), 0], [math.sin(self.rotation), math.cos(self.rotation), 0], [0, 0, 1]])
        scale_mat = Matrix3x3([[self.scale.x, 0, 0], [0, self.scale.y, 0], [0, 0, 1]])

        pivot = Vector2(-self.pivot.x * self.size.x,    -self.pivot.y * self.size.y)
        pivot_mat = Matrix3x3([[1, 0, pivot.x], [0, 1, pivot.y], [0, 0, 1]])

        return trans_mat @ rot_mat @ scale_mat @ pivot_mat
     
    # def update(self, delta_time):
    #     self.rotation += delta_time * 0.1
    #     self.reconstruct_body()
    #     pass

    def draw(self, surface):
        if len(self.rotated_vertices) > 2:
            verts = Maths.get_vertices(self.rotated_vertices)
            pygame.gfxdraw.filled_polygon(surface, verts, self.color)

            if self.draw_border == True:
                pygame.gfxdraw.aapolygon(surface, verts, self.border_color)

    def reconstruct_body(self):
        self.rotated_vertices = []
        for i in range(len(self.vertices)):
            rot_vert = self.get_matrix() @ self.vertices[i]
            self.rotated_vertices.append(rot_vert)
