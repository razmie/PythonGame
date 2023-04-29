import pygame
import pygame.gfxdraw
import numpy as np
from enum import Enum
import math
import World
from Nodes.UI.PanelWidget import PanelWidget
from Nodes.NodeBase import NodeBase
from CollisionUtil import CollisionUtil

class ButtonWidget(PanelWidget):
    class TextJustification(Enum):
        LEFT = 1
        MIDDLE = 2
        RIGHT = 3

    justification = TextJustification.LEFT
    padding = 8

    def __init__(self, world: World, name: str = None, on_click_delegate=None):
        super().__init__(world, name)
        self.on_click_delegate = on_click_delegate

    def set(self, position: np.array, size: np.array, color: tuple, font_id: str, text: str, text_color: tuple):
        self.position = position
        self.size = size
        self.color = color
        self.vertices = self.create_polygon_vertices()

        font_asset = self.world.assets.get_font_asset(font_id)
        self.rendered_text = font_asset.font.render(text, True, (0,0,0))

        self.reconstruct_body()

    def handle_events(self):
        super().handle_events()
        for event in self.game.cached_events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if CollisionUtil.is_point_in_polygon(event.pos, self.rotated_vertices):
                    if self.on_click_delegate:
                        self.on_click_delegate(self)

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        
        surface.blit(self.rendered_text, self.rendered_rect)

    def reconstruct_body(self):
        super().reconstruct_body()
        bounds = self.get_polygon_bounds(self.rotated_vertices)
        
        self.rendered_rect = self.rendered_text.get_rect()
        min = np.array(bounds[0])
        max = np.array(bounds[1])

        if self.justification == ButtonWidget.TextJustification.LEFT:
            text_pos = (self.padding + min[0], min[1] + (max[1] - min[1]) * 0.5)
            self.rendered_rect.midleft = text_pos 
        elif self.justification == ButtonWidget.TextJustification.MIDDLE:
            text_pos = (min[0] + (max[0] - min[0]) * 0.5, min[1] + (max[1] - min[1]) * 0.5)
            self.rendered_rect.center = text_pos
        elif self.justification == ButtonWidget.TextJustification.RIGHT:
            text_pos = (max[0] - self.padding, min[1] + (max[1] - min[1]) * 0.5)
            self.rendered_rect.midright = text_pos





