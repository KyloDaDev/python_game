import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up window
WIDTH, HEIGHT = 1600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("End Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


font_path = 'font/NotoSansCJK-Regular.otf'  # Adjust path as needed
font = pygame.font.Font(font_path, 36)



def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def end_menu():
    WIN.fill(WHITE)
    draw_text("You win!", font, BLACK, WIN, WIDTH // 2, HEIGHT // 3)
    
    try_again_btn = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    main_menu_btn = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 50)
    
    pygame.draw.rect(WIN, BLACK, try_again_btn)
    draw_text("Try again", font, WHITE, WIN, WIDTH // 2, HEIGHT // 2 + 25)
    
    pygame.draw.rect(WIN, BLACK, main_menu_btn)
    draw_text("Main menu", font, WHITE, WIN, WIDTH // 2, HEIGHT // 2 + 125)
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if try_again_btn.collidepoint(mouse_pos):
                    print("Try again!")
                    # Call your try again function here
                if main_menu_btn.collidepoint(mouse_pos):
                    print("Main menu!")
                    # Call your main menu function here

