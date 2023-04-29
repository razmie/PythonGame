import pygame
import pygame.gfxdraw
import numpy as np
import World
from Nodes.UI.PanelWidget import PanelWidget
from Nodes.NodeBase import NodeBase
from CollisionUtil import CollisionUtil

class ButtonWidget(PanelWidget):
    def __init__(self, world: World, on_click_delegate=None):
        super().__init__(world)
        
        self.on_click_delegate = on_click_delegate

    def set(self, position: np.array, size: np.array, color: tuple):
        self.position = position
        self.size = size
        self.color = color
        self.vertices = self.create_polygon_vertices()
       
    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if CollisionUtil.is_point_in_polygon(event.pos, self.rotated_vertices):
                    if self.on_click_delegate:
                        self.on_click_delegate(self)
