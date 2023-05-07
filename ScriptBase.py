import os, pygame
import World

class ScriptBase:
    def __init__(self, world: World):
        self.world = world
        self.level = world.level
        self.game = world.game
        self.script_file_path = None
        pass

    def handle_events(self):
        for event in self.game.cached_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:    
                    self.reload_level()

    def update(self, deltaTime: float):
        pass

    def draw(self, surface: pygame.Surface):
        pass

    def reload_level(self):
        game_path = os.path.dirname(self.script_file_path)
        base_dir, sub_dir = game_path.split("Assets\\Levels\\Worlds", 1)
        relative_path = os.path.relpath(self.script_file_path, base_dir)
        relative_path = relative_path.replace('\\', '/')
        base_path, extension = os.path.splitext(relative_path)
        relative_path = base_path + ".json"

        self.game.load_level(relative_path)