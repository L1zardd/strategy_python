import pygame
import random, math

pygame.init()

window=pygame.display.set_mode((1200,800),pygame.RESIZABLE)

class Unit:
	x=0
	y=0
	w=50
	h=50
	speed=25
	speed_x=0
	speed_y=0
	color=(0,120,0)
	dest=0,0
	state="idle"
	
	def draw(self):
		pygame.draw.rect(window,self.color,(int(self.x),int(self.y),self.w,self.h))
		
	def set_destination_point(self,x,y):
		self.dest=x,y
		X=abs(self.x-x)
		Y=abs(self.y-y)
		L=math.sqrt(X**2+Y**2)
		if L!=0:
			sin_alpha=Y/L
			cos_alpha=X/L
			self.speed_y=self.speed*sin_alpha
			self.speed_x=self.speed*cos_alpha
		else:
			self.dest=self.x,self.y
			self.speed_x=0.5
			self.speed_y=0.5
	
	def move_to_dest(self):
		if abs(self.dest[0]-self.x)<self.speed_x:
			self.x=self.dest[0]
			self.state="idle"
		else:
			if self.dest[0]>self.x:
				self.x+=self.speed_x
			else:
				self.x-=self.speed_x
		if abs(self.dest[1]-self.y)<self.speed_y:
			self.y=self.dest[1]
			self.state="idle"
		else:
			if self.dest[1]>self.y:
				self.y+=self.speed_y
			else:
				self.y-=self.speed_y
				
	def ai(self):
		if self.state=="idle":
			pass
		if self.state=="move":
			self.move_to_dest()
		
unit = Unit()
unit.x=600
unit.y=400

while True:
	for event in pygame.event.get():

		if event.type==pygame.QUIT:
			exit()
		if event.type==pygame.MOUSEBUTTONDOWN:
			print(event)
			unit.set_destination_point(event.pos[0],event.pos[1])
			unit.state="move"
	window.fill((120,120,250))
	unit.draw()
	unit.ai()
	pygame.display.update()
	pygame.time.delay(20)
