import pygame
import pygame.gfxdraw
import numpy as np
import World
from Nodes.NodeBase import NodeBase

class PanelWidget(NodeBase):
    def __init__(self, world: World, name: str = None):
        super().__init__(world)
        self.name = name
        self.position = np.array([0,0])

        self.size = np.array([100,100])
        self.color = (255,0,0)
        self.pivot = np.array([0,0])

        self.vertices = self.create_polygon_vertices()
        self.rotated_vertices = []

        self.draw_border: bool = False
        self.border_color: tuple = (0,0,0)

    def load(self, data):
        super.load(data)
        self.size = data.get("size") or self.size
        self.color = data.get("color") or self.color
        self.pivot = data.get("pivot") or self.pivot
        self.vertices = data.get("vertices") or self.vertices
       
    def create_polygon_vertices(self):
        vertices = []
        origin = (0,0)
        vertices.append((origin[0],                 origin[1]))
        vertices.append((origin[0] + self.size[0],  origin[1]))
        vertices.append((origin[0] + self.size[0],  origin[1] + self.size[1]))
        vertices.append((origin[0],                 origin[1] + self.size[1]))
        return vertices
        
    # def create_polygon_surface(self, polygon_bounds, vertices):
    #     surface_size = (polygon_bounds[2] - polygon_bounds[0], polygon_bounds[3] - polygon_bounds[1])

    #     surface = pygame.Surface(surface_size, pygame.SRCALPHA)
    #     pygame.gfxdraw.filled_polygon(surface, vertices, self.color)
    #     pygame.gfxdraw.aapolygon(surface, vertices, (0, 0, 0))
    #     return surface

    def construct_matrix(self):
        trans_mat = np.array([[1, 0, self.position[0]], [0, 1, self.position[1]], [0, 0, 1]])
        rot_mat = np.array([[np.cos(self.rotation), -np.sin(self.rotation), 0], [np.sin(self.rotation), np.cos(self.rotation), 0], [0, 0, 1]])
        scale_mat = np.array([[self.scale[0], 0, 0], [0, self.scale[1], 0], [0, 0, 1]])

        pivot = (-self.pivot[0] * self.size[0],    -self.pivot[1] * self.size[1])
        pivot_mat = np.array([[1, 0, pivot[0]], [0, 1, pivot[1]], [0, 0, 1]])

        return trans_mat @ rot_mat @ scale_mat @ pivot_mat
     
    # def update(self, delta_time):
    #     self.rotation += delta_time * 0.1
    #     self.reconstruct_body()
    #     pass

    def draw(self, surface):
        if len(self.rotated_vertices) > 2:
            pygame.gfxdraw.filled_polygon(surface, self.rotated_vertices, self.color)

            if self.draw_border == True:
                pygame.gfxdraw.aapolygon(surface, self.rotated_vertices, self.border_color)

    def reconstruct_body(self):
        self.rotated_vertices = []
        for i in range(len(self.vertices)):
            mat_position = np.array([self.vertices[i][0], self.vertices[i][1], 1])
            mat_position = self.get_matrix() @ mat_position
            self.rotated_vertices.append((mat_position[0], mat_position[1]))
