import pygame
import vector2

tile_size = 32

class tile:
	#create tile with image and name at world position x y added to space if it is defined
	def __init__(self,image,name,collidable=False,xpos=0,ypos=0):
		self.image = image
		self.name = name
		self.collidable = collidable
		self.x = xpos
		self.y = ypos

	#draw on screen
	def draw(self,screen):
		if(self.image != None):
			screen.blit(self.image,pygame.Rect(self.x,self.y,0,0))
		
#used to represent a 2d matrix of tiles based on a text file
class tilemap:
	def get_tile_list(self):
		return self.__tilemap
	
	def __init__(self):
		self.__tilemap = list()
		self.__tileset = dict()
		self.spawnpos = vector2.vector2(0,0)
		self.map_enemies = list()
		#no-op tile
		self.add_tile(None, '.')
	#add association of tile to image to dictionary. if space is None, will not be physical
	def add_tile(self,surface,name,collidable=False):
		self.__tileset[name] = tile(surface,name,collidable)
	
	#load map file into map 
	def load(self,filename):
		try:
			mapdata = open(filename + ".map","r").read()
			current_character = 0
			row = 0
			while current_character < len(mapdata):
				self.__tilemap.append([])
				while True:
					if current_character >= len(mapdata):
						break
					if mapdata[current_character] == '\n':
						break
					#prototype for the tile as predetermined in the tileset
					proto = self.__tileset[mapdata[current_character]]
					print "creating tile %s at %d %d" % (proto.name,len(self.__tilemap[row])*tile_size,row*tile_size)
					new_tile = tile(proto.image,proto.name,proto.collidable,len(self.__tilemap[row])*tile_size,row*tile_size)
					self.__tilemap[row].append(new_tile)
					current_character += 1
					
				current_character += 1
				row += 1
				
			mappointfile = open(filename + ".dat","r")
			if(mappointfile):
				mappointfile = mappointfile.read()
			mappointfile = mappointfile.split('\n')
			for row in range(len(mappointfile)):
				curr_line = mappointfile[row].split(" ")
				if(curr_line[0] == "spawn"):
					self.spawnpos = vector2.vector2(float(curr_line[1]),float(curr_line[2]))
				elif(curr_line[0] == "enemy"):
					self.map_enemies.append([curr_line[1],int(curr_line[2]),int(curr_line[3])])
		except:
			None
			#TODO: handle other types of tags
			
	#draw map on screen
	def draw(self,screen):
		for row in range(len(self.__tilemap)):
			for column in range(len(self.__tilemap[row])):
					self.__tilemap[row][column].draw(screen)

