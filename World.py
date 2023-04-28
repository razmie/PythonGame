import pygame
import Game
import json
from Camera import Camera
from Nodes.NodeBase import NodeBase
from Nodes.PointNode import PointNode
from Nodes.LineNode import LineNode

class World:
    game: Game = None
    camera: Camera = None

    nodes: NodeBase = []

    def __init__(self, new_game: Game):
        self.game = new_game
        self.camera = Camera(self)

        self.load_point_from_json('world.json')

    def update(self, deltaTime: float):
        self.camera.update(deltaTime)

        for node in self.nodes:
            node.update(deltaTime)
            node.draw()

    def load_point_from_json(self, file_path):
        self.nodes.clear()

        with open(file_path, 'r') as file:
            json_data = json.load(file)

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

