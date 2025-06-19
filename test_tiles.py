# test_tiles.py
import pygame
import sys
from worldmap.display.tile_manager import TileManager

def test_tile_loading():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tile Test")
    tile_manager = TileManager()
    
    # Test loading a few different combinations
    test_combinations = [
        ('Desert', 'Ground'),
        ('Tundra', 'Hills'),
        ('Grassland', 'Forest'),
        ('Desert', 'Mountain'),
        ('Wasteland', 'Ruins')
    ]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((50, 50, 50))  # Dark gray background
        
        # Display test tiles
        y = 50  # Starting y position
        for biome in ['Desert', 'Tundra', 'Scorched', 'Grassland', 'Wasteland']:
            x = 50
            valid_terrains = tile_manager.biome_terrain_mapping[biome]
            for terrain in valid_terrains:
                tile = tile_manager.get_tile(biome, terrain)
                screen.blit(tile, (x, y))
                x += tile_manager.hex_width + 10
            y += tile_manager.hex_height + 10
            
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_tile_loading()