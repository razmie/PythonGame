from ScriptBase import ScriptBase
import pygame
import World
from Input import Input
from Maths import Vector2
from Nodes.NodeBase import NodeBase
from Nodes.PolygonNode import PolygonNode
from CollisionUtil import CollisionUtil
from RenderUtil import RenderUtil
from Maths import Vector2
from GTK import GTK

class PolyDragger(NodeBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.hovering = False
        self.dragging = False
        self.bounds_colliding = False
        self.colliding = False
        self.click_offset = Vector2(0,0)

class PhysicsTest(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.world.camera.position = Vector2(0,0)
        self.mouse_down = False

        self.polygon1 = PolygonNode(world)
        vertices = [
            Vector2(0,0),
            Vector2(100,0),
            Vector2(100,100),
            Vector2(0,100)
        ]
        self.polygon1.set(Vector2(-200,-200), vertices, Vector2(0.5,0.5), RenderUtil.GREEN)
        self.world.nodes.append(self.polygon1)

        self.polyDragger1 = PolyDragger(world)
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


    

