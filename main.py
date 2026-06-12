import pygame
import sys
import math
from enum import Enum

pygame.init()

# Constants
INITIAL_WIDTH = 1280
INITIAL_HEIGHT = 720
FPS = 60
TITLE = "Make It Rain"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (20, 20, 20)
GOLD = (255, 215, 0)
DARK_GOLD = (200, 170, 0)


class Scene(Enum):
    INTRO = 1
    MAIN_MENU = 2


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = Scene.INTRO
        self.elapsed_time = 0
        self.width = INITIAL_WIDTH
        self.height = INITIAL_HEIGHT
        
        # Fonts
        self.font_huge = pygame.font.Font(None, 120)
        self.font_large = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 40)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.scene == Scene.INTRO and event.key == pygame.K_SPACE:
                    self.scene = Scene.MAIN_MENU
                    self.elapsed_time = 0
    
    def update(self):
        self.elapsed_time += 1 / FPS
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.scene == Scene.INTRO:
            self.draw_intro()
        elif self.scene == Scene.MAIN_MENU:
            self.draw_main_menu()
        
        pygame.display.flip()
    
    def draw_intro(self):
        """Multi-scene intro animation"""
        t = self.elapsed_time
        
        # Scene 1: Rain drops falling (0-2 seconds)
        if t < 2:
            progress = t / 2
            self.draw_rain_scene(progress)
        
        # Scene 2: Title emergence with glow (2-4 seconds)
        elif t < 4:
            progress = (t - 2) / 2
            self.draw_title_emergence(progress)
        
        # Scene 3: Full title with particle effects (4-6 seconds)
        elif t < 6:
            progress = (t - 4) / 2
            self.draw_title_final(progress)
        
        # Scene 4: Fade to main menu (6-7 seconds)
        elif t < 7:
            progress = (t - 6) / 1
            self.draw_fade_transition(progress)
        
        # Auto transition to main menu
        else:
            self.scene = Scene.MAIN_MENU
            self.elapsed_time = 0
        
        # Skip instruction
        skip_text = pygame.font.Font(None, 20).render("Press SPACE to continue", True, GOLD)
        skip_rect = skip_text.get_rect(bottomright=(self.width - 20, self.height - 20))
        self.screen.blit(skip_text, skip_rect)
    
    def draw_rain_scene(self, progress):
        """Falling rain effect with fading in"""
        num_drops = 30
        for i in range(num_drops):
            x = (i * self.width / num_drops + math.sin(i) * 50) % self.width
            y = (progress * self.height * 1.5 - (i % 5) * 100) % self.height
            
            alpha = int(255 * min(progress * 2, 1))
            drop_length = 20
            
            color_intensity = int(GOLD[0] * alpha / 255)
            pygame.draw.line(
                self.screen,
                (color_intensity, color_intensity // 2, 0),
                (x, y),
                (x, y + drop_length),
                2
            )
    
    def draw_title_emergence(self, progress):
        """Title emerges with scale and glow"""
        # Draw subtle rain in background
        num_drops = 10
        for i in range(num_drops):
            x = (i * self.width / num_drops) % self.width
            y = ((progress * 0.5 * self.height) - (i % 3) * 50) % self.height
            pygame.draw.line(self.screen, (DARK_GOLD[0] // 2, DARK_GOLD[1] // 2, 0), (x, y), (x, y + 15), 1)
        
        # Glow effect
        glow_intensity = int(100 * progress)
        glow_surface = pygame.Surface((self.width, self.height))
        glow_surface.set_alpha(glow_intensity)
        glow_surface.fill(GOLD)
        self.screen.blit(glow_surface, (0, 0))
        
        # Scale title in
        scale = 0.3 + progress * 0.7
        font_size = int(120 * scale)
        title_font = pygame.font.Font(None, font_size)
        title_text = title_font.render(TITLE, True, GOLD)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(title_text, title_rect)
    
    def draw_title_final(self, progress):
        """Final title display with money/particle effects"""
        # Draw falling money particles
        num_particles = 20
        for i in range(num_particles):
            x = (i * self.width / num_particles + math.sin(i + progress * 5) * 30) % self.width
            y = (progress * self.height * 0.5 + (i % 5) * 50) % self.height
            
            particle_size = 3
            pygame.draw.circle(self.screen, GOLD, (int(x), int(y)), particle_size)
        
        # Static title with glow
        title_text = self.font_huge.render(TITLE, True, GOLD)
        
        # Draw glow by rendering slightly offset multiple times
        glow_offset = 10
        for offset_x in range(-glow_offset, glow_offset + 1, 3):
            for offset_y in range(-glow_offset, glow_offset + 1, 3):
                glow_surface = title_text.copy()
                glow_surface.set_alpha(30)
                glow_rect = title_text.get_rect(
                    center=(self.width // 2 + offset_x, self.height // 2 + offset_y)
                )
                self.screen.blit(glow_surface, glow_rect)
        
        # Final title
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(title_text, title_rect)
    
    def draw_fade_transition(self, progress):
        """Fade to black and transition to menu"""
        # Draw final title
        title_text = self.font_huge.render(TITLE, True, GOLD)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(title_text, title_rect)
        
        # Fade overlay
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.set_alpha(int(255 * progress))
        fade_surface.fill(BLACK)
        self.screen.blit(fade_surface, (0, 0))
    
    def draw_main_menu(self):
        """Main menu with title only"""
        # Subtle animated background
        t = self.elapsed_time * 0.5
        for i in range(5):
            alpha = int(20 * (math.sin(t + i) + 1))
            line_y = (i * self.height / 5) % self.height
            line_surface = pygame.Surface((self.width, 1))
            line_surface.set_alpha(alpha)
            line_surface.fill(GOLD)
            self.screen.blit(line_surface, (0, line_y))
        
        # Main title
        title_text = self.font_huge.render(TITLE, True, GOLD)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtle subtitle
        subtitle_text = self.font_medium.render("The Game", True, DARK_GOLD)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, self.height // 2 + 100))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
