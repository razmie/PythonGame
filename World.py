import pygame
import Game
import json
from Camera import Camera
from Actors.PointActor import PointActor
from Actors.LineActor import LineActor

class World:
    game: Game = None
    camera: Camera = None

    point_actors = []
    line_actors = []

    def __init__(self, new_game: Game):
        self.game = new_game
        self.camera = Camera(new_game)

        self.load_point_from_json('world.json')

    def update(self, deltaTime: float):
        self.camera.update(deltaTime)

        for point_actor in self.point_actors:
            point_actor.update(deltaTime)
            point_actor.draw()

        for line_actor in self.line_actors:
            line_actor.update(deltaTime)
            line_actor.draw()

    def load_point_from_json(self, file_path):
        self.point_actors.clear()

        with open(file_path, 'r') as file:
            json_data = json.load(file)

            for data in json_data['point_actors']:
                position = data['position']
                size = data['size']
                color = data['color']
                point_actor = PointActor(self, position, size, color)
                self.point_actors.append(point_actor)

            for data in json_data['line_actors']:
                start_position = data['start_position']
                end_position = data['end_position']
                width = data['width']
                color = data['color']
                line_actor = LineActor(self, start_position, end_position, width, color)
                self.line_actors.append(line_actor)

