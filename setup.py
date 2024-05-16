import pygame
import sys
import os

pygame.init()

DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

background_path = "images/background/setup_background.jpg"  
wukong_path = "images/characters/wukong/wukong_idle.png"
bajie_path = "images/characters/bajie/bajie_idle.png"

window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

wukong_image = pygame.image.load(wukong_path)
wukong_image = pygame.transform.scale(wukong_image, (200, 200))
wukong_rect = wukong_image.get_rect()
wukong_rect.midtop = (DISPLAY_WIDTH // 4 - 150, 150)

bajie_image = pygame.image.load(bajie_path)
bajie_image = pygame.transform.scale(bajie_image, (200, 200))
bajie_rect = bajie_image.get_rect()
bajie_rect.midtop = (3 * DISPLAY_WIDTH // 4 + 150, 150)

small_wukong_image = pygame.transform.scale(wukong_image, (100, 100))
small_bajie_image = pygame.transform.scale(bajie_image, (100, 100))

selected_images = []
positions = [(DISPLAY_WIDTH // 2 - 150, DISPLAY_HEIGHT // 2 - 50), 
             (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50), 
             (DISPLAY_WIDTH // 2 + 150, DISPLAY_HEIGHT // 2 - 50), 
             (DISPLAY_WIDTH // 2 - 75, DISPLAY_HEIGHT // 2 + 100), 
             (DISPLAY_WIDTH // 2 + 75, DISPLAY_HEIGHT // 2 + 100)]

back_button_rect = pygame.Rect(20, 20, 100, 50)
next_button_rect = pygame.Rect(DISPLAY_WIDTH - 220, DISPLAY_HEIGHT - 60, 100, 50)  # Move left by 100 pixels

def handle_click(x, y):
    if 50 <= x <= 450 and 100 <= y <= 700 and len(selected_images)<5:
        selected_images.append('wukong')
    elif 1150 <= x <= 1550 and 100 <= y <= 700 and len(selected_images)<5:
        selected_images.append('bajie')
    else:
        for i, pos in enumerate(positions[:len(selected_images)]):
            img_rect = pygame.Rect(pos[0], pos[1], 100, 100)
            if img_rect.collidepoint(x, y):
                selected_images.pop(i)
                break

def draw_selected_images():
    for i, img in enumerate(selected_images):
        if i >= 5:
            break
        if img == 'wukong':
            window.blit(small_wukong_image, positions[i])
        elif img == 'bajie':
            window.blit(small_bajie_image, positions[i])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            handle_click(mouse_x, mouse_y)

    window.blit(background, (0, 0))

    draw_text("Please choose your champion", WHITE, DISPLAY_WIDTH // 2, 50)
    draw_text("(Your team size should be 3-5 champions)", WHITE, DISPLAY_WIDTH // 2, 100)

    pygame.draw.rect(window, BLACK, [50, 100, 400, 600])
    window.blit(wukong_image, wukong_rect)
    draw_text("WUKONG the great sage", WHITE, 250, 400)
    draw_text("ATK : 5 - 20", WHITE, 250, 450)
    draw_text("DEF : 1 - 10", WHITE, 250, 500)

    pygame.draw.rect(window, BLACK, [1150, 100, 400, 600])
    window.blit(bajie_image, bajie_rect)
    draw_text("BAJIE the marshal canopy", WHITE, 1350, 400)
    draw_text("ATK : 1 - 10", WHITE, 1350, 450)
    draw_text("DEF : 5 - 15", WHITE, 1350, 500)

    pygame.display.update()