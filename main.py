import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Game Title")

# Load the background image

WIDTH, HEIGHT = screen.get_width(), screen.get_height()
background_image = pygame.image.load("/Applications/workspace/python/images/background/mainmenu.png").convert()
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
back_button_rect = pygame.Rect(10, 10, 80, 30)


# Initialize screen state
current_screen = "main_menu"



# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                current_screen = "end_menu"
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

    elif current_screen == "end_menu":
        # Call the end_menu function
        print("ENDDD")
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

    # Update the screen
    pygame.display.flip()


    


