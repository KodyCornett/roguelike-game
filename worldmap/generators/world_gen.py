from opensimplex import OpenSimplex
import numpy as np
from typing import Dict, Any, List, Tuple
from .biome_rules import BiomeRules

class WorldGenerator:
    def __init__(self, width: int, height: int, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else np.random.randint(0, 99999)
        self.noise_gen = OpenSimplex(seed=self.seed)
        self.biome_rules = BiomeRules()

    def get_neighbors(self, y: int, x: int, grid: np.ndarray) -> List[Tuple[int, int, Any]]:
        """Get valid neighboring cells with their coordinates."""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    # Handle both numpy arrays and object arrays
                    value = grid[ny][nx] if isinstance(grid[ny][nx], (str, type(None))) else grid[ny][nx].item()
                    neighbors.append((ny, nx, value))
        return neighbors

    def generate_biome_map(self, elevation: np.ndarray, temperature: np.ndarray, moisture: np.ndarray) -> np.ndarray:
        """Generate improved biome map ensuring all biomes are present."""
        biome_map = np.full((self.height, self.width), '', dtype=object)
        
        # Define core regions for each biome type with more distinct boundaries
        biome_cores = {
            'Desert': {
                'temp_min': 0.7,
                'moist_max': 0.3,
                'elev_range': (0.2, 0.5)
            },
            'Tundra': {
                'temp_max': 0.25,  # Reduced from 0.3 to make tundra more rare
                'moist_range': (0.4, 0.7),
                'elev_range': (0.4, 0.8),
                'y_max': self.height // 4  # Restrict to top quarter of map
            },
            'Grassland': {
                'temp_range': (0.4, 0.6),
                'moist_range': (0.4, 0.7),
                'elev_range': (0.3, 0.5)
            },
            'Ocean': {
                'elev_max': 0.2
            }
        }
        
        # First pass: Place Ocean
        for y in range(self.height):
            for x in range(self.width):
                if elevation[y, x] < biome_cores['Ocean']['elev_max']:
                    biome_map[y, x] = 'Ocean'
                    continue
        
        # Second pass: Place core biomes with stricter rules
        for biome, conditions in biome_cores.items():
            if biome == 'Ocean':
                continue
                
            for y in range(self.height):
                # Skip if outside of y_max for Tundra
                if biome == 'Tundra' and y > conditions['y_max']:
                    continue
                    
                for x in range(self.width):
                    if biome_map[y, x]:  # Skip if already assigned
                        continue
                    
                    # Check conditions for each biome with more precise ranges
                    matches = True
                    if 'temp_min' in conditions and temperature[y, x] < conditions['temp_min']:
                        matches = False
                    if 'temp_max' in conditions and temperature[y, x] > conditions['temp_max']:
                        matches = False
                    if 'temp_range' in conditions and not (conditions['temp_range'][0] <= temperature[y, x] <= conditions['temp_range'][1]):
                        matches = False
                    if 'moist_range' in conditions and not (conditions['moist_range'][0] <= moisture[y, x] <= conditions['moist_range'][1]):
                        matches = False
                    if 'moist_max' in conditions and moisture[y, x] > conditions['moist_max']:
                        matches = False
                    if 'elev_range' in conditions and not (conditions['elev_range'][0] <= elevation[y, x] <= conditions['elev_range'][1]):
                        matches = False
                    
                    if matches:
                        biome_map[y, x] = biome

        # Fill remaining spaces based on temperature and moisture
        for y in range(self.height):
            for x in range(self.width):
                if not biome_map[y, x]:
                    # Use temperature and moisture to determine the best biome
                    if temperature[y, x] > 0.7:
                        biome_map[y, x] = 'Desert'
                    elif temperature[y, x] < 0.25 and y <= self.height // 4:  # Only in top quarter
                        biome_map[y, x] = 'Tundra'
                    else:
                        biome_map[y, x] = 'Grassland'

        # Third pass: Place Ruins and create Wasteland/Scorched zones
        ruin_positions = []
        ruins_to_place = min(5, (self.width * self.height) // 300)  # Increased number of ruins
        
        # Place ruins in different biomes
        target_biomes = ['Desert', 'Grassland', 'Tundra']
        for target_biome in target_biomes:
            if len(ruin_positions) >= ruins_to_place:
                break
                
            attempts = 0
            while attempts < 100:
                x = np.random.randint(5, self.width - 5)
                y = np.random.randint(5, self.height - 5)
                
                if (biome_map[y, x] == target_biome and
                    all(abs(rx - x) + abs(ry - y) > 15 for rx, ry in ruin_positions)):  # Reduced minimum distance
                    ruin_positions.append((x, y))
                    break
                    
                attempts += 1
        
        # Create Wasteland and Scorched areas around ruins with more variation
        for ruin_x, ruin_y in ruin_positions:
            wasteland_radius = np.random.randint(4, 7)  # Variable radius
            scorched_radius = np.random.randint(2, 4)   # Variable radius
            
            for dy in range(-wasteland_radius, wasteland_radius + 1):
                for dx in range(-wasteland_radius, wasteland_radius + 1):
                    y, x = ruin_y + dy, ruin_x + dx
                    if not (0 <= y < self.height and 0 <= x < self.width):
                        continue
                    
                    if biome_map[y, x] == 'Ocean':
                        continue
                        
                    distance = (dx ** 2 + dy ** 2) ** 0.5  # Using Euclidean distance
                    
                    # Create Scorched core with irregular edges
                    if distance <= scorched_radius:
                        if np.random.random() < 0.8 - (distance / scorched_radius) * 0.3:
                            biome_map[y, x] = 'Scorched'
                    # Create Wasteland in the outer ring with irregular edges
                    elif distance <= wasteland_radius:
                        if np.random.random() < 0.6 - (distance / wasteland_radius) * 0.3:
                            biome_map[y, x] = 'Wasteland'
        
        return biome_map

    def get_neighbors(self, y: int, x: int, grid: np.ndarray) -> List[Tuple[int, int, Any]]:
        """Get valid neighboring cells with their coordinates."""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    # Handle both numpy arrays and object arrays
                    value = grid[ny][nx] if isinstance(grid[ny][nx], (str, type(None))) else grid[ny][nx].item()
                    neighbors.append((ny, nx, value))
        return neighbors

    def generate_terrain_features(self, biome_map: np.ndarray, elevation: np.ndarray, moisture: np.ndarray) -> np.ndarray:
        """Generate terrain features with improved distribution."""
        terrain = np.full_like(biome_map, 'Ground', dtype=object)
        ruin_positions = []

        # Place oceans first
        ocean_mask = elevation < 0.15
        terrain[ocean_mask] = 'Ocean'
        biome_map[ocean_mask] = 'Ocean'
            
        # Place ruins first
        ruins_to_place = min(5, (self.width * self.height) // 300)
        attempts = 0
        max_attempts = 100
    
        while len(ruin_positions) < ruins_to_place and attempts < max_attempts:
            x = np.random.randint(5, self.width - 5)
            y = np.random.randint(5, self.height - 5)
    
            # Check if position is valid for ruins
            if (terrain[y, x] != 'Ocean' and
                all(abs(rx - x) + abs(ry - y) > 10 for rx, ry in ruin_positions)):
        
                terrain[y, x] = 'Ruins'
                ruin_positions.append((x, y))
        
                # Create Wasteland and Scorched areas around the ruin
                wasteland_radius = np.random.randint(4, 7)
                scorched_radius = np.random.randint(2, 4)
            
                for dy in range(-wasteland_radius, wasteland_radius + 1):
                    for dx in range(-wasteland_radius, wasteland_radius + 1):
                        ny, nx = y + dy, x + dx
                        if not (0 <= ny < self.height and 0 <= nx < self.width):
                            continue
                    
                        if terrain[ny, nx] == 'Ocean':
                            continue
                        
                        distance = ((dx ** 2 + dy ** 2) ** 0.5)
                    
                        # Create Scorched core
                        if distance <= scorched_radius:
                            if np.random.random() < 0.8:
                                biome_map[ny, nx] = 'Scorched'
                                if np.random.random() < 0.2:
                                    terrain[ny, nx] = 'Ruins'
                        # Create Wasteland in outer ring
                        elif distance <= wasteland_radius:
                            if np.random.random() < 0.7:
                                biome_map[ny, nx] = 'Wasteland'
                                if np.random.random() < 0.1:
                                    terrain[ny, nx] = 'Ruins'
            attempts += 1

        # Generate other terrain features
        for y in range(self.height):
            for x in range(self.width):
                if terrain[y, x] in ['Ocean', 'Ruins']:
                    continue

                biome = biome_map[y, x]
                elev = elevation[y, x]
                moist = moisture[y, x]

                try:
                    valid_terrains = self.biome_rules.get_valid_terrain_types(biome)
                except (AttributeError, KeyError):
                    # Fallback to default terrain if rules are missing
                    continue

                # Apply terrain features based on rules
                for feature in ['Mountain', 'Forest', 'Hills', 'Lakes']:
                    if feature not in valid_terrains:
                        continue
                    
                    try:
                        rules = self.biome_rules.terrain_rules.get(feature, {})
                        if not rules:
                            continue
                        
                        base_chance = rules.get('base_chance', 0.0)
                        
                        if ('valid_biomes' in rules and 
                            biome not in rules['valid_biomes']):
                            continue

                        # Apply requirements
                        if (rules.get('elevation_min', -1) > elev or
                            rules.get('moisture_min', -1) > moist):
                            continue

                        # Apply clustering
                        if 'cluster_chance' in rules:
                            neighbors = self.get_neighbors(y, x, terrain)
                            if any(n[2] == feature for n in neighbors):
                                base_chance = max(base_chance, rules['cluster_chance'])

                        if np.random.random() < base_chance:
                            terrain[y, x] = feature
                            break
                    except Exception:
                        continue

        return terrain


    def generate_world_map(self) -> Dict[str, Any]:
        # Generate base noise maps with different scales
        elevation = self.generate_noise(scale=75.0, octaves=5)
        
        # Generate base temperature with a north-south gradient
        base_temperature = np.zeros((self.height, self.width))
        for y in range(self.height):
            # Create gradient from north (cold) to south (hot)
            gradient = y / self.height  # 0 at north, 1 at south
            base_temperature[y, :] = gradient
        
        # Add noise to temperature but maintain the gradient
        temp_noise = self.generate_noise(scale=100.0, octaves=4)
        temperature = base_temperature * 0.7 + temp_noise * 0.3  # Mix gradient and noise
        
        moisture = self.generate_noise(scale=85.0, octaves=4)
        
        # Adjust the transformations to create more variation
        temperature = np.clip(temperature * 1.2 - 0.1, 0, 1)  # Maintain temperature range
        moisture = np.clip(moisture * 1.3 - 0.15, 0, 1)      # Adjust moisture
        
        # Keep elevation as is but ensure full range
        elevation = np.clip(elevation * 1.2, 0, 1)
        
        biome_map = self.generate_biome_map(elevation, temperature, moisture)
        terrain_features = self.generate_terrain_features(biome_map, elevation, moisture)
        
        return {
            'terrain_height': elevation,
            'terrain_types': terrain_features,
            'temperature': temperature,
            'moisture': moisture,
            'biomes': biome_map
        }

    def generate_noise(self, scale: float = 100.0, octaves: int = 6, 
                      persistence: float = 0.5, frequency: float = 2.0) -> np.ndarray:
        """Generate improved noise map with multiple octaves."""
        world = np.zeros((self.height, self.width))
        max_amplitude = 0.0
        amplitude = 1.0
        
        for octave in range(octaves):
            freq = frequency ** octave
            max_amplitude += amplitude
            
            for y in range(self.height):
                for x in range(self.width):
                    world[y, x] += self.noise_gen.noise2(
                        x * freq / scale, 
                        y * freq / scale
                    ) * amplitude
            
            amplitude *= persistence  # Move inside the octave loop
        
        # Normalize considering total amplitude
        world /= max_amplitude
        
        # Ensure range is exactly 0-1
        world = (world - world.min()) / (world.max() - world.min())
        
        return world