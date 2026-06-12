import pygame
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Payday - The Heist Game"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
GRAY = (100, 100, 100)


class GameState(Enum):
    """Enum for different game states"""
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4


class Game:
    """Main game class"""
    
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.GAME_OVER:
                        self.state = GameState.MENU
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse clicks if needed
                pass
    
    def update(self):
        """Update game logic"""
        if self.state == GameState.PLAYING:
            # Update game logic here
            pass
        elif self.state == GameState.PAUSED:
            # Pause logic
            pass
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(DARK_GRAY)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_paused()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw the main menu"""
        title_text = self.font_large.render("PAYDAY", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_medium.render("The Heist Game", True, GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        instruction_text = self.font_small.render("Press SPACE to Start", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_game(self):
        """Draw the game world"""
        # Placeholder for game rendering
        game_text = self.font_medium.render("Game World - Press SPACE to Pause", True, WHITE)
        game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_text, game_rect)
    
    def draw_paused(self):
        """Draw the paused screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        paused_text = self.font_large.render("PAUSED", True, WHITE)
        paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(paused_text, paused_rect)
        
        resume_text = self.font_small.render("Press SPACE to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(resume_text, resume_rect)
    
    def draw_game_over(self):
        """Draw the game over screen"""
        game_over_text = self.font_large.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_text = self.font_small.render("Press SPACE to Return to Menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Main game loop"""
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
