import pygame,random, math

class Entity:
	x=0
	y=0
	w=50
	h=50    
	color=(0,120,0)
	sel_color=(100,120,0)
	window=0    
	selected=True
	player=1
	
	def draw(self):
		if self.selected:
			pygame.draw.rect(self.window,self.sel_color,(int(self.x),int(self.y),self.w,self.h))
		else:
			pygame.draw.rect(self.window,self.color,(int(self.x),int(self.y),self.w,self.h))

	def __init__(self,window,x,y):
		self.x=x
		self.y=y
		self.window=window
		
	def distance(self,obj):
		x=abs(self.x-obj.x)
		y=abs(self.y-obj.y)
		d=math.hypot(x,y)
		print(d)
		return d


class Unit(Entity):
	x=0
	y=0
	w=20
	h=20
	color=(0,120,0)
	dest = 0, 0
	start = 0, 0
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
			if self.state=="move":
				self.state="idle"
			if self.state=="patrol":
				print("changed!")
				self.dest,self.start=self.start,self.dest
		else:
			if self.x<self.dest[0]:
				self.x+=self.speed_x
			else:
				self.x-=self.speed_x
				
		if abs(self.y-self.dest[1])<self.speed_y:
			self.y=self.dest[1]
			if self.state=="move":
				self.state="idle"
			if self.state=="patrol":
				print("changed!")
				self.dest,self.start=self.start,self.dest
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
		
		if self.state=="patrol":
			self.go_to_dest()
	
	
class ShootingUnit(Unit):
	target=None
	
	hp=100
	max_hp=100
	
	
	armor=5
	
	color=(200,120,200)
	sel_color=(200,120,100)
	
	bullets=[]
	
	def set_target(self,target):
		self.target=target
		
	
	def shoot(self):
		bullet=Bullet(self.window,self.x,self.y)
		bullet.target=self.target
		return bullet
		
	def ai(self):
		if self.state=="idle":
			pass
		if self.state=="move":
			self.go_to_dest()
		
		if self.state=="patrol":
			self.go_to_dest()
			
		if self.state=="shoot":
			if self.target!=None:
				self.bullets.append(self.shoot())
				
	def get_damage(self,dmg):
		self.hp-=dmg
			

		
class Bullet(Unit):
	target=None
	speed=20
	state="move"
	damage=10
	
	color=(200,200,200)
	
		
	def draw(self):
		pygame.draw.circle(self.window,self.color,(int(self.x),int(self.y)),2)
		
	def ai(self):
		if self.target!=None:
			self.set_destination_point((self.target.x,self.target.y))
			self.go_to_dest()
			if self.state=="idle":
				self.target.get_damage(self.damage)
		else:
			self.state="idle"

class GruntRobot(Unit):
	pass
	
class InfantryRobot(ShootingUnit):
	pass

class SniperRobot(ShootingUnit):
	pass
	
class RPGRobot(ShootingUnit):
	pass
	
class LightVenicle(ShootingUnit):
	pass
	
class TankVenicle(ShootingUnit):
	pass
	
class DevastatorVenicle(ShootingUnit):
	pass

				
class Banner(Entity):
	player=0
	spritefile="./assets/img/misc/banner_{}.png".format(player)
	capture_time=200
	capture=0
	capture_player=0
	
	def __init__(self,window,x,y):
		self.window=window
		self.x=x
		self.y=y
		self.sprite=pygame.image.load(self.spritefile)
	
	def draw(self):
		self.window.blit(self.sprite, (self.x,self.y))
		if self.capture!=0:
			pygame.draw.rect(self.window,(200,200,200),(self.x,self.y-5,64,4))
			pygame.draw.rect(self.window,(50,200,50),(self.x,self.y-4,math.floor((self.capture/self.capture_time)*64),2))
		
	def capture_banner(self,player):
		self.capture_player=player
		self.capture+=1
		if self.capture>=self.capture_time:
			self.change_player(player)
			self.capture=0
		
	
	def change_player(self,player):
		self.player=player
		print("player=",player)
		self.spritefile="./assets/img/misc/banner_{}.png".format(player)
		self.sprite=pygame.image.load(self.spritefile)
	
	#TO DO
	#сделать время захвата флага
	#сделать индикатор захвата флага

class Building(Entity):
	
	units=[]
	spritefile="building.png"

	def __init__(self,window,x,y):
		self.window=window
		self.w=128
		self.h=128
		self.x=x
		self.y=y
		self.color=(180,120,0)
		self.production_speed=100
		self.production=0
		self.sprite=pygame.image.load(self.spritefile)

	def produce_units(self):
		unit = Unit(self.window,self.x+self.w+10,self.y+self.h+10)
		unit.dest=(unit.x+random.randint(0,500),unit.y+random.randint(0,500))
		unit.state='move'
		self.units.append(unit)

	def ai(self):
		self.production+=1
		if self.production>=self.production_speed:
			self.production=0
			self.produce_units()
	
	def draw(self):
		self.window.blit(self.sprite, (self.x,self.y))
		pygame.draw.rect(self.window,(200,200,200),(self.x,self.y-5,self.w,4))
		pygame.draw.rect(self.window,(50,200,50),(self.x,self.y-4,math.floor((self.production/self.production_speed)*self.w),2))
		
		'''TO DO
		1.Анимация
		2.Шкала производства
		3.Точка назначения юнитов
		'''

class GruntFactory(Building):
	spritefile="building1.png"
	production_speed=120
	
	def produce_units(self):
		unit = GruntRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		self.units.append(unit)
	


class InfantryFactory(Building):
	pass #Matthew		

class SniperFactory(Building):
	spritefile="./assets/img/buildings/sniper_factory.png"
	production_speed=180
	
	def produce_units(self):
		unit = SniperRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		self.units.append(unit)
	
class RPGFactory(Building):
	production_speed=180
	spritefile="./assets/img/buildings/RPG_factory.png"

	def produce_units(self):
		unit = RPGRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		self.units.append(unit)	
	
class LightVenicleFactory(Building):
	pass #Alexei	
