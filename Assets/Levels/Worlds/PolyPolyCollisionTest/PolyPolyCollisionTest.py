from ScriptBase import ScriptBase
import pygame
import World
from Input import Input
from Maths import Vector2, Rect
from Nodes.NodeBase import NodeBase
from Nodes.PolygonNode import PolygonNode
from Nodes.PolygonDragger import PolygonDragger
from CollisionUtil import CollisionUtil
from RenderUtil import RenderUtil
from Maths import Vector2
from GTK import GTK

class PolyPolyCollisionTest(ScriptBase):
    class StepInfo:
        def __init__(self):
            self.test_edge1_pos1 = Vector2()
            self.test_edge1_pos2 = Vector2()
            self.test_edge1_pos1_idx = 0
            self.test_edge1_pos2_idx = 0
            self.test_polygon: PolygonNode = None

    def __init__(self, world: World):
        super().__init__(world)

        self.world.camera.position = Vector2(0,0)
        self.world.game.screen_color = (0,0,0)

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
        
        # Use for stepping through the collision process
        self.step_info = self.StepInfo()
        self.coll_stepper = self.step_through_polygons()
        self.coll_step_time = 0
        self.coll_step_time_max = 1

    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.load_level("Assets/Levels/Frontend/Frontend.json")

    def update(self, deltaTime: float):
        self.process_collision()

        for poly_info in self.poly_info_list:
            polygon, dragger = poly_info

            if dragger.colliding:
                polygon.color = RenderUtil.RED
            elif dragger.dragging or dragger.hovering:
                polygon.color = RenderUtil.DARK_GREEN
            else:
                if dragger.hovering:
                    polygon.color = RenderUtil.BLUE
                else:
                    polygon.color = RenderUtil.GREEN

        self.process_collision_step(deltaTime)

    def draw(self, surface: pygame.Surface):
        for poly_info in self.poly_info_list:
            polygon, dragger = poly_info

            if dragger.bounds_colliding:
                self.world.draw_rect(polygon.bounds, (0,0,0), 2)

    def process_collision(self):
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

    def step_through_polygons(self):
        poly_count = len(self.poly_info_list)
        step_info = self.StepInfo()

        while True:
            for i in range(poly_count):
                polygon1, dragger = self.poly_info_list[i]
                step_info.polygon1 = polygon1

                for k in range(len(polygon1.world_vertices)):
                    step_info.test_polygon = polygon1
                    step_info.test_edge1_pos1_idx = k
                    step_info.test_edge1_pos1 = polygon1.world_vertices[step_info.test_edge1_pos1_idx]
                    step_info.test_edge1_pos2_idx = (k+1)%len(polygon1.world_vertices)
                    step_info.test_edge1_pos2 = polygon1.world_vertices[step_info.test_edge1_pos2_idx]
                    yield step_info

    def process_collision_step(self, deltaTime: float):
        self.coll_step_time += deltaTime
        if self.coll_step_time > self.coll_step_time_max:
            self.coll_step_time = 0.0
            self.step_info = next(self.coll_stepper)

        test_polygon = self.step_info.test_polygon
        if test_polygon != None:
            edge1_pos1 = test_polygon.world_vertices[self.step_info.test_edge1_pos1_idx]
            edge1_pos2 = test_polygon.world_vertices[self.step_info.test_edge1_pos2_idx]
            line = edge1_pos2 - edge1_pos1

            # Draw edge line that's being tested.
            self.world.draw_line(edge1_pos1, edge1_pos2, 4, RenderUtil.WHITE)
            self.world.draw_point(edge1_pos1, 8, RenderUtil.WHITE)
            self.world.draw_point(edge1_pos2, 8, RenderUtil.WHITE)

            # Draw perpendicular line.
            perp = line.perpendicular()
            perp_norm = perp.normalize()
            screen_size = self.world.game.screen.get_size()
            perp_line_start = perp * -1000
            perp_line_end = perp * 1000
            self.world.draw_line(perp_line_start, perp_line_end, 1, RenderUtil.GRAY)

            # Draw projected polygons on the perpendicular line.
            poly_count = len(self.poly_info_list)
            for i in range(poly_count):
                for j in range(i+1, poly_count):
                    polygon1, dragger = self.poly_info_list[i]
                    polygon2, dragger = self.poly_info_list[j]

                    min1, max1 = CollisionUtil.project_polygon_onto_axis(polygon1.world_vertices, perp_norm)
                    min2, max2 = CollisionUtil.project_polygon_onto_axis(polygon2.world_vertices, perp_norm)

                    poly1_proj_min = perp_norm * min1
                    poly1_proj_max = perp_norm * max1
                    self.world.draw_line(poly1_proj_min, poly1_proj_max, 4, RenderUtil.CYAN)

                    poly2_proj_min = perp_norm * min2
                    poly2_proj_max = perp_norm * max2
                    self.world.draw_line(poly2_proj_min, poly2_proj_max, 4, RenderUtil.CYAN)


