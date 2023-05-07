import os, pygame
import World
from ScriptBase import ScriptBase
from Input import Input
from Maths import Vector2, Maths
from Nodes.NodeBase import NodeBase
from Nodes.PolygonNode import PolygonNode
from Nodes.PolygonDragger import PolygonDragger
from CollisionUtil import CollisionUtil
from SAT import SAT
from RenderUtil import RenderUtil
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

        self.script_file_path = os.path.abspath(__file__)

        self.world.camera.position = Vector2(0,0)
        self.world.game.screen_color = RenderUtil.BLACK

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
        # vertices = [
        #     Vector2(0,0),
        #     Vector2(100,-50),
        #     Vector2(150,100),
        #     Vector2(50,150),
        #     Vector2(-50,100)
        # ]
        vertices = [
            Vector2(-50,50),
            Vector2(0,-50),
            Vector2(50,50),
        ]
        self.polygon2.rotation = 0.5
        self.polygon2.set(Vector2(250,-100), vertices, Vector2(0,0), RenderUtil.GREEN)
        self.world.nodes.append(self.polygon2)

        self.polyDragger2 = PolygonDragger(world)
        self.polyDragger2.parent_node = self.polygon2
        self.world.nodes.append(self.polyDragger2)

        self.poly_info_list = [
                [self.polygon1, self.polyDragger1],
                [self.polygon2, self.polyDragger2]
            ]
        
        # Use for stepping through the collision process
        self.show_step = True
        self.step_info = self.StepInfo()
        self.stepper = self.get_polygon_by_step()
        self.step_time = 0
        self.step_time_max = 1
        self.can_step = True

    def handle_events(self):
        super().handle_events()
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.load_level("Assets/Levels/Frontend/Frontend.json")
                elif event.key == pygame.K_SPACE:
                    self.can_step = not self.can_step
                    if self.can_step:
                        self.world.game.screen_color = RenderUtil.BLACK
                    else:
                        self.world.game.screen_color = (16,16,16)
                elif event.key == pygame.K_d:
                    self.show_step = not self.show_step
                elif event.key == pygame.K_q or event.key == pygame.K_w:
                    for poly_info in self.poly_info_list:
                        polygon, dragger = poly_info

                        if dragger.hovering:
                            rot_val = 0

                            if event.key == pygame.K_q:
                                rot_val = Maths.pi() * 0.01
                            elif event.key == pygame.K_w:
                                rot_val = -Maths.pi_2() * 0.01

                            keys = pygame.key.get_pressed()
                            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                                rot_val = rot_val * 10

                            polygon.rotation = polygon.rotation + rot_val
                            polygon.reconstruct_body()

    def update(self, delta_time: float):
        self.process_collision()

        for poly_info in self.poly_info_list:
            polygon, dragger = poly_info

            if dragger.colliding:
                polygon.color = RenderUtil.DARK_RED
            elif dragger.dragging or dragger.hovering:
                polygon.color = RenderUtil.DARK_GREEN
            else:
                if dragger.hovering:
                    polygon.color = RenderUtil.BLUE
                else:
                    polygon.color = RenderUtil.GREEN

        if self.show_step:
            self.process_collision_step(delta_time)

    def draw(self, surface: pygame.Surface):
        for poly_info in self.poly_info_list:
            polygon, dragger = poly_info

            if dragger.bounds_colliding:
                self.world.draw_rect(polygon.bounds, RenderUtil.WHITE, 2)

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

                    SATResult1 = SAT.are_polygons_intersecting(polygon1.world_vertices, polygon2.world_vertices)
                    if SATResult1.overlapping:
                        dragger1.colliding = True
                        dragger2.colliding = True

                        #self.world.draw_line(vertex, vertex + axis, 8, RenderUtil.YELLOW)
                        self.world.draw_point(SATResult1.min_vertex, 12, RenderUtil.YELLOW)
                        self.world.draw_point(SATResult1.max_vertex, 12, RenderUtil.ORANGE)
                        #self.world.draw_point(vertex + axis, 12, RenderUtil.YELLOW)

                    else:
                        dragger1.colliding = False
                        dragger2.colliding = False
                else:
                    dragger1.bounds_colliding = False
                    dragger1.colliding = False
                    dragger2.bounds_colliding = False
                    dragger2.colliding = False

    def get_polygon_by_step(self):
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
        if self.can_step:
            self.step_time += deltaTime
            if self.step_time > self.step_time_max:
                self.step_time = 0.0
                self.step_info = next(self.stepper)

        test_polygon = self.step_info.test_polygon
        if test_polygon != None:
            edge1_pos1 = test_polygon.world_vertices[self.step_info.test_edge1_pos1_idx]
            edge1_pos2 = test_polygon.world_vertices[self.step_info.test_edge1_pos2_idx]
            line = edge1_pos2 - edge1_pos1

            # Draw perpendicular line.
            perp = line.perpendicular()
            perp_norm = perp.normalize()
            screen_size = self.world.game.screen.get_size()
            perp_line_start = perp * -1000
            perp_line_end = perp * 1000
            self.world.draw_line(perp_line_start, perp_line_end, 1, RenderUtil.WHITE)

            # Draw projected polygons on the perpendicular line.
            poly_count = len(self.poly_info_list)
            for i in range(poly_count):
                for j in range(i+1, poly_count):
                    polygon1, dragger = self.poly_info_list[i]
                    polygon2, dragger = self.poly_info_list[j]

                    min1, max1, min_vert1, max_vert1 = SAT.project_polygon_onto_axis(polygon1.world_vertices, perp_norm)
                    min2, max2, min_vert2, max_vert2 = SAT.project_polygon_onto_axis(polygon2.world_vertices, perp_norm)

                    MIN_COLOR = (0,255,255) # Min is lighter colour.
                    MAX_COLOR = (0,128,128) # Max is darker colour.

                    poly1_proj_min = perp_norm * min1
                    poly1_proj_max = perp_norm * max1
                    self.world.draw_line(poly1_proj_min, poly1_proj_max, 4, (0,191,191))
                    
                    self.world.draw_line(min_vert1, poly1_proj_min, 1, (64,64,64))
                    self.world.draw_point(poly1_proj_min, 6, MIN_COLOR)
                    self.world.draw_line(max_vert1, poly1_proj_max, 1, (64,64,64))
                    self.world.draw_point(poly1_proj_max, 6, MAX_COLOR)
                    
                    poly2_proj_min = perp_norm * min2
                    poly2_proj_max = perp_norm * max2
                    self.world.draw_line(poly2_proj_min, poly2_proj_max, 4, (0,191,191))

                    self.world.draw_line(min_vert2, poly2_proj_min, 1, (64,64,64))
                    self.world.draw_point(poly2_proj_min, 6, MIN_COLOR)
                    self.world.draw_line(max_vert2, poly2_proj_max, 1, (64,64,64))
                    self.world.draw_point(poly2_proj_max, 6, MAX_COLOR)

                    self.world.draw_point(min_vert1, 6, MIN_COLOR)
                    self.world.draw_point(max_vert1, 6, MAX_COLOR)
                    self.world.draw_point(min_vert2, 6, MIN_COLOR)
                    self.world.draw_point(max_vert2, 6, MAX_COLOR)

                    overlap = min(max1, max2) - max(min1, min2)
                    #print(overlap)
                    if overlap < 0:
                        pass
                    else:
                        # Draw overlap.
                        overlap_min = max(min1, min2)
                        overlap_max = min(max1, max2)
                        overlap_proj_min = perp_norm * overlap_min
                        overlap_proj_max = perp_norm * overlap_max
                        self.world.draw_line(overlap_proj_min, overlap_proj_max, 8, RenderUtil.RED)

            # Draw edge line that's being tested.
            self.world.draw_line(edge1_pos1, edge1_pos2, 4, RenderUtil.WHITE)
            self.world.draw_point(edge1_pos1, 8, RenderUtil.WHITE)
            self.world.draw_point(edge1_pos2, 8, RenderUtil.WHITE)
