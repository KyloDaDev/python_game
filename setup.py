import pygame
import sys
import random
from character import Character

pygame.init()

DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
DARK_GRAY = (169, 169, 169)  # Color for inactive "next" button

background_path = "images/background/setup_background.jpg"
wukong_path = "images/characters/wukong/setup.png"
bajie_path = "images/characters/bajie/setup.png"

window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

click_sound = pygame.mixer.Sound("sound/click.mp3") 
font_path = 'font/NotoSansCJK-Regular.otf'  # Adjust path as needed
font = pygame.font.Font(font_path, 24)



def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)
class InputBox:
        def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = WHITE
            self.text = text
            self.txt_surface = font.render(text, True, BLACK)
            self.active = False

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = RED if self.active else WHITE
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    self.txt_surface = font.render(self.text, True, BLACK)

        def draw(self, screen):
            pygame.draw.rect(screen, WHITE, self.rect)
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 1))
            pygame.draw.rect(screen, self.color, self.rect, 2)

def setup_screen(window,language):

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

     
    ai_character_names = ['wukong', 'bajie']

    input_boxes = []
    positions = [(DISPLAY_WIDTH // 2 - 150, DISPLAY_HEIGHT // 2 - 50),
                (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 50),
                (DISPLAY_WIDTH // 2 + 150, DISPLAY_HEIGHT // 2 - 50),
                (DISPLAY_WIDTH // 2 - 75, DISPLAY_HEIGHT // 2 + 100),
                (DISPLAY_WIDTH // 2 + 75, DISPLAY_HEIGHT // 2 + 100)]

    selected_images = []
   
    for pos in positions:
        input_boxes.append(InputBox(pos[0], pos[1] + 110, 100, 30))

    back_button_rect = pygame.Rect(20, 20, 100, 50)
    next_button_rect = pygame.Rect(DISPLAY_WIDTH - 220, DISPLAY_HEIGHT - 60, 100, 50)

    def handle_click(x, y):
        if 50 <= x <= 450 and 100 <= y <= 700 and len(selected_images) < 5:
            click_sound.play()
            selected_images.append('wukong')
        elif 1150 <= x <= 1550 and 100 <= y <= 700 and len(selected_images) < 5:
            click_sound.play()
            selected_images.append('bajie')
        else:
            for i, pos in enumerate(positions[:len(selected_images)]):
                img_rect = pygame.Rect(pos[0], pos[1], 100, 100)
                if img_rect.collidepoint(x, y):
                    click_sound.play()
                    selected_images.pop(i)
                    input_boxes[i].text = ""  # Clear the name when the image is removed
                    break
    
    def draw_selected_images():
        global wukong_count, bajie_count
        wukong_count = 0
        bajie_count = 0
        for i, img in enumerate(selected_images):
            if i >= 5:
                break
            if img == 'wukong':
                window.blit(small_wukong_image, positions[i])
                wukong_count+=1
            elif img == 'bajie':
                window.blit(small_bajie_image, positions[i])
                bajie_count+=1
            input_boxes[i].draw(window)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                handle_click(mouse_x, mouse_y)
                if next_button_rect.collidepoint(mouse_x, mouse_y) and len(selected_images) >= 3:
                    player_count = len(selected_images)
                    ai_count = len(selected_images)  # Example AI count
                    player_position = 1
                    ai_position = 1

                    # Create player characters
                    player_characters = []
                    for i, img in enumerate(selected_images):
                        if img == 'wukong':
                            player_characters.append(Character('player',input_boxes[i].text, 'wukong', 100, "fighter", player_position))
                            player_position += 1
                            player_count += 1
                        
                        elif img == 'bajie':
                            player_characters.append(Character('player',input_boxes[i].text, 'bajie', 100, "tank", player_position))
                            player_position += 1
                            player_count += 1
                        
                        
                    

                    # Create AI characters
                    
                    ai_characters = []
                    for i in range(ai_count):
                        ai_name = f"AI{random.randint(10, 99)}"
                        character_name = random.choice(ai_character_names)
                        ai_position = i  # Adjust this according to your positioning logic
                        ai_characters.append(Character('ai', ai_name, character_name, 100, 6, ai_position))

                    return "game",player_characters,ai_characters
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    return  "main_menu",[],[]
            for box in input_boxes:
                box.handle_event(event)

        window.blit(background, (0, 0))
        choose_chpm = "开始" if language == "Chinese" else "Please Choose Your Champion"
        draw_text(choose_chpm, WHITE, DISPLAY_WIDTH // 2, 50)
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

        pygame.draw.rect(window, GRAY, [50, 700, 1500, 200])
        draw_text('Click the "next" button to go next', WHITE, DISPLAY_WIDTH // 2, 750)

        draw_selected_images()

        pygame.draw.rect(window, RED, back_button_rect)
        draw_text("<back", WHITE, back_button_rect.centerx, back_button_rect.centery)

        if len(selected_images) >= 3:
            pygame.draw.rect(window, RED, next_button_rect)
            draw_text("next>", WHITE, next_button_rect.centerx, next_button_rect.centery)
        else:
            pygame.draw.rect(window, DARK_GRAY, next_button_rect)
            draw_text("next>", WHITE, next_button_rect.centerx, next_button_rect.centery)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
