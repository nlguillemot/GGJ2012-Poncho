import sys
import pygame

import character
import tilemap
import bullet
import gui
import enemy

#global constants
screen_dimensions = 640, 480

#initialize pygame library
pygame.init()

#set up the screen
screen = pygame.display.set_mode(screen_dimensions)
#set window title
pygame.display.set_caption("Poncho")

#create the gui overlay that gives info about the game to the player
gui_overlay = gui.gui()

#create kid and set default position
kid = character.character()

#hook up the player to the gui
gui_overlay.set_player(kid)

#convert image for bullet to screen format
bullet.bullet_image = bullet.bullet_image.convert_alpha()

#create a red tile for testing
red_tile = pygame.Surface((tilemap.tile_size,tilemap.tile_size))
red_tile.fill(0xFF0000)

#create a blue tile for testing
blue_tile = pygame.Surface((tilemap.tile_size,tilemap.tile_size))
blue_tile.fill(0xFFFFFF)

#load placeholder tile graphic 
placeholder_tile = pygame.image.load("placeholdertile.png").convert_alpha()
ground1_tile = pygame.image.load("ground1.png").convert_alpha()
grass1_tile = pygame.image.load("grass1.png").convert_alpha()
topsoil1_tile = pygame.image.load("topsoil1.png").convert_alpha()

pillar_tile_top = pygame.image.load("pillar_top.png").convert_alpha()
pillar_tile_middle = pygame.image.load("pillar_middle.png").convert_alpha()
pillar_tile_bottom = pygame.image.load("pillar_bottom.png").convert_alpha()
pillar_tile_one = pygame.image.load("pillar_one.png").convert_alpha()

#create set of tiles and set up associations between tile images and letters in the map file
background_tiles = tilemap.tilemap()
background_tiles.add_tile(red_tile,"R")
background_tiles.add_tile(blue_tile,"B")
background_tiles.add_tile(placeholder_tile,"P")
background_tiles.add_tile(ground1_tile,"G",True)
background_tiles.add_tile(topsoil1_tile,"m",True)
background_tiles.add_tile(pillar_tile_top,"T",True)
background_tiles.add_tile(pillar_tile_middle,"l",True)
background_tiles.add_tile(pillar_tile_bottom,"L",True)
background_tiles.add_tile(pillar_tile_one,"I",True)

foreground_tiles = tilemap.tilemap()
foreground_tiles.add_tile(grass1_tile,"f")

#load the map from a file
background_tiles.load("firstmap")
foreground_tiles.load("firstmapf")

kid.set_tile_map_for_collisions(background_tiles.get_tile_list())
kid.set_tile_map_for_data(background_tiles)

kid.restart_level()

#keep track of time
clock = pygame.time.Clock()
	
#main loop for game
while True:
	#handle events
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			kid.handle_key_down(event.key)
			if (event.key == pygame.K_ESCAPE):
				sys.exit()
		elif event.type == pygame.KEYUP:
			kid.handle_key_up(event.key)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			print "Clicked at %d,%d" % (event.pos[0],event.pos[1])
		#if you press the X button close the game
		elif event.type == pygame.QUIT:
			sys.exit()
	
	#get delta time of current frame
	lapse = clock.tick(60)
	#update bob's position
	kid.update(lapse/1000.0)
	#update bullet positions
	for bullets in bullet.bullet_list:
		bullets.update(lapse/1000.0)
	for enemies in enemy.enemy_list:
		enemies.update(lapse/1000.0)
	#clear the screen
	screen.fill(0x000000)
	#draw the tilemap
	background_tiles.draw(screen)
	#draw kid
	kid.draw(screen)
	#draw enemy1
	for enemies in enemy.enemy_list:
		enemies.draw(screen)
	#draw bullets
	for bullets in bullet.bullet_list:
		bullets.draw(screen)
	#draw foreground
	foreground_tiles.draw(screen)
	#draw the gui
	gui_overlay.draw(screen)
	#refresh the screen
	pygame.display.flip()
	
