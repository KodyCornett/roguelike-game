import pygame
import os
from worldmap.display.tile_manager import TileManager

def test_tile_size():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Tile Size Test")
    
    tile_manager = TileManager()
    
    # Get a single tile to check its dimensions
    test_tile = tile_manager.get_tile('Desert', 'Ground')
    
    # Print the actual dimensions
    print(f"Tile dimensions:")
    print(f"Width: {test_tile.get_width()}")
    print(f"Height: {test_tile.get_height()}")
    print(f"Expected dimensions:")
    print(f"Width: {tile_manager.hex_width}")
    print(f"Height: {tile_manager.hex_height}")
    
    # Display single tile
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        screen.fill((50, 50, 50))
        screen.blit(test_tile, (100, 100))
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    test_tile_size()