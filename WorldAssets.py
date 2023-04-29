import World
import pygame

class FontAsset:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.font = pygame.font.Font(name, size)

class WorldAssets:
    fonts: list = {}

    def __init__(self):
        pass

    def add_font_asset(self, font_id: str, name: str, size: int):
        font_asset = FontAsset(name, size)
        self.fonts[font_id] = font_asset

    def get_font_asset(self, font_id: str) -> FontAsset:
        return self.fonts[font_id]
