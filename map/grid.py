import pygame
from settings import GRAY

class Grid:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, GRAY, rect)