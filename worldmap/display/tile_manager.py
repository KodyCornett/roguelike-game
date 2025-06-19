import os
import pygame

class TileManager:
    def __init__(self):
        self.hex_width = 70  # Keep width as is
        self.hex_height = 80  # Keep height as is
        # For pointy-top hexes, horizontal offset should be width * 0.75
        self.hex_horiz_offset = self.hex_width * 0.75
        # Vertical offset for pointy-top hexes
        self.hex_vert_offset = self.hex_height
        
        self.biome_terrain_mapping = {
            'Desert': ['Ground', 'Hills', 'Forest', 'Ruins', 'Lakes'],
            'Tundra': ['Ground', 'Hills', 'Forest', 'Lakes', 'Ruins'],
            'Scorched': ['Ground', 'Mountain', 'Ruins', 'Forest', 'Lakes', 'Hills'],
            'Grassland': ['Ground', 'Hills', 'Forest', 'Lakes', 'Ruins', 'Mountain'],
            'Wasteland': ['Ground', 'Hills', 'Ruins', 'Forest', 'Lakes', 'Mountain'],
            'Ocean': ['Ocean']
        }
        
        self.biome_types = ['Desert', 'Tundra', 'Scorched', 'Grassland', 'Wasteland', 'Ocean']
        self.terrain_types = ['Ground', 'Hills', 'Lakes', 'Forest', 'Ruins', 'Mountain', 'Ocean']
        
        self.tiles = {}
        self._tiles_loaded = False
        self.load_tiles()

    def load_tiles(self):
        if self._tiles_loaded:
            return
        
        base_path = os.path.join('assets', 'MapTiles', 'PNG')
        if not os.path.exists(base_path):
            print(f"Error: Base path not found: {base_path}")
            return

        print(f"Loading tiles from: {base_path}")
        
        # Initialize tiles dictionary
        for biome in self.biome_types:
            self.tiles[biome] = {}
            biome_path = os.path.join(base_path, biome)
            
            if not os.path.exists(biome_path):
                print(f"Biome path not found: {biome_path}")
                continue

            # Handle Ocean biome specially
            if biome == 'Ocean':
                if os.path.exists(biome_path):
                    ocean_files = [f for f in os.listdir(biome_path) if f.lower().endswith('.png')]
                    if ocean_files:
                        try:
                            ocean_image = pygame.image.load(os.path.join(biome_path, ocean_files[0]))
                            self.tiles['Ocean']['Ocean'] = pygame.transform.scale(
                                ocean_image, (self.hex_width, self.hex_height)
                            )
                            print(f"Successfully loaded Ocean tile")
                        except pygame.error as e:
                            print(f"Failed to load Ocean tile: {e}")
                continue

            # Load other biome tiles
            for terrain in self.biome_terrain_mapping[biome]:
                terrain_path = os.path.join(biome_path, terrain)
                if not os.path.exists(terrain_path):
                    print(f"Terrain path not found: {terrain_path}")
                    continue

                # Load all tile variants
                png_files = sorted([f for f in os.listdir(terrain_path) if f.lower().endswith('.png')])
                if not png_files:
                    print(f"No PNG files found in: {terrain_path}")
                    continue

                print(f"\nLoading {biome}/{terrain} variants:")
                print(f"Found files: {png_files}")
                
                # Initialize list for this terrain type
                self.tiles[biome][terrain] = []

                # Load all tile variants
                for png_file in png_files:
                    full_path = os.path.join(terrain_path, png_file)
                    try:
                        print(f"Loading variant: {png_file}")
                        image = pygame.image.load(full_path)
                        scaled_image = pygame.transform.scale(image, (self.hex_width, self.hex_height))
                        self.tiles[biome][terrain].append(scaled_image)
                        print(f"Successfully loaded variant: {png_file}")
                    except pygame.error as e:
                        print(f"Failed to load {png_file}: {e}")

                # Keep the list for multiple variants, only convert to single tile if exactly one variant
                if len(self.tiles[biome][terrain]) == 1:
                    print(f"Single variant found for {biome}/{terrain}, converting to direct reference")
                    self.tiles[biome][terrain] = self.tiles[biome][terrain][0]
                else:
                    variant_count = len(self.tiles[biome][terrain])
                    print(f"Multiple variants ({variant_count}) found for {biome}/{terrain}")
                    if variant_count > 0:
                        print(f"First variant type: {type(self.tiles[biome][terrain][0])}")

        self._tiles_loaded = True
        print("\nLoaded biomes:", list(self.tiles.keys()))
        for biome in self.tiles:
            print(f"Terrains for {biome}:", list(self.tiles[biome].keys()))

    def get_tile(self, biome: str, terrain: str) -> pygame.Surface:
        """Get a tile image for the given biome and terrain combination."""
        # Map numeric or unknown biomes/terrains to their string representations
        biome_str = str(biome)
        terrain_str = str(terrain)
        
        # Handle numeric biomes
        biome_mapping = {
            '0': 'Ocean',
            '1': 'Desert',
            '2': 'Scorched',
            '3': 'Grassland',
            '4': 'Tundra',
            '5': 'Wasteland'
        }
        
        # Handle numeric terrains
        terrain_mapping = {
            '0': 'Ocean',
            '1': 'Ground',
            '2': 'Hills',
            '3': 'Mountain',
            '4': 'Forest',
            '5': 'Lakes',
            '6': 'Ruins'
        }
        
        # Convert numeric values to string names
        biome_str = biome_mapping.get(biome_str, biome_str)
        terrain_str = terrain_mapping.get(terrain_str, terrain_str)
        
        # Handle Ocean tiles specially
        if terrain_str == 'Ocean' or biome_str == 'Ocean':
            return self.tiles.get('Ocean', {}).get('Ocean') or self._create_fallback_tile('Ocean', 'Ocean')
        
        # Try to get the tile from loaded tiles
        tile = self.tiles.get(biome_str, {}).get(terrain_str)
        if tile is not None:
            if isinstance(tile, list):
                import random
                return random.choice(tile)  # Random selection will now happen only once per position
            return tile
        
        # Return fallback tile if no valid tile is found
        return self._create_fallback_tile(biome_str, terrain_str)

    def _create_fallback_tile(self, biome: str, terrain: str) -> pygame.Surface:
        """Create a basic colored tile when the actual tile image is not available."""
        # Define base colors for biomes
        biome_colors = {
            'Desert': (238, 214, 175),    # Sandy yellow
            'Tundra': (220, 220, 220),    # Light gray
            'Scorched': (139, 69, 19),    # Brown
            'Grassland': (34, 139, 34),   # Forest green
            'Wasteland': (169, 169, 169), # Gray
            'Ocean': (0, 105, 148)        # Blue
        }
        
        # Define modifiers for different terrain types
        terrain_modifiers = {
            'Ground': 1.0,
            'Hills': 0.8,    # Slightly darker
            'Lakes': 0.6,    # Much darker
            'Forest': 0.7,   # Darker
            'Ruins': 0.9,    # Slightly darker
            'Mountain': 0.5, # Very dark
            'Ocean': 0.8     # Slightly darker
        }
        
        # Create transparent surface
        surface = pygame.Surface((self.hex_width, self.hex_height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparent background
        
        # Get base color and modifier
        base_color = biome_colors.get(biome, (128, 128, 128))  # Gray as default
        modifier = terrain_modifiers.get(terrain, 1.0)
        
        # Calculate final color
        final_color = tuple(int(c * modifier) for c in base_color)
        
        # Draw hexagon
        points = [
            (self.hex_width//2, 0),                # Top
            (self.hex_width, self.hex_height//4),   # Upper right
            (self.hex_width, self.hex_height*3//4), # Lower right
            (self.hex_width//2, self.hex_height),   # Bottom
            (0, self.hex_height*3//4),             # Lower left
            (0, self.hex_height//4)                # Upper left
        ]
        
        # Fill and outline
        pygame.draw.polygon(surface, final_color, points)
        pygame.draw.polygon(surface, (50, 50, 50), points, 1)  # Dark outline
        
        return surface