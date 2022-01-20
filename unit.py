import pygame,random, math

class Entity:
    x=0
    y=0
    w=50
    h=50    
    color=(0,120,0)
    window=0
    
    def draw(self):
        pygame.draw.rect(self.window,self.color,(int(self.x),int(self.y),self.w,self.h))

    def __init__(self,window,x,y):
        self.x=x
        self.y=y
        self.window=window


class Unit(Entity):
	x=0
	y=0
	w=20
	h=20
	color=(0,120,0)
	dest = 0, 0
	speed=5
	speed_x=0
	speed_y=0
	state="idle"
	window=0

	def set_destination_point(self,pos):
		self.dest=pos
		X=abs(self.dest[0]-self.x)
		Y=abs(self.dest[1]-self.y)
		L=math.sqrt(X*X+Y*Y)
		if L!=0:
			sin_a=Y/L
			cos_a=X/L
			self.speed_x=self.speed*cos_a
			self.speed_y=self.speed*sin_a
		else:
			self.speed_x=1
			self.speed_y=1
		
	def go_to_dest(self):
		if abs(self.x-self.dest[0])<self.speed_x:
			self.x=self.dest[0]
			self.state="idle"
		else:
			if self.x<self.dest[0]:
				self.x+=self.speed_x
			else:
				self.x-=self.speed_x
				
		if abs(self.y-self.dest[1])<self.speed_y:
			self.y=self.dest[1]
			self.state="idle"
		else:
			if self.y<self.dest[1]:
				self.y+=self.speed_y
			else:
				self.y-=self.speed_y
	
	def ai(self):
		if self.state=="idle":
			pass
		if self.state=="move":
			self.go_to_dest()
	
class Building(Entity):

    def __init__(self):
        self.w=300
        self.h=300
        self.color=(180,120,0)
        self.production_speed=100
        self.production=0

    def produce_units(self):
        unit = Unit()
        unit.x=self.x+self.w+10
        unit.y=self.y+self.h+10
        unit.dest=(unit.x+random.randint(0,500),unit.y+random.randint(0,500))
        unit.state='move'
        units.append(unit)

    def ai(self):
        self.production+=1
        if self.production>=self.production_speed:
            self.production=0
            self.produce_units()