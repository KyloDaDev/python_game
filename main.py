import pygame
import sys
from game import game_screen
from setup import setup_screen

# Initialize Pygame
pygame.init()
# Initialize Pygame mixer
pygame.mixer.init()

pygame.mixer.music.load("sound/main.mp3")
pygame.mixer.music.play(-1)  
# Load click sound
click_sound = pygame.mixer.Sound("sound/click.mp3") 
# Set up the screen
screen = pygame.display.set_mode((1600, 800))
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
background_image = pygame.image.load("images/background/battle_ground.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Set up colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
font_path = 'font/NotoSansCJK-Regular.otf'  # Adjust path as needed
font = pygame.font.Font(font_path, 36)

# Set up the buttons
button_width = 200
button_height = 50
button_spacing = 20
start_button = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 - button_height * 2 - button_spacing * 2, button_width, button_height)
option_button = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2, button_width, button_height)
quit_button = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 + button_height * 2 + button_spacing * 2, button_width, button_height)
back_button = pygame.Rect(20, 20, 100, 30)  # Smaller back button in the top left

language_buttons = {
    "Chinese": pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 - button_height - button_spacing, button_width, button_height),
    "English": pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 + button_height + button_spacing, button_width, button_height)
}

selected_language = None  # Initially no language selected
current_screen = "main_menu"  # Initial screen state

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def draw_setting_page():
    global current_screen, selected_language
    screen.fill(WHITE)

    # Determine text based on selected language
    text_back = "返回" if selected_language == "Chinese" else "Back"

    # Draw back button
    back_text = font.render(text_back, True, BLACK)
    screen.blit(back_text, back_text.get_rect(center=back_button.center))

    # Draw language options with selection effect
    for lang, rect in language_buttons.items():
        text = "中文" if lang == "Chinese" and selected_language == "Chinese" else "English" if lang == "English" and selected_language == "Chinese" else lang
        color = GREEN if selected_language == lang else BLUE
        pygame.draw.rect(screen, color, rect)
        text_surf = font.render(text, True, BLACK)
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    # Process input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                click_sound.play()
                current_screen = "main_menu"  # Return to the main menu when back button is clicked
            for lang, rect in language_buttons.items():
                if rect.collidepoint(event.pos):
                    click_sound.play()
                    selected_language = lang  # Update selected language

def mainMenu():
    # Update texts based on selected language before drawing
    text_start = "开始" if selected_language == "Chinese" else "Start"
    text_options = "选项" if selected_language == "Chinese" else "Options"
    text_quit = "退出" if selected_language == "Chinese" else "Quit"
    
    # Draw the buttons
    pygame.draw.rect(screen, WHITE, start_button)
    pygame.draw.rect(screen, WHITE, option_button)
    pygame.draw.rect(screen, WHITE, quit_button)

    # Add text to the buttons
    start_text = font.render(text_start, True, BLACK)
    screen.blit(start_text, start_text.get_rect(center=start_button.center))

    option_text = font.render(text_options, True, BLACK)
    screen.blit(option_text, option_text.get_rect(center=option_button.center))

    quit_text = font.render(text_quit, True, BLACK)
    screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

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
            if current_screen == "main_menu":
                if start_button.collidepoint(mouse_pos):
                    click_sound.play()
                    current_screen = "start_game"
                elif option_button.collidepoint(mouse_pos):
                    click_sound.play()
                    current_screen = "settings_menu"
                elif quit_button.collidepoint(mouse_pos):
                    click_sound.play()
                    pygame.quit()
                    sys.exit()
            elif current_screen == "settings_menu":
                draw_setting_page()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Draw the background
    screen.blit(background_image, (0, 0))
    if current_screen == "main_menu":
        # Load and play background music
        
          
        current_screen = mainMenu()
    elif current_screen == "start_game":
        # Load and play background music  
        current_screen, player_list, ai_list = setup_screen(screen,selected_language)
    elif current_screen == "game":
        pygame.mixer.music.load("sound/battle.mp3")  # Load battle music
        pygame.mixer.music.play(-1)
        result = game_screen(screen, player_list, ai_list,selected_language)
        pygame.mixer.music.load("sound/main.mp3")
        pygame.mixer.music.play(-1)
        if result in ["restart", "main_menu"]:
            current_screen = result
    elif current_screen in ["restart"]:
        current_screen = "start_game"
    elif current_screen == "settings_menu":
        draw_setting_page()

    pygame.display.flip()
