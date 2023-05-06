import pygame, pygame.gfxdraw
import os, importlib, inspect, json
import Game, Level
from Maths import Maths, Rect
from Camera import Camera
from WorldAssets import WorldAssets
from ScriptBase import ScriptBase
from Nodes.NodeBase import NodeBase

class World:
    game: Game = None
    level: Level = None

    def __init__(self, level: Game, world_file_path: str = None):
        self.level = level
        self.game = self.level.game
        self.camera = Camera(self)

        self.assets = WorldAssets()

        self.nodes: NodeBase = []

        self.script_paths: list = []
        self.scripts: ScriptBase = []

        self.load_point_from_json(world_file_path)

        for script_path in self.script_paths:
            script = self.execute_script(script_path)
            self.scripts.append(script)

    def update(self, deltaTime: float):
        self.camera.update(deltaTime)

        for node in self.nodes:
            node.handle_events()
            node.update(deltaTime)
            if node.can_draw:
                node.draw(self.game.screen)

        for script in self.scripts:
            script.handle_events()
            script.update(deltaTime)
            script.draw(self.game.screen)

    def load_point_from_json(self, file_path: str):
        if file_path is None:
            return
        assert os.path.exists(file_path)
        
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        for font_data in json_data['fonts']:
            font_id = font_data["font_id"]
            font_name = font_data["font_name"]
            font_size = font_data["font_size"]

            self.assets.add_font_asset(font_id, font_name, font_size)

        script_names = json_data['script_names']
        self.get_script_paths_from_names(file_path, script_names)

        for node_data in json_data['nodes']:
            self.load_node(node_data, None)

    def load_node(self, node_data, parent_node):
        type_name = node_data['type']
        node_class = globals()[type_name]
        node = node_class(self)
        node.parent_node = parent_node
        if node is not None:
            node.load(node_data)
            self.nodes.append(node)

        child_node_list = node_data.get("child_nodes")
        if child_node_list is not None:
            for child_node in child_node_list:
                self.load_node(child_node, node)

    def get_script_paths_from_names(self, file_path: str, names: list):
        dir_path = os.path.dirname(file_path)

        for name in names:
            script_path = os.path.join(dir_path, name).replace("\\","/")
            self.script_paths.append(script_path)

    def execute_script(self, script_path) -> ScriptBase:
        # Import the module from the script file
        module_spec = importlib.util.spec_from_file_location('my_module', script_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        FoundScriptClass = None

        # Get the class from the module that inherits from ParentClass
        for name, obj in inspect.getmembers(module):
            if name != "ScriptBase" and inspect.isclass(obj) and issubclass(obj, ScriptBase):
                FoundScriptClass = obj
                break

        # Create an object from the MyClass class
        script_object = FoundScriptClass(self)
        return script_object
    
    def draw_point(self, position, size: int, color: pygame.color):
        screen_pos = self.camera.world_to_screen(position)
        screen_size = self.camera.world_to_screen_size(size)

        # Draw circle on seperate surface to fix bug with draw circle.
        circle_surface = pygame.Surface((screen_size*2, screen_size*2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, color, (screen_size, screen_size), screen_size)

        self.game.screen.blit(circle_surface, (screen_pos.x - screen_size, screen_pos.y - screen_size))

    def draw_line(self, start_position, end_position, width: int, color: pygame.color):
        screen_start = self.camera.world_to_screen(start_position)
        screen_end = self.camera.world_to_screen(end_position)
        screen_width = int(self.camera.world_to_screen_size(width))
        screen_width = max(screen_width, 1)

        pygame.draw.line(self.game.screen, color, screen_start, screen_end, screen_width)

    def draw_rect(self, rect: Rect, color: pygame.color, line_width: int = 0):
        pos = self.camera.world_to_screen(rect.position)
        width = self.camera.world_to_screen_size(rect.size.x)
        height = self.camera.world_to_screen_size(rect.size.y)

        pygame.draw.rect(self.game.screen, color, ((pos.x, pos.y), (width, height)), line_width)

    def draw_polygon(self, vertices, color: pygame.color):
        if len(vertices) <= 2:
            return
        
        screen_vertices = []
        for vertex in vertices:
            screen_vertices.append(self.camera.world_to_screen(vertex))

        if len(vertices) > 2:
            pygame.gfxdraw.filled_polygon(self.game.screen, Maths.get_vertices(screen_vertices), color)
