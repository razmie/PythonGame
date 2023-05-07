import Game
from World import World

class Level:
    game: Game = None
    world: World = None

    def __init__(self, new_game: Game, world_file_path: str = None):
        self.game = new_game
        self.world = World(self, world_file_path)

    def update(self, delta_time: float):
        self.world.update(delta_time)
