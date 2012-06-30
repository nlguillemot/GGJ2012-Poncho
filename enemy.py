import pygame
import vector2
import bullet
import collision as cl

enemy_list = list()

def spawn_enemies(the_map):
	#create enemy1 and set position
	for entries in the_map.map_enemies:
			new_enemy = enemy()
			new_enemy.set_image(pygame.image.load(entries[0] + ".png").convert_alpha())
			new_enemy.set_position(entries[1], entries[2])
	
#Base enemy class that all other enemies inherit from
class enemy:
	def __init__(self):
		self.max_movement_speed = 200 
		self.movement_direction = 1 
		enemy_list.append(self)		#1 --> Moving right/down
				#-1 --> Moving left/up
	def set_image(self,image):
		self.image = image
		
	def update(self, dtime):
		for bullets in bullet.bullet_list:
			if cl.AABB_2d_collide(self.position.x, self.position.y, self.image.get_width(), self.image.get_height(), 
			bullets.position.x, bullets.position.y, bullets.image.get_width(), bullets.image.get_height()):
				enemy_list.remove(self)
				break
				
	#sets the x and y of the character
	def set_position(self, xpos, ypos):
		self.position = vector2.vector2(xpos, ypos)
	#retrieves the x and y of the character
	def get_position(self):
		return self.position
		
	def draw(self, screen):
		screen.blit(self.image, pygame.Rect(self.position.x,self.position.y,0,0))
