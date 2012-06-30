import pygame
import character

class gui:

	def __init__(self):
		self.font = pygame.font.Font("arial.ttf", 28)
		
	#set the player which the gui will display info about
	def set_player(self,player):
		self.player = player
	
	def draw(self,screen):
		pygame.font.init()
		ammo_draw = self.font.render("["*self.player.bullet_ammo, True, (255,0,0))
		screen.blit(ammo_draw, ((screen.get_width() - ammo_draw.get_width()),(0)))
		
		reload_draw = pygame.Surface(((self.player.bullet_reload_time*70),24))
		reload_draw.fill(0xFFFF00)
		screen.blit(reload_draw,(430,6))
