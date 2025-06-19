from worldmap.display.tile_manager import TileManager

class HexGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for x in range(width)] for y in range(height)]
        self.tile_manager = TileManager()

    def get_hex_position(self, row, col):
        # Convert grid coordinates to screen coordinates
        x = col * self.tile_manager.hex_width * 0.75
        y = row * self.tile_manager.hex_vert_offset
        # Offset every other row
        if row % 2:
            x += self.tile_manager.hex_width * 0.375
        return x, y

    def get_grid_coordinates(self, screen_x, screen_y):
        # Convert screen coordinates to grid coordinates
        row = int(screen_y / self.tile_manager.hex_vert_offset)
        col = int(screen_x / (self.tile_manager.hex_width * 0.75))
        # Adjust for offset rows
        if row % 2:
            col = int((screen_x - self.tile_manager.hex_width * 0.375) / 
                     (self.tile_manager.hex_width * 0.75))
        return row, col

    def set_tile(self, row, col, tile_data):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = tile_data

    def get_tile(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None