import pygame
import Level
import Game
import json
import os
import importlib
import inspect
import os
from Camera import Camera
from WorldAssets import WorldAssets
from WorldScript import ScriptBase
from Nodes.NodeBase import NodeBase
from Nodes.PointNode import PointNode
from Nodes.LineNode import LineNode

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

        self.load_point_from_json(world_file_path)

        for script_path in self.script_paths:
            self.execute_script(script_path)

    def click(self):
        print("click")

    def update(self, deltaTime: float):
        self.camera.update(deltaTime)

        for node in self.nodes:
            node.handle_events()
            node.update(deltaTime)
            node.draw(self.game.screen)

    def load_point_from_json(self, file_path: str):
        if file_path is None:
            return
        if os.path.exists(file_path) == False:
            return
        
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

    def execute_script(self, script_path):
        # Import the module from the script file
        module_spec = importlib.util.spec_from_file_location('my_module', script_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        # Get the class from the module that inherits from ParentClass
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, ScriptBase):
                FoundScriptClass = obj
                break

        # Create an object from the MyClass class
        my_object = FoundScriptClass(self)
