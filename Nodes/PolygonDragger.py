import pygame
from Maths import Vector2
from Input import Input
from Nodes.NodeBase import NodeBase
from CollisionUtil import CollisionUtil

class PolygonDragger(NodeBase):
    def __init__(self, world):
        super().__init__(world)
        self.hovering = False
        self.dragging = False
        self.bounds_colliding = False
        self.colliding = False
        self.click_offset = Vector2(0,0)
        self.can_draw = False
        self.world_mouse_position = Vector2(0,0)

    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.hovering:
                        polygon = self.parent_node
                        if polygon == None:
                            return
        
                        self.click_offset = polygon.position - self.world_mouse_position
                        self.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.dragging:
                        self.dragging = False

    def update(self, deltaTime: float):
        mouse_position = Input.get_mouse_position()
        self.world_mouse_position = self.world.camera.screen_to_world(mouse_position)

        polygon = self.parent_node
        if polygon == None:
            return

        if CollisionUtil.is_point_in_polygon(self.world_mouse_position, polygon.world_vertices):
            if self.hovering == False:
                self.hovering = True
        else:
            if self.hovering:
                self.hovering = False

        if self.dragging:
            polygon.position = self.world_mouse_position + self.click_offset
            polygon.reconstruct_body()
