from ScriptBase import ScriptBase
import pygame
import World
from Input import Input
from Maths import Vector2
from Nodes.NodeBase import NodeBase
from Nodes.Physics.PolygonPhsxBody import PolygonPhsxBody
from RenderUtil import RenderUtil
from Maths import Vector2
from Nodes.Physics.PhysicsManager import PhysicsManager
from Nodes.Physics.PolygonPhsxDragger import PolygonPhsxDragger
from GTK import GTK

class PhysicsTest(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.world.camera.position = Vector2(0,0)
        self.mouse_down = False

        self.polygon1 = PolygonPhsxBody(world)
        vertices = [
            Vector2(0,0),
            Vector2(100,0),
            Vector2(100,100),
            Vector2(0,100)
        ]
        self.polygon1.set(Vector2(-200,0), vertices, Vector2(0.5,0.5), RenderUtil.GREEN)
        self.polygon1.apply_gravity = False
        self.world.nodes.append(self.polygon1)

        self.polygon2 = PolygonPhsxBody(world)
        vertices = [
            Vector2(0,0),
            Vector2(100,0),
            Vector2(100,100),
            Vector2(0,100)
        ]
        self.polygon2.set(Vector2(200,0), vertices, Vector2(0.5,0.5), RenderUtil.GREEN)
        self.polygon2.apply_gravity = False
        self.world.nodes.append(self.polygon2)

        # self.polyDragger1 = PolygonPhsxDragger(world)
        # self.polyDragger1.parent_node = self.polygon1
        # self.world.nodes.append(self.polyDragger1)

        physics_manger = PhysicsManager(world)
        self.world.nodes.append(physics_manger)

    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.load_frontend()

    def update(self, delta_time: float):
        super().update(delta_time)

        key_down = False
        move_direction = Vector2(0,0)
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            move_direction += Vector2(-1,0)
            key_down = True
        if keys[pygame.K_d]:
            move_direction += Vector2(1,0)
            key_down = True
        if keys[pygame.K_w]:
            move_direction += Vector2(0,-1)
            key_down = True
        if keys[pygame.K_s]:
            move_direction += Vector2(0,1)
            key_down = True

        if key_down:
            if move_direction.length() > 0:
                move_direction = move_direction.normalize()
                move = move_direction * delta_time * 1000

                self.polygon1.apply_impulse(move, True)




    

