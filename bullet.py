import vector2
import pygame

#speed of bullets shot in px/s
bullet_speed = 500

#global list of bullets currently active in the game
bullet_list = []

bullet_image = pygame.image.load("bullet.png")

#represents a projectile fired by the character
class bullet:	
	#initialized with a given speed and position
	def __init__(self,xpos,ypos,xspeed,yspeed):
		self.position = vector2.vector2(xpos,ypos)
		self.speed = vector2.vector2(xspeed,yspeed)
		self.image = bullet_image
	
	#update position in function of time (time in seconds)
	def update(self,dtime):
		#update position with speed
		self.position.x += self.speed.x * dtime
		self.position.y += self.speed.y * dtime
		self.__handle_out_of_screen_bounds()
		
	#pops bullet to other side of screen if it goes out of bounds
	def __handle_out_of_screen_bounds(self):
		screen_width = pygame.display.get_surface().get_width()
		screen_height = pygame.display.get_surface().get_height()
		
		if(self.position.x >= screen_width): #out of the screen at the right
			self.position.x = -self.image.get_width()
		elif(self.position.x <= -self.image.get_width()): #out of the screen at the left
			self.position.x = screen_width
		if(self.position.y >= screen_height): #out of the screen at the bottom
			self.position.y = -self.image.get_height()
		elif(self.position.y <= -self.image.get_height()): #out of the screen at the top
			self.position.y = screen_height
	def draw(self,screen):
		screen.blit(self.image, pygame.Rect(self.position.x,self.position.y,0,0))