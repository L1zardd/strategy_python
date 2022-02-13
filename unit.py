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
	spritefile = "assets/img/units/RobotGruntSmall.png"
	sprite=''
	
	hp=100
	max_hp=100
	armor=5
	shooting_radius=128
	shooting_speed=50 # ~1 в секунду
	speed=3
	
	
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.sprite=pygame.image.load(self.spritefile)
		#self.sprite=pygame.transform.scale(self.sprite,(32,32))
		
	def draw(self):
		self.window.blit(self.sprite,(self.x,self.y))
	
class InfantryRobot(ShootingUnit):
     spritefile="assets/img/units/RobotInfantrySmall.png"
     sprite=''

     hp=100
     max_hp=100
     armor=10
     shooting_speed=150
     shooting_radius=160
     speed=5


     def __init__(self,window,x,y):
         super().__init__(window,x,y)
         self.sprite=pygame.image.load(self.spritefile)
         self.sprite=pygame.transform.scale(self.sprite,(32,32))

     def draw(self):
         self.window.blit(self.sprite,(self.x,self.y) )

class SniperRobot(ShootingUnit):
    spritefile = "assets/img/units/RobotSniperSmall.png"
    sprite=' '
    hp=100
    max_hp=100
    armor=5
    shooting_radius=1280
    shooting_speed=250 
    speed=2
    
    def __init__(self,window,x,y):
        super().__init__(window,x,y)
        self.sprite=pygame.image.load(self.spritefile)
        #self.sprite=pygame.transform.scale(self.sprite,(32,32))

    def draw(self):
        self.window.blit(self.sprite,(self.x,self.y))

class RPGRobot(ShootingUnit):
    spritefile = "assets/img/units/RobotRPGSmall.png"
    sprite = ''

    hp = 150
    max_hp = 150
    armor = 15
    shooting_radius = 350
    shooting_speed = 17  # ~1 в 3секунды
    speed = 3

    def __init__(self, window, x, y):
        super().__init__(window, x, y)
        self.sprite = pygame.image.load(self.spritefile)
        #self.sprite = pygame.transform.scale(self.sprite, (32, 32))

    def draw(self):
        self.window.blit(self.sprite, (self.x, self.y))
	
class LightVenicle(ShootingUnit):
    spritefile = "assets/img/units/LightVenicleSmall.png"
    sprite=''
    hp=130
    max_hp=130
    armor=5
    shooting_radius=128
    shooting_speed=80 # ~1 в секунду
    speed=9

    def __init__(self,window,x,y):
        super().__init__(window,x,y)
        self.sprite=pygame.image.load(self.spritefile)
        #self.sprite=pygame.transform.scale(self.sprite,(32,32))

    def draw(self):
        self.window.blit(self.sprite,(self.x,self.y))
	
class TankVenicle(ShootingUnit):
    
    spritefile = "assets/img/units/TankVenicleSmall.png"
    sprite=''
    
    hp=700
    max_hp=700
    armor=10
    shooting_radius=256
    shooting_speed=125 # ~1 раз в 2.5 секунды
    speed=5
    
    def __init__(self, window, x, y):
        super().__init__(window, x ,y)
        self.sprite=pygame.image.load(self.spritefile)
        #self.sprite=pygame.transform.scale(self.sprite, (128,64))

    
    def draw(self):
        self.window.blit(self.sprite,(self.x,self.y))
	
class DevastatorVenicle(ShootingUnit):
    spritefile = "assets/img/units/DevastatorSmall.png"
    sprite=''

    hp=500
    max_hp=500
    armor=15
    shooting_radius=128
    shooting_speed=10 # ~1 в секунду
    speed=1
    def __init__(self,window,x,y):
        super().__init__(window,x,y)
        self.sprite=pygame.image.load(self.spritefile)
        #self.sprite=pygame.transform.scale(self.sprite,(32,32))

    def draw(self):
        self.window.blit(self.sprite,(self.x,self.y))

				
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
	spritefile="./assets/img/buildings/building1.png"
	production_speed=120
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.production_speed=220
	
	def produce_units(self):
		unit = GruntRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		self.units.append(unit)
	


class InfantryFactory(Building):
	pass #Matthew		

class SniperFactory(Building):
	spritefile="./assets/img/buildings/sniper_factory.png"
	production_speed=380
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.production_speed=380
	
	def produce_units(self):
		print("Sniper factory pr speed", self.production_speed)
		unit = SniperRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		self.units.append(unit)
	
class RPGFactory(Building):
	production_speed=580
	spritefile="./assets/img/buildings/RPG_factory.png"
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.production_speed=580

	def produce_units(self):
		print("RPG factory pr speed", self.production_speed)
		unit = RPGRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		self.units.append(unit)	
	
class LightVenicleFactory(Building):
	pass #Alexei	
