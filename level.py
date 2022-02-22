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
	sprite=None
	
	def draw(self):
		pygame.draw.rect(self.window,self.color,(int(self.x),int(self.y),self.w,self.h))
	

class Map:
	#Массив, хранящий уровень
	level=[]
	#ширина и высота в клетках
	w=0
	h=0
	#окно отрисовки
	window=None
	#файл с тайлами
	tilemap_file='assets/img/tiles/daLandSnow.png'
	tilemap=None
	
	def __init__(self,window,w,h):
		self.window=window		
		self.tilemap=pygame.image.load(self.tilemap_file)
		#self.create_random_map(w,h)

		
	
	def create_random_map(self,w,h):
		for i in range(h):
			row=[]
			for j in range(w):
				tile = Tile()
				tile.window=self.window
				tile.x=j*tile.w
				tile.y=i*tile.h
				tile.color=[0,0,180]
				tile.rect=tile.x,tile.y,tile.w,tile.h
				tile.sprite=self.tilemap.subsurface(0*64,37*64,64,64)
				row.append(tile)
			self.level.append(row)
	
	
	def open_level_file(self,filename):
		filelevel=open(filename)
		filetext=filelevel.readlines()
		print(filetext)
		self.h=len(filetext)
		self.w=len(filetext[0])
		print(self.w,self.h)
		for i,textrow in enumerate(filetext):
			
			row=[]
			for j,s in enumerate(textrow):
				if s.isdigit():				
					tile = Tile()
					tile.window=self.window
					print(i,j)
					tile.x=j*tile.w
					tile.y=i*tile.h
					tile.color=[0,0,180]
					tile.rect=tile.x,tile.y,tile.w,tile.h
					if s=='1':
						tile.sprite=self.tilemap.subsurface(0*64,37*64,64,64)					
					if s=='0':
						tile.sprite=self.tilemap.subsurface(0*64,36*64,64,64)
					if s=='2':
						tile.sprite=self.tilemap.subsurface(random.randint(0,9)*64,9*64,64,64)
					if s=='3':
						tile.sprite=self.tilemap.subsurface(random.randint(0,9)*64,10*64,64,64)
					if s=='4':
						tile.sprite=self.tilemap.subsurface(random.randint(0,9)*64,16*64,64,64)
					if s=='5':
						tile.sprite=self.tilemap.subsurface(random.randint(0,9)*64,6*64,64,64)
					if s=='6':
						tile.sprite=self.tilemap.subsurface(random.randint(0,9)*64,6*64,64,64)	
					row.append(tile)
			
			self.level.append(row)
			
	def draw(self):
		for row in self.level:
			for tile in row:
				#tile.draw()
				self.window.blit(tile.sprite,tile.rect)

	
