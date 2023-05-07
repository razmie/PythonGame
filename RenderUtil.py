import pygame
from Maths import Vector2, Rect

class RenderUtil:
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    CYAN = (0,255,255)
    YELLOW = (255,255,0)
    MAGENTA = (255,0,255)
    WHITE = (255,255,255)
    ORANGE = (255,128,0)
    GRAY = (128,128,128)
    BLACK = (0,0,0)

    LIGHT_RED = (255,128,128)
    LIGHT_GREEN = (128,255,128)
    LIGHT_BLUE = (128,128,255)
    DARK_RED = (128,0,0)
    DARK_GREEN = (0,128,0)
    DARK_BLUE = (0,0,128)

    @staticmethod
    def get_polygon_bounds(vertices):
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        
        for vertex in vertices:
            if vertex.x < min_x:
                min_x = vertex.x
            if vertex.y < min_y:
                min_y = vertex.y
            if vertex.x > max_x:
                max_x = vertex.x
            if vertex.y > max_y:
                max_y = vertex.y

        #return Vector2(min_x, min_y), Vector2(max_x, max_y)
        return Rect(min_x, min_y, max_x-min_x, max_y-min_y) 

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