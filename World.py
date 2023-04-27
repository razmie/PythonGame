import pygame
import Game
import json
from Camera import Camera
from Actors.PointActor import PointActor

class World:
    game: Game = None
    camera: Camera = None

    points = [(0, 0), (150, 200), (200, 400)]

    point_actors = []

    def __init__(self, new_game: Game):
        self.game = new_game
        self.camera = Camera(new_game)

        self.point_actor = PointActor(self)

        self.load_point_from_json('world.json')

    def update(self, deltaTime: float):
        self.camera.update(deltaTime)

        for point_actor in self.point_actors:
            point_actor.update(deltaTime)
            point_actor.draw()

    def load_point_from_json(self, file_path):
        self.point_actors.clear()

        with open(file_path, 'r') as file:
            json_data = json.load(file)

        for data in json_data:
            position = data['position']
            size = data['size']

            point_actor = PointActor(self, position, size)
            self.point_actors.append(point_actor)

