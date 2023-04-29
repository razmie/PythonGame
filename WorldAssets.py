import World
import pygame

class FontAsset:
    def __init__(self, font_name: str, font_size: int):
        self.font_name = font_name
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, font_size)

class WorldAssets:
    fonts: list = {}

    def __init__(self):
        pass

    def add_font_asset(self, font_id: str, font_name: str, font_size: int):
        font_asset = FontAsset(font_name, font_size)
        self.fonts[font_id] = font_asset

    def get_font_asset(self, font_id: str) -> FontAsset:
        return self.fonts[font_id]
