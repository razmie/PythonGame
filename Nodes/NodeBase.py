import numpy as np
import Game
import World

class NodeBase:
    game: Game = None
    world: World = None
    position = np.array([0, 0])

    def __init__(self, new_world: World):
        self.world = new_world
        self.game = new_world.game

    def update(self, deltaTime: float):
        pass

    def draw(self):
        pass