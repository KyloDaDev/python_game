import pygame
import random
from character import Character

pygame.init()

def game_screen(window, player_list, ai_list):
    clock = pygame.time.Clock()
    fps = 60

    # Game window
    screen = pygame.display.set_mode((1600, 800))
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    pygame.display.set_caption('Battle')

    # Load images
    background_img = pygame.image.load('images/background/mainmenu.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))
    panel_img = pygame.image.load('images/icons/panel.png').convert_alpha()
    panel_img = pygame.transform.scale(panel_img, (screen.get_width(), 150))

    # Fonts
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    # Function for drawing background
    def draw_bg():
        screen.blit(background_img, (0, 0))

    # Function for drawing panel
    def draw_panel():
        screen.blit(panel_img, (0, HEIGHT - 150))

    def draw_end_screen(message):
        # Draw the semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)  # Adjust the transparency level (0-255)
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (0, 0))

        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text, text_rect)

        restart_btn = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
        main_menu_btn = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 50)

        pygame.draw.rect(screen, (0, 0, 0), restart_btn)
        draw_text("Restart", small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 25)
        pygame.draw.rect(screen, (0, 0, 0), main_menu_btn)
        draw_text("Main Menu", small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 125)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if restart_btn.collidepoint(mouse_pos):
                        return "restart"
                    if main_menu_btn.collidepoint(mouse_pos):
                        return "main_menu"

    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)
    
    # AI attack timing variables
    ai_attack_delay = 1000  # Delay in milliseconds (4 seconds)
    last_attack_time = 0
    player_attacked = False

    def trigger_ai_attack():
        nonlocal last_attack_time, player_attacked
        player_attacked = False
        last_attack_time = pygame.time.get_ticks()

    def update_ai_attack():
        nonlocal last_attack_time, player_attacked
        if player_attacked:
            current_time = pygame.time.get_ticks()
            if current_time - last_attack_time > ai_attack_delay:
                last_attack_time = current_time
                # AI's turn to attack
                if ai_characters and player_characters:  # Ensure there are characters to attack
                    ai_attacker = random.choice(ai_characters)
                    player_target = random.choice(player_characters)
                    ai_attacker.attack(player_target, screen)
                    print(f"{ai_attacker.name} attacks {player_target.name}")
                    
                    # Check if the attacked player character is dead
                    if player_target.hp <= 0:
                        player_characters.remove(player_target)
                    player_attacked = False  # Reset the flag after AI attacks

    run = True

    # Create player characters
    player_characters = player_list

    # Create AI characters
    ai_characters = ai_list

    selected_character = None

    while run:
        clock.tick(fps)
        draw_bg()
        draw_panel()

        # Draw characters
        for char in player_characters + ai_characters:
            if char.alive:
                char.draw(screen)
                char.update()
            else:
                if char.side == "player":
                    player_characters.remove(char)
                elif char.side == "ai":
                    ai_characters.remove(char)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                # Check if a player character was clicked
                for char in player_characters:
                    if char.is_clicked(pos):
                        if selected_character:
                            selected_character.selected = False  # Deselect previously selected character
                        selected_character = char
                        selected_character.selected = True  # Select the clicked character
                        break
                else:  # If no player character was clicked
                    # Check if an enemy was clicked
                    for char in ai_characters:
                        if char.is_clicked(pos):
                            # Player's attack logic
                            if selected_character:
                                selected_character.attack(char, screen)
                                print(f"{selected_character.name} attacks {char.name}")
                                selected_character.selected = False  # Deselect after attack
                                selected_character = None

                                # Check if the attacked AI character is dead
                                if char.hp <= 0:
                                    ai_characters.remove(char)

                                # Trigger AI attack with a delay after player attacks
                                if ai_characters:
                                    
                                    trigger_ai_attack()
                                    player_attacked = True

                            break

        # Check if the game is over
        if not player_characters:
            return draw_end_screen("You Lost!")
        elif not ai_characters:
            return draw_end_screen("You Win!")
        
        # Update AI attack
        update_ai_attack()

        pygame.display.update()

    pygame.quit()
    return "quit"
