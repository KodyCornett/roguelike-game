import pygame
from settings import TILE_SIZE

class Unit:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.has_acted = False

    def draw(self, screen):
        padding = 5
        size = TILE_SIZE - 2 * padding
        rect = pygame.Rect(self.x * TILE_SIZE + padding, self.y * TILE_SIZE + padding, size, size)
        pygame.draw.rect(screen, self.color, rect)