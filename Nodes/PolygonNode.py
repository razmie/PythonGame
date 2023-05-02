import pygame
import pygame.gfxdraw
import numpy as np
import Nodes.NodeBase
import World
from RenderUtil import RenderUtil

class PolygonNode(Nodes.NodeBase.NodeBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.vertices = []
        self.world_vertices = []
        self.pivot = np.array([0,0])
        self.color = (0,0,0)
        self.bounds = ((0,0), (0,0))

    def construct_matrix(self):
        trans_mat = np.array([[1, 0, self.position[0]], [0, 1, self.position[1]], [0, 0, 1]])
        rot_mat = np.array([[np.cos(self.rotation), -np.sin(self.rotation), 0], [np.sin(self.rotation), np.cos(self.rotation), 0], [0, 0, 1]])
        scale_mat = np.array([[self.scale[0], 0, 0], [0, self.scale[1], 0], [0, 0, 1]])

        bounds = RenderUtil.get_polygon_bounds(self.vertices)
        size = ((bounds[1][0] - bounds[0][0]), (bounds[1][1] - bounds[0][1]))
        pivot = (-self.pivot[0] * size[0], -self.pivot[1] * size[1])
        pivot_mat = np.array([[1, 0, pivot[0]], [0, 1, pivot[1]], [0, 0, 1]])

        return trans_mat @ rot_mat @ scale_mat @ pivot_mat
    
    def set(self, position: np.array, vertices: list, pivot: tuple, color: tuple):
        self.position = position
        self.vertices = vertices
        self.pivot = np.array(pivot)
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
            mat_position = np.array([self.vertices[i][0], self.vertices[i][1], 1])
            mat_position = self.get_matrix() @ mat_position
            self.world_vertices.append((mat_position[0], mat_position[1]))

        self.bounds = RenderUtil.get_polygon_bounds(self.world_vertices)
