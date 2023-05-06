from ScriptBase import ScriptBase
import pygame
import World
from Input import Input
from Maths import Vector2
from Nodes.NodeBase import NodeBase
from Nodes.PolygonNode import PolygonNode
from Nodes.PolygonDragger import PolygonDragger
from CollisionUtil import CollisionUtil
from RenderUtil import RenderUtil
from Maths import Vector2
from GTK import GTK

class PolyPolyCollisionTest(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.world.camera.position = Vector2(0,0)

        self.polygon1 = PolygonNode(world)
        vertices = [
            Vector2(0,0),
            Vector2(100,0),
            Vector2(100,100),
            Vector2(0,100)
        ]
        self.polygon1.set(Vector2(-200,-200), vertices, Vector2(0.5,0.5), RenderUtil.GREEN)
        self.world.nodes.append(self.polygon1)

        self.polyDragger1 = PolygonDragger(world)
        self.polyDragger1.parent_node = self.polygon1
        self.world.nodes.append(self.polyDragger1)

        self.polygon2 = PolygonNode(world)
        vertices = [
            Vector2(0,0),
            Vector2(100,-50),
            Vector2(150,100),
            Vector2(50,150),
            Vector2(-50,100)
        ]
        self.polygon2.rotation = 0.5
        self.polygon2.set(Vector2(250,-100), vertices, Vector2(0.5,0.5), RenderUtil.GREEN)
        self.world.nodes.append(self.polygon2)

        self.polyDragger2 = PolygonDragger(world)
        self.polyDragger2.parent_node = self.polygon2
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

    def update(self, deltaTime: float):
        # Do collision detection
        poly_count = len(self.poly_info_list)
        for i in range(poly_count):
            for j in range(i+1, poly_count):
                poly_info1 = self.poly_info_list[i]
                poly_info2 = self.poly_info_list[j]

                polygon1, dragger1 = poly_info1
                polygon2, dragger2 = poly_info2

                #coll = GTK.intersect(polygon1.world_vertices, polygon2.world_vertices)
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
                if dragger.hovering:
                    polygon.color = RenderUtil.BLUE
                else:
                    polygon.color = RenderUtil.GREEN
                

    def draw(self, surface: pygame.Surface):
        for poly_info in self.poly_info_list:
            polygon, dragger = poly_info

            if dragger.bounds_colliding:
                rect = (polygon.bounds[0], (polygon.bounds[1].x-polygon.bounds[0].x, (polygon.bounds[1].y-polygon.bounds[0].y)))
                self.world.draw_rect(rect, (0,0,0), 2)