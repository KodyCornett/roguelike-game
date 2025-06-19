import pygame
import sys
import os

pygame.init()
FONT = pygame.font.Font(None, 40)
MENU_OPTIONS = ['Start', 'Settings', 'Quit']
# Define colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Bright yellow for hover
NORMAL_COLOR = BLACK    # Default black color
HOVER_COLOR = YELLOW    # Yellow color for hover

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.selected = 0
        self.options = MENU_OPTIONS
        self.clock = pygame.time.Clock()
        self.option_rects = []  # Store rectangles for click detection
        
        # Load the title image
        try:
            title_path = os.path.join('assets', 'UI', 'title.png')
            self.title = pygame.image.load(title_path)
            self.title_rect = self.title.get_rect(center=(self.screen.get_width() // 2, 100))
        except pygame.error as e:
            print(f"Couldn't load title image: {e}")
            self.title = None
        
        try:
            image_path = os.path.join('assets', 'UI', 'origbig.png')
            self.background = pygame.image.load(image_path)
            self.background = pygame.transform.scale(self.background,
                                                     (self.screen.get_width(),
                                                      self.screen.get_height()))
        except pygame.error as e:
            print(f"Couldn't load background image: {e}")
            self.background = None

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(WHITE)

        # Draw the title image instead of text
        if self.title:
            self.screen.blit(self.title, self.title_rect)

        total_height = len(self.options) * 60
        start_y = (self.screen.get_height() - total_height) // 2
        self.option_rects = []  # Clear previous rectangles

        # Draw menu options
        for i, option in enumerate(self.options):
            color = HOVER_COLOR if i == self.selected else NORMAL_COLOR
            text = FONT.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, start_y + i * 60))
            self.screen.blit(text, rect)
            self.option_rects.append(rect)
        
        pygame.display.flip()

    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    # Update selected option based on mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    self.selected = -1  # Reset selection
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            self.selected = i
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        clicked_option = self.handle_mouse_click(event.pos)
                        if clicked_option:
                            return clicked_option
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected]
            self.clock.tick(30)

    def handle_mouse_click(self, pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(pos):
                return self.options[i]
        return None