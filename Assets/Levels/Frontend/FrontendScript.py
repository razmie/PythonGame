from WorldScript import WorldScript
from World import World

class FrontendScript(WorldScript):
    def __init__(self, world: World):
        super().__init__(world)
        print("Test")
