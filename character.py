# Modify the Character class to include side, name, and other attributes
import pygame
import sys
import random
import math

pygame.init()
class Character():


    def attack(self, target,screen):
        
        self.image = self.attack_image
        self.last_attack_time = pygame.time.get_ticks()
        atk = 0
        defend=0
        if(self.type=="fighter"):
            atk=random.randint(5, 20)
        else:
            atk =random.randint(1,10)
        
        if(target.type=="fighter"):
            defend=random.randint(1, 10)
        else:
            defend=random.randint(5, 15)
        
        damage = atk-defend+random.randint(-5, 10)
        print("Damage:{damage}")
        if(damage>0):
            target.hp -= damage
        if(damage>0):
            self.exp += damage
        target.exp+=defend
        if(damage>10):
            target.exp+=math.ceil(target.exp*0.2)
        elif(damage<=0):
            target.exp+=math.ceil(target.exp*0.5)
        if target.exp>=100:
            target.exp-=100
            target.lvl+=1
        if self.exp>=100:
            self.exp-=100
            self.lvl+=1
        if target.hp<=0:
            target.alive=False
        self.update_time = pygame.time.get_ticks()

    def update(self):
        
        
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.last_attack_time >= self.attack_time:
            self.image = self.idle_image
            
		

    def __init__(self, side,name, char_name, max_hp, type, position):
        self.name=name
        self.char_name = char_name
        self.max_hp = max_hp
        self.hp = max_hp
        self.type = type
        self.lvl = 1
        self.exp = 0
    
        self.alive = True
        self.selected = False
        self.side = side
        self.attack_time = 500  # 0.5 seconds in milliseconds
        self.last_attack_time = 0
        self.load_images()
        # Load and resize the image
        img = pygame.image.load(f'images/characters/{self.char_name}/idle.png')
        small_width, small_height =100, 100  # Set to very small sizes
        self.image = pygame.transform.scale(img, (small_width, small_height))
        
        self.rect = self.image.get_rect()
        if side == "player":
            self.rect.center = (50 + (position * 100), 600)
        elif side == "ai":
            self.rect.center = (1550 - (position * 100), 600)

    def draw(self, screen):
        if self.selected:
            self.draw_selection_border(screen)
        screen.blit(self.image, self.rect)
        self.draw_exp_and_level(screen)
        self.draw_health_bar(screen)
        self.draw_name(screen)

    def draw_selection_border(self, screen):
        border_color = (0, 255, 0)  # Green color for selection
        border_rect = self.rect.inflate(10, 10)  # Create a larger rectangle for the border
        pygame.draw.rect(screen, border_color, border_rect, 3)  # Draw the border

    def load_images(self):
        idle_image = pygame.image.load(f"images/characters/{self.char_name}/idle.png")
        small_width, small_height =100, 100  # Set to very small sizes
        self.idle_image = pygame.transform.scale(idle_image, (small_width, small_height))
        
        if(self.side=="player"):
            attack_image = pygame.image.load(f"images/characters/{self.char_name}/attack_right.png")
        elif(self.side=="ai"):
            attack_image = pygame.image.load(f"images/characters/{self.char_name}/attack_left.png")
        small_width, small_height =100, 100  # Set to very small sizes
        self.attack_image = pygame.transform.scale(attack_image, (small_width, small_height))
        
    def draw_exp_and_level(self, screen):
        WHITE = (255, 255, 255)
        font = pygame.font.Font(None, 24)

        text_exp = font.render(f"Exp: {self.exp}/100", True, WHITE)
        text_lvl = font.render(f"Lvl: {self.lvl}", True, WHITE)
        
        exp_rect = text_exp.get_rect(center=(self.rect.centerx, self.rect.centery - 60))
        lvl_rect = text_lvl.get_rect(center=(self.rect.centerx, self.rect.centery - 80))

        screen.blit(text_lvl, lvl_rect)
        screen.blit(text_exp, exp_rect)

    def draw_health_bar(self, screen):
        red = (255, 0, 0)
        green = (0, 255, 0)

        # Calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red,  (self.rect.x, self.rect.y + self.rect.height, 50, 5))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y + self.rect.height, 50 * ratio, 5))

    def draw_name(self, screen):
        WHITE = (255, 255, 255)
        font = pygame.font.Font(None, 24)
        text_name = font.render(self.name, True, WHITE)
        name_rect = text_name.get_rect(center=(self.rect.centerx, self.rect.centery +100))
        screen.blit(text_name, name_rect)

    def is_clicked(self, pos):
        
        return self.rect.collidepoint(pos)
    