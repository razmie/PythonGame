from ScriptBase import ScriptBase
import pygame
import World
from Maths import Vector2
from Input import Input
from Nodes.PolygonNode import PolygonNode
from CollisionUtil import CollisionUtil

class PolyPointCollisionTest(ScriptBase):
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
        self.polygon1.set(Vector2(-200,-200), vertices, Vector2(0.5,0.5), (0,0,255))
        self.world.nodes.append(self.polygon1)

        self.polygon2 = PolygonNode(world)
        vertices = [
            Vector2(0,0),
            Vector2(100,-50),
            Vector2(150,100),
            Vector2(50,150),
            Vector2(-50,100)
        ]
        self.polygon2.set(Vector2(250,-100), vertices, Vector2(0.5,0.5), (0,0,255))
        self.world.nodes.append(self.polygon2)

        self.polygon3 = PolygonNode(world)
        vertices = [
            Vector2(0,0),
            Vector2(100,-50),
            Vector2(200,0),
            Vector2(250,100),
            Vector2(220,140),
            Vector2(150,50),
            Vector2(100,20),
            Vector2(50,100),
            Vector2(-20,130),
        ]
        self.polygon3.set(Vector2(-100,100), vertices, Vector2(0.5,0.5), (0,0,255))
        self.world.nodes.append(self.polygon3)

    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.load_level("Assets/Levels/Frontend/Frontend.json")

    def update(self, deltaTime: float):
        mouse_position = Input.get_mouse_position()
        self.world_mouse_position = self.world.camera.screen_to_world(mouse_position)

        poly_info_list = [
                [self.polygon1, 1],
                [self.polygon2, -0.1],
                [self.polygon3, 3]
            ]
        self.is_inside = False

        for poly_info in poly_info_list:
            polygon = poly_info[0]
            rotation_speed = poly_info[1]

            polygon.rotation += deltaTime * rotation_speed
            polygon.reconstruct_body()

            if self.is_inside == False:
                if CollisionUtil.is_point_in_polygon(self.world_mouse_position, polygon.world_vertices):
                    self.is_inside = True

    def draw(self, surface: pygame.Surface):
        color = (255,0,0) if self.is_inside else (0,255,0)

        self.world.draw_point(self.world_mouse_position, 10, color)
