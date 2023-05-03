from ScriptBase import ScriptBase
import pygame
import numpy as np
import World
from Nodes.NodeBase import NodeBase
from Nodes.PolygonNode import PolygonNode
from CollisionUtil import CollisionUtil
from RenderUtil import RenderUtil
from GTK import GTK

class PolyDragger(NodeBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.hovering = False
        self.dragging = False
        self.bounds_colliding = False
        self.colliding = False
        self.click_offset = np.array([0,0])

class PolyPolyCollisionTest(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.world.camera.position = np.array([0,0])
        self.mouse_down = False

        self.polygon1 = PolygonNode(world)
        vertices = [
            [0,0],
            [100,0],
            [100,100],
            [0,100]
        ]
        self.polygon1.set((-200,-200), vertices, (0.5,0.5), RenderUtil.GREEN)
        self.world.nodes.append(self.polygon1)

        self.polyDragger1 = PolyDragger(world)
        self.world.nodes.append(self.polyDragger1)

        self.polygon2 = PolygonNode(world)
        vertices = [
            [0,0],
            [100,-50],
            [150,100],
            [50,150],
            [-50,100]
        ]
        self.polygon2.rotation = 0.5
        self.polygon2.set((250,-100), vertices, (0.5,0.5), RenderUtil.GREEN)
        self.world.nodes.append(self.polygon2)

        self.polyDragger2 = PolyDragger(world)
        self.world.nodes.append(self.polyDragger2)

        self.poly_info_list = [
                [self.polygon1, self.polyDragger1],
                [self.polygon2, self.polyDragger2]
            ]

    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.load_level("Assets/Levels/Frontend/Frontend.json")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True

                    for poly_info in self.poly_info_list:
                        polygon, dragger = poly_info
                        if dragger.hovering:
                            dragger.click_offset = polygon.position - self.world_mouse_position
                            dragger.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False

                    for poly_info in self.poly_info_list:
                        polygon, dragger = poly_info
                        if dragger.dragging:
                            dragger.dragging = False

    def update(self, deltaTime: float):
        mouse_position = pygame.mouse.get_pos()
        self.world_mouse_position = self.world.camera.screen_to_world(mouse_position)

        for poly_info in self.poly_info_list:
            polygon, dragger = poly_info

            if CollisionUtil.is_point_in_polygon(self.world_mouse_position, polygon.world_vertices):
                if dragger.hovering == False:
                    dragger.hovering = True
                    polygon.color = RenderUtil.BLUE
            else:
                if dragger.hovering:
                    dragger.hovering = False
                    polygon.color = RenderUtil.GREEN

            if dragger.dragging:
                polygon.position = self.world_mouse_position + dragger.click_offset
                polygon.reconstruct_body()

        # Do collision detection
        poly_count = len(self.poly_info_list)
        for i in range(poly_count):
            for j in range(i+1, poly_count):
                poly_info1 = self.poly_info_list[i]
                poly_info2 = self.poly_info_list[j]

                polygon1, dragger1 = poly_info1
                polygon2, dragger2 = poly_info2

                ##coll = GTK.intersect(polygon1.world_vertices, polygon2.world_vertices)
                #print(coll)

                if CollisionUtil.are_bounding_boxes_inside(polygon1.bounds, polygon2.bounds):
                    dragger1.bounds_colliding = True
                    dragger2.bounds_colliding = True

                    if CollisionUtil.are_polygons_intersecting(polygon1.world_vertices, polygon2.world_vertices):
                        dragger1.colliding = True
                        dragger2.colliding = True
                    else:
                        dragger1.colliding = False
                        dragger2.colliding = False
                else:
                    dragger1.bounds_colliding = False
                    dragger1.colliding = False
                    dragger2.bounds_colliding = False
                    dragger2.colliding = False
            

        for poly_info in self.poly_info_list:
            polygon, dragger = poly_info

            if dragger.colliding:
                polygon.color = RenderUtil.RED
            elif dragger.dragging or dragger.hovering:
                polygon.color = RenderUtil.BLUE
            else:
                polygon.color = RenderUtil.GREEN
                

    def draw(self, surface: pygame.Surface):
        for poly_info in self.poly_info_list:
            polygon, dragger = poly_info

            if dragger.bounds_colliding:
                rect = (polygon.bounds[0],(polygon.bounds[1][0]-polygon.bounds[0][0],(polygon.bounds[1][1]-polygon.bounds[0][1])))
                self.world.draw_rect(rect, (0,0,0), 2)