from typing import Dict, Any, List

import numpy as np

class BiomeRules:
    def __init__(self):
        # Define valid terrain types for each biome
        self.biome_terrain_mapping = {
            'Desert': ['Ground', 'Hills', 'Forest', 'Ruins'],
            'Tundra': ['Ground', 'Hills', 'Forest', 'Lakes', 'Ruins'],
            'Scorched': ['Ground', 'Mountain', 'Ruins', 'Forest', 'Lakes', 'Hills'],
            'Grassland': ['Ground', 'Hills', 'Forest', 'Lakes', 'Ruins', 'Mountain'],
            'Wasteland': ['Ground', 'Hills', 'Ruins', 'Forest', 'Lakes', 'Mountain'],
            'Ocean': ['Ocean']
        }

        # Previous code remains the same...

        self.rules = {
            'Ocean': {
                'temperature_range': (0.0, 1.0),
                'moisture_range': (0.0, 1.0),
                'elevation_range': (0.0, 0.2),
                'terrain_weights': {'Ocean': 1.0},
                'neighbor_weights': {
                    'Ocean': 1.5,
                    'Grassland': 0.4,
                    'Desert': 0.3
                }
            },
            'Grassland': {
                'temperature_range': (0.3, 0.7),    # Narrowed range
                'moisture_range': (0.4, 0.8),       # Adjusted range
                'elevation_range': (0.2, 0.6),      # Adjusted range
                'terrain_weights': {
                    'Ground': 0.6,
                    'Forest': 0.3,
                    'Hills': 0.1
                },
                'neighbor_weights': {
                    'Grassland': 1.5,  # Reduced from 2.0
                    'Desert': 0.6,
                    'Forest': 0.4,
                    'Wasteland': 0.2
                }
            },
            'Desert': {
                'temperature_range': (0.6, 1.0),    # High temperature
                'moisture_range': (0.0, 0.3),       # Low moisture
                'elevation_range': (0.2, 0.5),      # Adjusted range
                'terrain_weights': {
                    'Ground': 0.8,
                    'Hills': 0.2
                },
                'neighbor_weights': {
                    'Desert': 1.5,     # Reduced from 2.0
                    'Grassland': 0.5,
                    'Wasteland': 0.3
                }
            },
            'Wasteland': {
                'temperature_range': (0.5, 0.8),
                'moisture_range': (0.1, 0.3),
                'elevation_range': (0.3, 0.5),
                'terrain_weights': {
                    'Ground': 0.7,
                    'Hills': 0.2,
                    'Ruins': 0.1
                },
                'neighbor_weights': {
                    'Wasteland': 1.0,
                    'Desert': 0.7,
                    'Grassland': 0.5
                }
            },
            'Scorched': {
                'temperature_range': (0.8, 1.0),
                'moisture_range': (0.0, 0.2),
                'elevation_range': (0.4, 0.6),
                'terrain_weights': {
                    'Ground': 0.7,
                    'Mountain': 0.2,
                    'Ruins': 0.1
                },
                'neighbor_weights': {
                    'Scorched': 1.0,
                    'Wasteland': 0.6,
                    'Desert': 0.4
                }
            }
        }

        # Define terrain feature rules with biome restrictions
        self.terrain_rules = {
            'Ground': {
                'base_chance': 0.6,
                'min_spacing': 0,
                'valid_biomes': ['Desert', 'Tundra', 'Scorched', 'Grassland', 'Wasteland']
            },
            'Hills': {
                'base_chance': 0.3,
                'elevation_min': 0.4,
                'min_spacing': 2,
                'cluster_chance': 0.6,
                'valid_biomes': ['Desert', 'Tundra', 'Grassland', 'Wasteland']
            },
            'Lakes': {
                'base_chance': 0.15,
                'moisture_min': 0.5,
                'min_spacing': 3,
                'valid_biomes': ['Tundra', 'Grassland']
            },
            'Forest': {
                'base_chance': 0.25,
                'moisture_min': 0.4,
                'min_spacing': 1,
                'cluster_chance': 0.5,
                'valid_biomes': ['Tundra', 'Grassland']
            },
            'Ruins': {
                'base_chance': 0.03,
                'min_spacing': 15,
                'max_count': 3,
                'valid_biomes': ['Desert', 'Scorched', 'Grassland', 'Wasteland']
            },
            'Mountain': {
                'base_chance': 0.2,
                'elevation_min': 0.7,
                'min_spacing': 2,
                'cluster_chance': 0.7,
                'valid_biomes': ['Tundra', 'Scorched']
            },
            'Ocean': {
                'base_chance': 1.0,
                'elevation_max': 0.2,
                'valid_biomes': ['Ocean']
            }
        }

    def get_possible_biomes(self, temperature: float, moisture: float, elevation: float) -> List[str]:
        """Determine possible biomes for given conditions."""
        possible_biomes = []
        
        # Special case for ocean
        if elevation < 0.2:
            return ['Ocean']
            
        for biome, rules in self.rules.items():
            if biome == 'Ocean':
                continue  # Skip Ocean in normal biome selection
                
            temp_range = rules['temperature_range']
            moist_range = rules['moisture_range']
            elev_range = rules['elevation_range']
            
            if (temp_range[0] <= temperature <= temp_range[1] and
                moist_range[0] <= moisture <= moist_range[1] and
                elev_range[0] <= elevation <= elev_range[1]):
                possible_biomes.append(biome)
        
        return possible_biomes if possible_biomes else ['Wasteland']

    def get_valid_terrain_types(self, biome: str) -> List[str]:
        """Get list of valid terrain types for a given biome."""
        return self.biome_terrain_mapping.get(biome, ['Ground'])

    def get_neighbor_weight(self, current_biome: str, neighbor_biome: str) -> float:
        """Get the weight for a neighboring biome."""
        if current_biome not in self.rules:
            return 0.1
        neighbor_weights = self.rules[current_biome]['neighbor_weights']
        return neighbor_weights.get(neighbor_biome, 0.1)

    def is_valid_terrain_for_biome(self, terrain: str, biome: str) -> bool:
        """Check if a terrain type is valid for a given biome."""
        return terrain in self.biome_terrain_mapping.get(biome, [])

    def get_terrain_weight(self, biome: str, terrain: str) -> float:
        """Get the weight for a terrain type in a specific biome."""
        if not self.is_valid_terrain_for_biome(terrain, biome):
            return 0.0
        terrain_weights = self.rules.get(biome, {}).get('terrain_weights', {})
        return terrain_weights.get(terrain, 0.1)