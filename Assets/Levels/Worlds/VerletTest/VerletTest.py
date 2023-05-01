from ScriptBase import ScriptBase
import pygame
import numpy as np
import World
from Nodes.Physics.VerletManager import VerletManager
from Nodes.PointNode import PointNode
from Nodes.Physics.PointPhyNode import PointPhyNode

class VerletTest(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)

        background_node = PointNode(self.world)
        background_node.position = np.array([0, 0])
        background_node.size = 200
        background_node.color = (0,0,0)
        self.world.nodes.append(background_node)

        for i in range(0, 2):
            phy_node = PointPhyNode(world)
            phy_node.set(np.array([0,0]), 20, (255, 0, 0))
            self.world.nodes.append(phy_node)

        verlet_manger = VerletManager(world)
        self.world.nodes.append(verlet_manger)

    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.load_level("Assets/Levels/Frontend/Frontend.json")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Get the mouse position.
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_world = self.world.camera.screen_to_world(mouse_pos)

                    phy_node = PointPhyNode(self.world)
                    phy_node.set(mouse_world, 20, (255, 0, 0))
                    self.world.nodes.append(phy_node)

    

