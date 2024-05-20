import pygame
import sys
from game import game_screen
from setup import setup_screen

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((1600, 800),)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_image = pygame.image.load("images/background/battle_ground.jpg").convert()
background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the fonts
font = pygame.font.Font(None, 36)

# Set up the buttons
button_width = 200
button_height = 50
start_button = pygame.Rect((screen.get_width() - button_width) // 2, (screen.get_height() - button_height) // 2, button_width, button_height)
quit_button = pygame.Rect((screen.get_width() - button_width) // 2, (screen.get_height() + button_height) // 2 + 20, button_width, button_height)

# Initialize screen state
current_screen = "main_menu"

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def mainMenu():
  
    # Draw the buttons
    pygame.draw.rect(screen, WHITE, start_button)
    pygame.draw.rect(screen, WHITE, quit_button)

    # Add text to the buttons
    start_text = font.render("Start", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    quit_text = font.render("Quit", True, BLACK)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)

    pygame.display.update()
    return "main_menu"

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                current_screen = "start_game"
            elif quit_button.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    # Draw the background
    screen.blit(background_image, (0, 0))
    if current_screen == "main_menu":
        current_screen = mainMenu()
    elif current_screen == "start_game":
        current_screen, player_list, ai_list = setup_screen(screen)
        
    elif current_screen == "game":
        result = game_screen(screen, player_list, ai_list)
        if result in ["restart", "main_menu"]:
            current_screen = result
    elif current_screen in ["restart"]:
        current_screen = "start_game"

    pygame.display.flip()
