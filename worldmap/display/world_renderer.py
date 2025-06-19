import pygame
import numpy as np
from worldmap.display.tile_manager import TileManager

class WorldRenderer:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_manager = TileManager()
        
        # Get hex dimensions from tile manager
        self.hex_width = self.tile_manager.hex_width
        self.hex_height = self.tile_manager.hex_height
        
        # Calculate offsets
        self.horizontal_spacing = self.hex_width
        self.vertical_spacing = int(self.hex_height * 0.75)  # 3/4 of height

    def get_hex_position(self, row: int, col: int) -> tuple[float, float]:
        """Calculate the pixel position of a hexagonal tile."""
        x = col * self.tile_manager.hex_horiz_offset
        y = row * self.tile_manager.hex_vert_offset
        
        if row % 2:
            x += self.tile_manager.hex_horiz_offset / 2
        
        return x, y

    def draw(self, screen, world_data, display_mode='terrain'):
        """Draw the world map to the screen using hexagonal tiles."""
        height, width = world_data['terrain_types'].shape
        
        # Clear the screen first
        screen.fill((0, 0, 0))  # Black background
        
        # Draw each hex tile
        for y in range(height):
            for x in range(width):
                # Get tile position
                pos_x, pos_y = self.get_hex_position(y, x)
                
                # Get the appropriate tile based on terrain and biome
                biome = world_data['biomes'][y, x]
                terrain = world_data['terrain_types'][y, x]
                
                # Get the tile from tile manager
                tile = self.tile_manager.get_tile(biome, terrain)
                if tile:
                    # Create a rect for positioning
                    tile_rect = tile.get_rect()
                    tile_rect.topleft = (pos_x, pos_y)
                    
                    # Draw the tile
                    screen.blit(tile, tile_rect)

    # Remove or comment out the create_surface method if you're not using it anymore