import pygame
import sys
import numpy as np
from worldmap.generators.world_gen import WorldGenerator
from worldmap.display.world_renderer import WorldRenderer
from settings import *
from menu import Menu, WHITE, BLACK, GRAY
from title_screen import TitleScreen
from worldmap.grid import HexGrid
from worldmap.display.tile_manager import TileManager


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lost in the Lift")
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.menu = Menu(screen)
        self.title_screen = TitleScreen(screen)
        self.current_state = 'menu'
        self.world_state = None
        self.selected_ship_name = None

    def run(self):
        while True:
            if self.current_state == 'menu':
                selected_option = self.menu.run()
                if selected_option == "Start":
                    self.current_state = 'title'
                elif selected_option == "Quit":
                    pygame.quit()
                    sys.exit()
            elif self.current_state == 'title':
                self.selected_ship_name = self.title_screen.run()  # Store the returned ship name
                if self.selected_ship_name:  # Only proceed if a ship name was returned
                    self.current_state = 'game'
                    self.world_state = WorldMapState()
            elif self.current_state == 'game':
                self.run_game()

    def run_game(self):
        while self.current_state == 'game':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_state = 'menu'
                        return
                    self.world_state.handle_event(event)
            
            self.world_state.update()
            self.screen.fill(GRAY)
            self.world_state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

class WorldMapState:
    def __init__(self):
        map_width = 100
        map_height = 80
        self.world_generator = WorldGenerator(width=map_width, height=map_height)
        self.world_renderer = WorldRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.hex_grid = HexGrid(map_width, map_height)
        self.tile_manager = TileManager()
        self.world_data = None
        self.display_mode = 'terrain'
        self.camera_x = 0
        self.camera_y = 0
        self.tile_variants = {}
        self.camera_speed = 10
        
        # Initialize the mappings
        self.biome_mapping = {
            'Desert': 'Desert',
            'Tundra': 'Tundra',
            'Scorched': 'Scorched',
            'Grassland': 'Grassland',
            'Wasteland': 'Wasteland'
        }
        
        self.terrain_mapping = {
            'Ground': 'Ground',
            'Hills': 'Hills',
            'Lakes': 'Lakes',
            'Forest': 'Forest',
            'Ruins': 'Ruins',
            'Mountain': 'Mountain',
            'Ocean': 'Ocean'
        }
        
        self.generate_new_world()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.display_mode = 'biome' if self.display_mode == 'terrain' else 'terrain'
            elif event.key == pygame.K_r:
                self.generate_new_world()

    def update(self):
        # Get all currently pressed keys
        keys = pygame.key.get_pressed()
        
        # Store old camera position to check if we need to redraw
        old_camera = (self.camera_x, self.camera_y)
        
        # Handle camera movement
        if keys[pygame.K_LEFT]:
            self.camera_x += self.camera_speed
        if keys[pygame.K_RIGHT]:
            self.camera_x -= self.camera_speed
        if keys[pygame.K_UP]:
            self.camera_y += self.camera_speed
        if keys[pygame.K_DOWN]:
            self.camera_y -= self.camera_speed

    def generate_new_world(self):
        self.tile_variants = {}
        self.world_data = self.world_generator.generate_world_map()
        for y in range(self.hex_grid.height):
            for x in range(self.hex_grid.width):
                tile_data = {
                    'terrain': self.world_data['terrain_types'][y][x],
                    'biome': self.world_data['biomes'][y][x],
                    'height': self.world_data['terrain_height'][y][x]
                }
                self.hex_grid.set_tile(y, x, tile_data)

    def get_tile_variant(self, row, col, biome, terrain):
        """Get a consistent tile variant for a given position."""
        key = (row, col, str(biome), str(terrain))
        if key in self.tile_variants:
            return self.tile_variants[key]
        
        try:
            tile = self.tile_manager.get_tile(biome, terrain)
            self.tile_variants[key] = tile
            return tile
        except Exception as e:
            print(f"Error getting tile variant: {e}")
            return None

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Clear screen with black
        
        # Get tile dimensions
        hex_width = self.hex_grid.tile_manager.hex_width
        hex_height = self.hex_grid.tile_manager.hex_height
        hex_vert_offset = int(self.hex_grid.tile_manager.hex_vert_offset)
        
        # Add an initial offset to adjust the starting position of the entire map
        initial_x_offset = 90  # Adjust this value to move the entire map right/left
        initial_y_offset = 20   # Adjust this value to move the entire map up/down
        
        # Calculate visible area
        visible_width = (SCREEN_WIDTH // hex_width) + 4
        visible_height = (SCREEN_HEIGHT // hex_vert_offset) + 4
        
        # Calculate starting position
        start_row = max(0, -self.camera_y // hex_vert_offset)
        start_col = max(0, -self.camera_x // hex_width)
        
        # Calculate end positions
        end_row = min(self.hex_grid.height, start_row + visible_height + 4)
        end_col = min(self.hex_grid.width, start_col + visible_width + 4)
        
        # Draw visible tiles
        for row in range(int(start_row), int(end_row)):
            for col in range(int(start_col), int(end_col)):
                x, y = self.hex_grid.get_hex_position(row, col)
                x += self.camera_x + initial_x_offset  # Add initial offset to x
                y += self.camera_y + initial_y_offset  # Add initial offset to y
                
                # Only draw if the tile would be visible
                if (-hex_width <= x <= SCREEN_WIDTH and 
                    -hex_height <= y <= SCREEN_HEIGHT):
                    tile = self.hex_grid.get_tile(row, col)
                    if tile:
                        tile_image = self.get_tile_variant(row, col, tile['biome'], tile['terrain'])
                        if tile_image:
                            screen.blit(tile_image, (x, y))
                            
                            # Draw border
                            points = [
                                (x + hex_width//2, y),              # Top
                                (x + hex_width, y + hex_height//4), # Upper right
                                (x + hex_width, y + hex_height*3//4), # Lower right
                                (x + hex_width//2, y + hex_height),   # Bottom
                                (x, y + hex_height*3//4),           # Lower left
                                (x, y + hex_height//4)              # Upper left
                            ]
                            pygame.draw.polygon(screen, (100, 100, 100), points, 1)

if __name__ == '__main__':
    game = Game()
    game.run()