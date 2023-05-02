from ScriptBase import ScriptBase
import pygame
import numpy as np
import World
from Nodes.Physics.PhysicsManager import PhysicsManager
from Nodes.Physics.PolygonPhsxBody import PolygonPhsxBody

class PhysicsTest(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)

        phy_node = PolygonPhsxBody(world)
        vertices = [
            [0,0],
            [100,0],
            [100,100],
            [0,100]
        ]
        phy_node.set(np.array([0,-300]), vertices, (0,0), (0,0,255))        
        phy_node.mass = 5
        self.world.nodes.append(phy_node)

        ground = PolygonPhsxBody(world)
        vertices = [
            [-400,-50],
            [400,-50],
            [400,50],
            [-400,50]
        ]
        ground.set(np.array([0,250]), vertices, (0,0), (0,0,0))        
        ground.mass = np.inf
        self.world.nodes.append(ground)

        physics_manger = PhysicsManager(world)
        self.world.nodes.append(physics_manger)

    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.load_level("Assets/Levels/Frontend/Frontend.json")


    

