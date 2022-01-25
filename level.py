import pygame
import random,math

class Tile:
	x=600
	y=400
	w=64
	h=64
	color=[0,255,0]
	window=None
	rect=0,0,64,64
	
	def draw(self):
		pygame.draw.rect(self.window,self.color,(int(self.x),int(self.y),self.w,self.h))
	

class Map:
	level=[]
	w=0
	h=0
	window=None
	tilemap_file='daLandSnow.png'
	tilemap=None
	
	def __init__(self,window,w,h):
		self.window=window
		self.create_random_map(w,h)
		self.tilemap=pygame.image.load(self.tilemap_file)
		
	
	def create_random_map(self,w,h):
		for i in range(h):
			row=[]
			for j in range(w):
				tile = Tile()
				tile.window=self.window
				tile.x=j*tile.w
				tile.y=i*tile.h
				tile.color=[0,random.randint(1,255),0]
				tile.rect=tile.x,tile.y,tile.w,tile.h
				row.append(tile)
			self.level.append(row)
			
	def draw(self):
		for row in self.level:
			for tile in row:
				self.window.blit(self.tilemap,tile.rect)
	
	
