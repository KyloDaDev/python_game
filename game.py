import pygame
import random
from character import Character

pygame.init()

def game_screen(window, player_list, ai_list,language):
    clock = pygame.time.Clock()
    fps = 60
    click_sound = pygame.mixer.Sound("sound/click.mp3") 
    attack_sound = pygame.mixer.Sound("sound/attack.mp3") 
    die_sound = pygame.mixer.Sound("sound/die.mp3") 
    # Game window
    screen = pygame.display.set_mode((1600, 800))
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    pygame.display.set_caption('Battle')
    
    # Load images
    background_img = pygame.image.load('images/background/battle_ground.jpg').convert_alpha()
    background_img = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))
    
    burger_menu_img = pygame.image.load('images/icons/burger_menu.png').convert_alpha()
    burger_menu_img = pygame.transform.scale(burger_menu_img, (50, 50))

    # Fonts
    
    font_path = 'font/NotoSansCJK-Regular.otf'  # Adjust path as needed
    font = pygame.font.Font(font_path, 74)


    small_font = pygame.font.Font(font_path, 36)
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(80)  # Adjust the transparency level (0-255)
    overlay.fill((0, 0, 0))  # Black color for the overlay

    # Function for drawing background
    def draw_bg():
        screen.blit(background_img, (0, 0))
        screen.blit(overlay, (0, 0))


    

    def draw_end_screen(message,language):
        
        draw_bg()  # Draw the background instead of the overlay

        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text, text_rect)

        restart_btn = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
        main_menu_btn = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 50)

        pygame.draw.rect(screen, (0, 0, 0), restart_btn)
        restart_txt="重新开始" if language == "Chinese" else "Restart"    #TODO
        draw_text(restart_txt, small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 25)
        pygame.draw.rect(screen, (0, 0, 0), main_menu_btn)
        mainmeu_txt="主菜单" if language == "Chinese" else "Mainmenu"    #TODO
        draw_text(mainmeu_txt, small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 125)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if restart_btn.collidepoint(mouse_pos):
                        click_sound.play()
                        return "restart"
                    if main_menu_btn.collidepoint(mouse_pos):
                        click_sound.play()
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
                    attack_sound.play()
                    ai_attacker.attack(player_target, screen)
                    print(f"{ai_attacker.name} attacks {player_target.name}")
                    
                    # Check if the attacked player character is dead
                    if player_target.hp <= 0:
                        die_sound.play()
                        print("die")
                        player_characters.remove(player_target)
                        
                    player_attacked = False  # Reset the flag after AI attacks

    run = True

    # Create player characters
    player_characters = player_list

    # Create AI characters
    ai_characters = ai_list

    selected_character = None

    menu_open = False
    burger_menu_rect = pygame.Rect(WIDTH - 60, 10, 50, 50)
    resume_btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
    end_game_btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)

    while run:
        clock.tick(fps)
        draw_bg()
       

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

        # Draw burger menu button
        screen.blit(burger_menu_img, burger_menu_rect.topleft)

        # Draw menu options if menu is open
        if menu_open:
            # Draw the semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)  # Adjust the transparency level (0-255)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            pygame.draw.rect(screen, (255, 255, 255), resume_btn_rect)
            resume_txt ="恢复游戏" if language == "Chinese" else "Resume"    #TODO
            draw_text(resume_txt, small_font, (0, 0, 0), screen, resume_btn_rect.centerx, resume_btn_rect.centery)
            pygame.draw.rect(screen, (255, 255, 255), end_game_btn_rect)
            endgame_txt="结束游戏" if language == "Chinese" else "End Game"    #TODO
            draw_text(endgame_txt, small_font, (0, 0, 0), screen, end_game_btn_rect.centerx, end_game_btn_rect.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                if burger_menu_rect.collidepoint(pos):
                    click_sound.play()
                    menu_open = not menu_open  # Toggle menu
                elif menu_open:
                    if resume_btn_rect.collidepoint(pos):
                        click_sound.play()
                        menu_open = False  # Close menu
                    elif end_game_btn_rect.collidepoint(pos):
                        click_sound.play()
                        return "main_menu"
                else:
                    # Check if a player character was clicked
                    for char in player_characters:
                        if char.is_clicked(pos):
                            click_sound.play()
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
                                    attack_sound.play()
                                    selected_character.attack(char, screen)
                                    print(f"{selected_character.name} attacks {char.name}")
                                    selected_character.selected = False  # Deselect after attack
                                    selected_character = None

                                    # Check if the attacked AI character is dead
                                    if char.hp <= 0:
                                        die_sound.play()
                                        ai_characters.remove(char)
                                        

                                    # Trigger AI attack with a delay after player attacks
                                    if ai_characters:
                                        trigger_ai_attack()
                                        player_attacked = True

                                break

        # Check if the game is over
        if not player_characters:
            pygame.mixer.music.load("sound/lost.mp3")
            pygame.mixer.music.play(-1)  
            return draw_end_screen("再接再厉，下次胜利"if language == "Chinese" else "You Lost!",language)
        elif not ai_characters:
            pygame.mixer.music.load("sound/win.mp3")
            pygame.mixer.music.play(-1)  
            return draw_end_screen("大吉大利今晚吃鸡"if language == "Chinese" else "You Win!",language)
        
        # Update AI attack
        update_ai_attack()

        pygame.display.update()

    pygame.quit()
    return "quit"
