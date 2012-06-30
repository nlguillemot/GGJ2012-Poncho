import pygame
import vector2
import bullet
import collision as cl
from math import fabs
import enemy

gravity = 9.8
gravity_modifier = 3

#creates a class for characters in the game 
class character:
	#set run speed
	max_movement_speed = 200 #px/s
	min_movement_speed = 2
	movement_acceleration = 400 #ps/s^2
	friction_constant = 0.05 #u
	
	bullet_reload_max = 2 #milliseconds
	bullet_reload_ammo = 4
	
	position_x_start = 200
	position_y_start = 300

	jump_speed = 10 #px/s
	
	def __init__(self):
		self.set_acceleration(0,0)
		self.set_position(0,0)
		self.position.x = self.position_x_start
		self.position.y = self.position_y_start
		self.set_speed(0,0)
		self.direction = 1

		self.jumps_allowed = 2
		self.affected_by_gravity = True
		
		self.bullet_ammo = 4
		self.bullet_reload_time = 0
		
		self.__is_key_down_right = False
		self.__is_key_down_left = False
		
		#images
		self.idle = pygame.image.load("kid_idle.png").convert_alpha()
		self.run = pygame.image.load("kid_run.png").convert_alpha()
		self.jump = pygame.image.load("kid_jump.png").convert_alpha()
		self.skid = pygame.image.load("kid_skid.png").convert_alpha()	

		self.image = self.idle
		
		self.in_air = True
		
	#sets the x and y of the character
	def set_position(self, xpos, ypos):
		self.position = vector2.vector2(xpos, ypos)
	#retrieves the x and y of the character
	def get_position(self):
		return self.position
		
	#set the acceleration of the character
	def set_acceleration(self, xaccel, yaccel):
		self.acceleration = vector2.vector2(xaccel, yaccel)
	#get the acceleration of the character
	def get_acceleration(self):
		return self.acceleration

	#defines the horizontal and vertical speeds of the character
	def set_speed(self, xspeed, yspeed):
		self.speed = vector2.vector2(xspeed, yspeed)
	#retrieves the vector of the character's speed
	def get_speed(self):
		return self.speed
		
	#define whether or not the character is affected by gravity
	def set_affected_by_gravity(self, state):
		self.affected_by_gravity = state
		
	#applies gravity when necessary
	def __apply_gravity(self,dtime):
		self.speed.y += (gravity * gravity_modifier) * dtime
			
	#returns whether or not the character is on the ground
	def __on_hit_floor(self):
		self.in_air = False
		self.jumps_allowed = 2
			
	#returns whether or not the character is in the air
	def __is_in_air(self):
		return self.in_air
	
	#returns whether or not the character is moving horizontally at the maximum speed
	def __is_at_max_speed(self):
		return fabs(self.speed.x) >= self.max_movement_speed
	
	#def applies acceleration and friction depending on keys currently pressed and current speed and all that stuff
	def __update_x_acceleration(self):
		self.acceleration.x = 0
		if (self.__is_key_down_left and not self.speed.x <= -self.max_movement_speed):
			self.acceleration.x += -self.movement_acceleration
		if (self.__is_key_down_right and not self.speed.x >= self.max_movement_speed):
			self.acceleration.x += self.movement_acceleration
		if(not self.__is_key_down_left and not self.__is_key_down_right):
			self.speed.x *= (1.0-self.friction_constant)
			#if you're moving at a negligeable speed, just stop him 
			if(fabs(self.speed.x) <= (self.min_movement_speed)):
				self.speed.x = 0
			
	#updates the speed and position depending on the acceleration
	def __update_x_pos_and_speed(self,dtime):
		if(fabs(self.speed.x) > self.max_movement_speed):
			self.speed.x = self.max_movement_speed * fabs(self.speed.x)/self.speed.x
		self.speed.x += (self.acceleration.x * dtime)
		self.position.x += self.speed.x *dtime
	
	#updates the y position, speed, acceleration depending on dtime
	def __update_y_pos_speed_acceleration(self,dtime):
		self.__apply_gravity(dtime)
		self.position.y += self.speed.y

	#decides what the animation played should be based on the physics and the direction facing and all that
	def __update_animation(self):
		if(self.__is_in_air()):
			self.image = self.jump
		#on floor
		else:
			if(fabs(self.speed.x) <= self.min_movement_speed):
				self.image = self.idle
			elif((self.__is_key_down_left == False) and (self.__is_key_down_right == False)):
				self.image = self.skid
			else:
				self.image = self.run
				
	#updating bullet properties
	def __update_bullet(self,dtime):
		if (self.bullet_reload_time > 0):
			self.bullet_reload_time -= dtime
			if(self.bullet_reload_time <= 0):
				self.bullet_ammo = self.bullet_reload_ammo
				
				self.bullet_reload_time = 0
			
		if ((self.bullet_ammo == 0) and (self.bullet_reload_time == 0)):
			self.bullet_reload_time = self.bullet_reload_max
	
	def set_tile_map_for_collisions(self,target):
		self.tile_map_for_collisions = target
	
	def set_tile_map_for_data(self,target):
		self.tile_map_for_data = target
		
	#get list of tiles currently colliding with the player
	def __get_colliding_tiles(self):
		colliding_tiles = list()
		for row in range(len(self.tile_map_for_collisions)):
			for column in range(len(self.tile_map_for_collisions[row])):
				current_tile = self.tile_map_for_collisions[row][column] 
				if(cl.AABB_2d_collide(self.position.x,self.position.y,self.image.get_width(),self.image.get_height(),
									current_tile.x,current_tile.y,current_tile.image.get_width(),current_tile.image.get_height())):
					colliding_tiles.append(current_tile)
		return colliding_tiles
	
	#resolves collisions with tiles
	def __resolve_collisions(self):
		old_pos = vector2.vector2(self.position.x,self.position.y)
		old_speed = vector2.vector2(self.speed.x,self.speed.y)
		
		for tiles in self.__get_colliding_tiles():
			if tiles.collidable:
				depth = cl.AABB_intersection_depth(self.position.x,self.position.y,self.image.get_width(),self.image.get_height(),
											tiles.x,tiles.y,tiles.image.get_width(),tiles.image.get_height())
				if(fabs(depth.x) > 0.05 or fabs(depth.y) > 0.05):
					absDepthX = fabs(depth.x)
					absDepthY = fabs(depth.y)
					if(absDepthY < absDepthX):
						self.position = vector2.vector2(self.position.x,self.position.y + depth.y)
					else:
						#if under your feet
						if fabs(tiles.y - (self.position.y + self.image.get_height() - self.speed.y)) < 0.05:
							#if depth.x > 0.05 or tiles.y > self.position.y + self.image.get_height():
							None
						#not under your feet
						else:
							self.position = vector2.vector2(self.position.x + depth.x, self.position.y)
		
		if(fabs(old_pos.x - self.position.x) > 0.05):
			#print "stopped x because resolved %f" % (old_pos.x - self.position.x)
			self.speed.x = 0
			self.acceleration.x = 0
		if(fabs(old_pos.y - self.position.y) > 0.05):
			self.speed.y = 0
		if(old_speed.y > 0 and fabs(self.speed.y) < 0.05 and self.in_air):
			self.__on_hit_floor()
			
	#restarts the level
	def restart_level(self):
		print "respawning at %f %f" % (self.tile_map_for_data.spawnpos.x,self.tile_map_for_data.spawnpos.y)
		self.position = vector2.vector2(self.tile_map_for_data.spawnpos.x,self.tile_map_for_data.spawnpos.y)
		bullet.bullet_list = list()
		self.bullet_ammo = self.bullet_reload_ammo
		self.bullet_reload_time = 0
		enemy.spawn_enemies(self.tile_map_for_data)
					
	#detects character collision with bullets
	def is_hit_by_bullet(self):
		for bullets in bullet.bullet_list:
			if cl.AABB_2d_collide(self.position.x, self.position.y, self.image.get_width(), self.image.get_height(), 
			bullets.position.x, bullets.position.y, bullets.image.get_width(), bullets.image.get_height()):
				self.restart_level()
				break
	
	def handle_enemy_collisions(self):
		for enemies in enemy.enemy_list:
			if(cl.AABB_2d_collide(self.position.x,self.position.y,self.image.get_width(),self.image.get_height(),
								enemies.position.x,enemies.position.y,enemies.image.get_width(),enemies.image.get_height())):
				self.restart_level()
				break
						
	#dtime is in seconds, this updates the character's position based on time passed
	def update(self, dtime):
		self.__update_x_acceleration()
		self.__update_x_pos_and_speed(dtime)	
		self.__update_y_pos_speed_acceleration(dtime)
		
		self.__resolve_collisions()
		
		self.__update_animation()
		self.__update_bullet(dtime)
		
		self.is_hit_by_bullet()
		self.handle_enemy_collisions()
		
	#draws the character
	def draw(self, screen):
		needs_to_be_flipped = (self.direction == -1)
		transformed_image = pygame.transform.flip(self.image, needs_to_be_flipped, 0)
		screen.blit(transformed_image, pygame.Rect(self.position.x,self.position.y,0,0))
		
	#handles keys pressed down
	def handle_key_down(self, key):
		
		if (key == pygame.K_RIGHT):
			self.__is_key_down_right = True
			if (not self.__is_in_air()):
				self.image = self.run
			
			self.direction = 1
			self.acceleration.x = self.movement_acceleration
		elif (key == pygame.K_LEFT):
			self.__is_key_down_left = True
			if (not self.__is_in_air()):
				self.image = self.run

			self.direction = -1
			self.acceleration.x = -self.movement_acceleration
		elif (key == pygame.K_z):
			if (self.jumps_allowed > 0):
				self.in_air = True
				self.image = self.jump
				self.speed.y = -self.jump_speed
				self.jumps_allowed -= 1
		elif key == pygame.K_r:
			self.restart_level()			
		elif (key == pygame.K_x):
			self.__shoot_bullet()
		elif (key == pygame.K_c):
			self.bullet_reload_time = self.bullet_reload_max
			print self.bullet_reload_time
			
	#handles key release
	def handle_key_up(self, key):
		if (key == pygame.K_RIGHT):
			self.__is_key_down_right = False
			if (self.direction is 1):
				if (not self.__is_in_air()):
					self.image = self.idle
				
		elif (key == pygame.K_LEFT):
			self.__is_key_down_left = False
			if (self.direction is -1):
				if (not self.__is_in_air()):
					self.image = self.idle

	#shoots a bullet from the player
	def __shoot_bullet(self):
		bullet_offset = 10
		if ((self.bullet_ammo > 0) and (self.bullet_reload_time is 0)):
			new_bullet_position = vector2.vector2(self.position.x - bullet_offset,self.position.y + self.image.get_height()/2)
			print ("spawned bullet at %d %d") % (new_bullet_position.x, new_bullet_position.y)
			#if player facing right, offset bullet spawn position to his right side
			if(self.direction == 1):
				new_bullet_position.x += self.image.get_width() + 2*bullet_offset
				
			self.bullet_ammo -= 1
		
			#spawn bullet at new_bullet_position with speed left or right depending on facing direction	
			bullet.bullet_list.append(bullet.bullet(new_bullet_position.x,new_bullet_position.y,bullet.bullet_speed * self.direction,0))
