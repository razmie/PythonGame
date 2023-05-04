import pygame

class FontAsset:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.font = pygame.font.Font(name, size)

class WorldAssets:
    def __init__(self):
        self.fonts: list = {}

    def add_font_asset(self, font_id: str, name: str, size: int):
        font_asset = FontAsset(name, size)
        self.fonts[font_id] = font_asset

    def get_font_asset(self, font_id: str) -> FontAsset:
        return self.fonts[font_id]
