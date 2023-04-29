import pygame
import pygame.gfxdraw
import math
import World
from Nodes.NodeBase import NodeBase

class ButtonWidget(NodeBase):
    def __init__(self, world: World, position: tuple, size: tuple, font_id: str, text: str, color: tuple, on_click_delegate=None):
        super().__init__(world)
        self.position = position
        self.size = size
        self.angle = 0
        self.text = text
        self.color = color
        self.on_click_delegate = on_click_delegate

        self.sides = 8
        self.radius = 100
        self.vertices = self.get_polygon_vertices()
        self.widget_surface = self.create_polygon_surface()
        self.rotated_surface = pygame.transform.rotate(self.widget_surface, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=self.vertices[0])
       





        # font_asset = world.assets.get_font_asset(font_id)
        
        # rendered_text = font_asset.font.render(self.text, True, self.color)

        # self.rotated_text = pygame.transform.rotate(rendered_text, self.angle)
        # self.rotated_rect = self.rotated_text.get_rect()
        # self.rotated_rect.center = self.position

        # self.button_surface = pygame.Surface((self.size[0], self.size[1]))

    def get_polygon_vertices(self):
        vertices = []
        for i in range(self.sides):
            angle_deg = 360.0 / self.sides * i
            angle_rad = math.radians(angle_deg)
            x = self.position[0] + math.cos(angle_rad) * self.radius
            y = self.position[1] + math.sin(angle_rad) * self.radius
            vertices.append((x, y))
        return vertices
        
    def create_polygon_surface(self):
        surface = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.gfxdraw.filled_polygon(surface, self.vertices, self.color)
        pygame.gfxdraw.aapolygon(surface, self.vertices, (0, 0, 0))
        return surface
     
    def draw(self, surface):
        surface.blit(self.rotated_surface, self.rotated_rect)


        # rotated_surface = pygame.transform.rotate(self.rect_surface, 111)
        # rotated_rect = rotated_surface.get_rect()
        # rotated_rect.center = self.rect.center

        # surface.blit(rotated_surface, rotated_rect)


        # rotated_surface = pygame.transform.rotate(self.button_surface, self.angle)
        # rotated_rect = self.rotated_surface.get_rect(center=self.rect.center)
        # surface.blit(rotated_surface, rotated_rect)

        # surface.blit(self.rotated_text, self.rotated_rect)
        # surface.blit(self.rotated_surface, self.rotated_rect)
        # pygame.draw.rect(surface, (255, 0, 0), self.rotated_rect, 2)
       
    # def handle_events(self):
    #     for event in self.game.cached_events:
    #         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    #             if self.rotated_rect.collidepoint(event.pos):
    #                 if self.on_click_delegate:
    #                     self.on_click_delegate()