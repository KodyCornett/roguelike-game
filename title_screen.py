import pygame
import random
import sys
import os
from menu import WHITE, BLACK
from settings import *

class MovingShip:
    def __init__(self, screen_width, screen_height):
        try:
            ship_path = os.path.join('assets', 'UI', 'Ship.png')
            self.image = pygame.image.load(ship_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (440, 260))
        except pygame.error as e:
            print(f"Couldn't load ship image: {e}")
            self.image = pygame.Surface((100, 60))
            self.image.fill(WHITE)
            
        self.rect = self.image.get_rect()
        self.x = -self.rect.width
        self.y = screen_height // 3
        self.speed = 4
        self.screen_width = screen_width

    def update(self):
        self.x += self.speed
        if self.x > self.screen_width:
            self.x = -self.rect.width
            self.y = random.randint(50, SCREEN_HEIGHT - 150)
            
    def draw(self, screen):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        screen.blit(self.image, self.rect)

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 40)
        self.clock = pygame.time.Clock()
        
        # Load background
        try:
            bg_path = os.path.join('assets', 'UI', 'titlebg.png')
            self.background = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Couldn't load background image: {e}")
            self.background = None

        # Create moving ship
        self.ship = MovingShip(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # List of possible ship names
        self.ship_names = [
            "The Brasswarden",
            "The Astrid",
            "The Starweaver",
            "The Iron Phoenix",
            "The Crystal Maiden",
            "The Stormchaser",
            "The Quantum Dawn",
            "The Nebula's Heart",
            "The Solarwind",
            "The Celestial Rose",
            "The Driftrunner",
            "The Ashrider",
            "The Stormfury",
            "The Clockspire",
            "The Vaporspine",
            "The Driftneedle",
            "The Mist Gale",
            "The Coiljack",
            "The Rust Casket",
            "The Star Nomad",
            "The Ethereal Wing",
            "The Cosmic Destiny",
            "The Stellar Spirit",
            "The Nova's Promise",
            "The Astral Voyager",
            "The Cosmic Horizon",
            "The Stellar Phoenix",
            "The Dawn Treader",
            "The Starborn",
            "The Cosmic Echo",
            "The Nebula Dancer",
            "The Star Chaser",
            "The Void Walker",
            "The Stellar Guardian",
            "The Cosmic Valor",
            "The Star Sovereign",
            "The Nova's Grace",
            "The Celestial Storm",
            "The Astral Pioneer",
            "The Cosmic Venture",
            "The Star Seeker",
            "The Void Whisper",
            "The Nova Knight",
            "The Stellar Horizon",
            "The Cosmic Light",
            "The Star Drifter",
            "The Nebula Weaver",
            "The Void Hunter",
            "The Stellar Dream",
            "The Cosmic Heart",
            "The Star Walker",
            "The Nova Spirit",
            "The Celestial Hope"
        ]
        
        self.selected_ship = random.choice(self.ship_names)
        self.game_title = f"Lost in the Lift: {self.selected_ship}'s Tale"
        
        # Create text surfaces with a shadow effect
        self.title_text = self.create_text_with_shadow(self.game_title, self.font_large)
        self.press_any_key = self.create_text_with_shadow("Press any key to begin", self.font_small)
        
        # Position the text
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.press_key_rect = self.press_any_key.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))

        self.start_time = pygame.time.get_ticks()
        self.input_delay = 500

        # Add button properties
        self.button_font = pygame.font.Font(None, 36)
        self.continue_button = self.create_text_with_shadow("Continue", self.button_font)
        self.button_rect = self.continue_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 7 // 8))
        self.button_hover = False

    def create_text_with_shadow(self, text, font, shadow_offset=2):
        # Create shadow text
        shadow_surface = font.render(text, True, BLACK)
        # Create main text
        text_surface = font.render(text, True, WHITE)
        
        # Create combined surface
        combined = pygame.Surface(shadow_surface.get_size(), pygame.SRCALPHA)
        combined.blit(shadow_surface, (shadow_offset, shadow_offset))
        combined.blit(text_surface, (0, 0))
        
        return combined

    def draw(self):
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Draw the moving ship
        self.ship.draw(self.screen)
        
        # Draw the text elements
        self.screen.blit(self.title_text, self.title_rect)
        
        if pygame.time.get_ticks() - self.start_time > self.input_delay:
            # Draw continue button with hover effect
            if self.button_hover:
                hover_button = self.create_text_with_shadow("Continue", self.button_font, shadow_offset=3)
                hover_rect = hover_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 7 // 8))
                self.screen.blit(hover_button, hover_rect)
            else:
                self.screen.blit(self.continue_button, self.button_rect)
            
        pygame.display.flip()

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    # Check if mouse is over button
                    mouse_pos = pygame.mouse.get_pos()
                    self.button_hover = self.button_rect.collidepoint(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_pos = pygame.mouse.get_pos()
                        if self.button_rect.collidepoint(mouse_pos):
                            return self.selected_ship
                elif event.type == pygame.KEYDOWN and current_time - self.start_time > self.input_delay:
                    if event.key == pygame.K_RETURN:  # Also allow Enter key to continue
                        return self.selected_ship

            self.ship.update()
            self.draw()
            self.clock.tick(60)