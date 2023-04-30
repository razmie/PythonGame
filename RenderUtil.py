import numpy as np
import pygame
import World

class RenderUtil:
    @staticmethod
    def get_polygon_bounds(vertices):
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        
        for vertex in vertices:
            x, y = vertex
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
                
        return ((min_x, min_y), (max_x, max_y))

    def lerp(self, p1, p2, f):
        return p1 + f * (p2 - p1)

    def lerp2d(self, p1, p2, f):
        return tuple(self.lerp( p1[i], p2[i], f) for i in range(2))

    def draw_quad(self, surface, quad, img):
        points = dict()

        for i in range(img.get_size()[1]+1):
            b = self.lerp2d(quad[1], quad[2], i/img.get_size()[1])
            c = self.lerp2d(quad[0], quad[3], i/img.get_size()[1])
            for u in range(img.get_size()[0]+1):
                a = self.lerp2d(c, b, u/img.get_size()[0])
                points[(u,i)] = a

        for x in range(img.get_size()[0]):
            for y in range(img.get_size()[1]):
                pygame.draw.polygon(
                    surface,
                    img.get_at((x,y)),
                    [points[(a,b)] for a, b in [(x,y), (x,y+1), (x+1,y+1), (x+1,y)]] 
                )