import pygame
import sys
pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
screen = pygame.display.set_mode((1600, 800),)

WIDTH, HEIGHT = screen.get_width(), screen.get_height()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battle')
action_cooldown=0
action_wait_time= 90


#load images
#background image
background_img = pygame.image.load('images/background/mainmenu.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))
#panel image
panel_img = pygame.image.load('images/icons/panel.png').convert_alpha()
panel_img = pygame.transform.scale(panel_img, (screen.get_width(),350))


#function for drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))


#function for drawing panel
def draw_panel():
	bottom_panel = 150
	screen.blit(panel_img, (0, HEIGHT - bottom_panel))


#fighter class
class Character():
    def attack(self,target):
       target.hp-=1
	

    def update(self,hp,exp,lvl):
       self.hp=hp
       self.exp=exp
       self.lvl=lvl
	
    def __init__(self, side,name, max_hp, strength,position):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        
       
        self.alive = True
        img = pygame.image.load(f'images/{self.name}/idle.png')
        self.image = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        self.rect = self.image.get_rect()
        if side == "left":
            self.rect.center = (100+((position) * 100), HEIGHT - 150-self.image.get_height() // 2)  # Set y position to bottom of screen
        elif side == "right":
            self.rect.center = (WIDTH - 100- ((position) * 100), HEIGHT-150 - self.image.get_height() // 2)
              # Set y position to bottom of screen
			  
    
    def draw(self):
	    screen.blit(self.image, self.rect)
 
		

    

		
    
    
		

    
		

class HealthBar():
	
   

	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp


	def draw(self, hp):
		red = (255, 0, 0)
		green=(0,255,0)
	    
		#update with new health
		self.hp = hp
	
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

class Exp():
    def __init__(self,x,y,exp,lvl):
      self.x = x
      self.y = y
      self.exp=exp
      self.lvl = lvl
    
    def draw(self,exp,lvl):
		# Colors
        WHITE = (255, 255, 255)

        # Font settings
        font = pygame.font.Font(None, 36)
        self.exp = exp
        self.lvl = lvl
        text_exp = font.render(f"Exp: {self.exp}/100", True, WHITE)
        text_level = font.render(f"Lvl: {self.lvl}", True, WHITE)
        
        # Calculate vertical spacing
        spacing = 10
        text_height = text_exp.get_height() + text_level.get_height() + spacing
        
        # Position the text vertically centered
        y_exp = self.y
        y_level = y_exp + text_exp.get_height() + spacing

        # Draw the text
        screen.blit(text_level, (self.x, y_exp))
        screen.blit(text_exp, (self.x, y_level))

	  

	
	  
    
		
	

        
		
	

knight = Character("left",  'knight', 300, 10,1)
knight2 = Character("left",  'knight', 30, 10,3)
knight3 = Character("left",  'knight', 30, 10,5)

bandit1 = Character("right", 'bandit', 100, 6, 1)
bandit2 = Character("right",  'bandit', 20, 6, 3)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)


knight_health_bar = HealthBar(140, 800 - 350 + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, 800 - 350 + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, 800 - 350 + 100, bandit2.hp, bandit2.max_hp)

exp_display = Exp(140, 800 - 350-30 , 0, 1)

run = True
while run:
	
   
	clock.tick(fps)
	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	knight_health_bar.draw(knight.hp)
    #draw fighters
	knight.draw()
	knight2.draw()
	knight3.draw()
	exp_display.draw(100,2)
	
	for bandit in bandit_list:
		bandit.draw()
	bandit1_health_bar.draw(bandit1.hp)
	action_cooldown+=1
	if action_cooldown>= action_wait_time:
		knight.attack(bandit1)
		action_cooldown=0
	    
	    
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
    
    
    
    
    

	pygame.display.update()

pygame.quit()
