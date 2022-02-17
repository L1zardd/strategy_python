import pygame,random, math

#базовый класс
#для всего, что отрисовано на экране
#кроме карты 
class Entity:
	#координаты
	x=0
	y=0
	#размеры
	w=50
	h=50    
	#цвет
	color=(0,120,0)
	#цвет_выбранного
	sel_color=(100,120,0)
	#окно, в котором будем отрисовывать объект
	window=0    
	#выбран - не выбран
	selected=False
	#игрок
	player=1
	
	#отрисовка объекта 
	def draw(self):
		#если выбрана
		if self.selected:
			#одним цветом
			pygame.draw.rect(self.window,self.sel_color,(int(self.x),int(self.y),self.w,self.h))
		else:
			#иначе - другим
			pygame.draw.rect(self.window,self.color,(int(self.x),int(self.y),self.w,self.h))

	#конструктор
	def __init__(self,window,x,y):
		#указываем координаты
		self.x=x
		self.y=y
		#и окно для отрисовки
		self.window=window
	
	#измерение дистанции от этого объекта до объекта obj
	def distance(self,obj):
		#по теореме Пифагора
		x=abs(self.x-obj.x)
		y=abs(self.y-obj.y)
		#вычислим гипотенузу - расстояние меж объектами
		d=math.hypot(x,y)		
		return d

#класс Юнит, унаследованный от Сущности
#умеет бегать
class Unit(Entity):	
	#точка назначения (в которую юнит движется)
	dest = 0, 0
	#и точка отправления
	start = 0, 0
	#скорость
	speed=5
	#скорости по осям
	speed_x=0
	speed_y=0
	#состояние юнита
	state="idle"

	#указываем точку назначения юнита
	def set_destination_point(self,pos):
		#двигается в то место, которое передали в pos
		self.dest=pos
		#Вычисляем скорости по осям x и y
		#По теореме Пифагора
		X=abs(self.dest[0]-self.x)
		Y=abs(self.dest[1]-self.y)
		L=math.hypot(X,Y)
		if L!=0:
			#Вычисляем синусы для большого треугольника (между точкой старта и назначения)
			sin_a=Y/L
			cos_a=X/L
			#и Вычисляем скорости по осям x и y
			self.speed_x=self.speed*cos_a
			self.speed_y=self.speed*sin_a
		else:
			self.speed_x=1
			self.speed_y=1
	
	#Один шаг в указанную точку
	def go_to_dest(self):
		#Если уже дошел до точки
		if abs(self.x-self.dest[0])<self.speed_x:
			#Помещаем его в конечную точку
			self.x=self.dest[0]
			#Останавливаем - больше не двигается
			if self.state=="move":
				self.state="idle"
			#Если патрулировал - побежал обратно
			if self.state=="patrol":
				self.dest,self.start=self.start,self.dest
		else:
			#Если еще не дошел до конца
			if self.x<self.dest[0]:
				#Двигаем на шаг, равный speed_x в нужную сторону
				self.x+=self.speed_x
			else:
				self.x-=self.speed_x
		#То же самое по y
		if abs(self.y-self.dest[1])<self.speed_y:
			self.y=self.dest[1]
			if self.state=="move":
				self.state="idle"
			if self.state=="patrol":
				self.dest,self.start=self.start,self.dest
		else:
			if self.y<self.dest[1]:
				self.y+=self.speed_y
			else:
				self.y-=self.speed_y
				
	#Искусственный интеллект
	def ai(self):
		#Если стоим
		if self.state=="idle":
			#стоим и ничего не делаем
			pass
		#Если двигаемся
		if self.state=="move":
			#делаем шаг в точку назначения
			self.go_to_dest()
		#Если патрулируем
		if self.state=="patrol":
			#делаем шаг в точку назначения
			self.go_to_dest()
	
	
class ShootingUnit(Unit):
	#Цель стрельбы
	target=None
	#Хитпойнты
	hp=100
	max_hp=100
	#дистанция стрельбы
	shooting_radius=50
	#скорость перезарядки
	shooting_speed=50
	#счетчик для стрельбы
	shooting=0 
	
	#Броня
	armor=5
	
	#Пули	
	bullets=[]
	
	#настройка цели
	def set_target(self,target):
		self.target=target
		
	#создаем снаряд
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
			#если стреляем
		if self.state=="shoot":
			#если есть цель стрельбы
			if self.target!=None:
				#и она жива
				if self.target.hp>=0:
					#счетчик перезарядки возрастает на единицу
					self.shooting+=1
					#если дошел до порогового значения
					if self.shooting>=self.shooting_speed:
						#создаем пулю
						self.bullets.append(self.shoot())
						self.shooting=0
				else:
					#если цели нет - останавливаем юнит
					self.target=None
					self.state="idle"
	#получение урона			
	def get_damage(self,dmg):
		#поправка на броню - случайная
		a=random.randint(0,self.armor)
		#поправку вычитаем
		dmg=dmg-a
		if dmg<0:
			dmg=0
		#уменьшаем здоровье
		self.hp-=dmg
			

		
class Bullet(Unit):
	target=None
	speed=20
	state="move"
	damage=10
	
	color=(200,200,200)
	
		
	def draw(self):
		#рисуем круг
		pygame.draw.circle(self.window,self.color,(int(self.x),int(self.y)),2)
		
	def ai(self):
		#если цель есть
		if self.target!=None:
			#двигаемся к цели
			self.set_destination_point((self.target.x,self.target.y))
			self.go_to_dest()
			#если до цели долетели
			if self.state=="idle":
				#наносим урон
				self.target.get_damage(self.damage)
		else:
			self.state="idle"

class LaserRay(Bullet):
	
	color=(200,50,50)
	damage=30
	
	def draw(self):
		pygame.draw.line(self.window,self.color,(int(self.x),int(self.y)),(int(self.target.x),int(self.target.y)),3)

class GruntRobot(ShootingUnit):
	spritefile = "assets/img/units/RobotGruntSmall.png"
	sprite=''
	
	hp=50
	max_hp=50
	armor=1
	shooting_radius=50
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
	 armor=7
	 shooting_speed=150
	 shooting_radius=100
	 speed=5


	 def __init__(self,window,x,y):
		 super().__init__(window,x,y)
		 self.sprite=pygame.image.load(self.spritefile)
		 #self.sprite=pygame.transform.scale(self.sprite,(32,32))

	 def draw(self):
		 self.window.blit(self.sprite,(self.x,self.y) )

class SniperRobot(ShootingUnit):
	spritefile = "assets/img/units/RobotSniperSmall.png"
	sprite=' '
	hp=80
	max_hp=80
	armor=5
	shooting=249
	shooting_radius=280
	shooting_speed=250 
	speed=2
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.sprite=pygame.image.load(self.spritefile)
		#self.sprite=pygame.transform.scale(self.sprite,(32,32))

	def draw(self):
		self.window.blit(self.sprite,(self.x,self.y))
		
	def shoot(self):
		bullet=LaserRay(self.window,self.x,self.y)
		bullet.target=self.target
		return bullet

class RPGRobot(ShootingUnit):
	spritefile = "assets/img/units/RobotRPGSmall.png"
	sprite = ''

	hp = 150
	max_hp = 150
	armor = 15
	shooting_radius = 140
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
	#игрок, которому принадлежит знамя
	player=0
	spritefile="./assets/img/misc/banner_{}.png".format(player)
	#время на захват флага
	capture_time=200
	#счетчик захвата флага
	capture=0
	#захватывающий в данный момент игрок
	capture_player=0
	connected_factory=None
	
	def __init__(self,window,x,y):
		self.window=window
		self.x=x
		self.y=y
		self.sprite=pygame.image.load(self.spritefile)
	
	def draw(self):
		self.window.blit(self.sprite, (self.x,self.y))
		if self.capture!=0:
			pygame.draw.rect(self.window,(200,200,200),(self.x,self.y-5,64,4))
			#шкала прогресса захвата
			pygame.draw.rect(self.window,(50,200,50),(self.x,self.y-4,math.floor((self.capture/self.capture_time)*64),2))
		
	#один шаг захвата знамени
	def capture_banner(self,player):
		self.capture_player=player
		self.capture+=1
		if self.capture>=self.capture_time:
			self.change_player(player)
			self.capture=0
		
	
	def change_player(self,player):
		self.player=player		
		#заново выбирает файл спрайта
		self.spritefile="./assets/img/misc/banner_{}.png".format(player)
		#и перезагружает его
		self.sprite=pygame.image.load(self.spritefile)
		self.connected_factory.player=player
	
#базовое строение
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
		unit.player=self.player
		self.units.append(unit)

	def ai(self):
		if self.player!=0:
			self.production+=1
			if self.production>=self.production_speed:
				self.production=0
				self.produce_units()
	
	def draw(self):
		self.window.blit(self.sprite, (self.x,self.y))
		pygame.draw.rect(self.window,(200,200,200),(self.x,self.y-5,self.w,4))
		pygame.draw.rect(self.window,(50,200,50),(self.x,self.y-4,math.floor((self.production/self.production_speed)*self.w),2))
		
		'''TO DO
		1.Точка назначения юнитов
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
		unit.player=self.player
		self.units.append(unit)
	


class InfantryFactory(Building):
	spritefile="./assets/img/buildings/infantry_factory.png"
	production_speed=280
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.production_speed=380
	
	def produce_units(self):		
		unit = InfantryRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		unit.player=self.player
		self.units.append(unit)	

class SniperFactory(Building):
	spritefile="./assets/img/buildings/sniper_factory.png"
	production_speed=380
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.production_speed=380
	
	def produce_units(self):		
		unit = SniperRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		unit.player=self.player
		self.units.append(unit)
	
class RPGFactory(Building):
	production_speed=480
	spritefile="./assets/img/buildings/RPG_factory.png"
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.production_speed=580

	def produce_units(self):
		unit = RPGRobot(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		unit.player=self.player
		self.units.append(unit)	
	
class LightVenicleFactory(Building):
	production_speed=1000
	spritefile="./assets/img/buildings/light_venicle_factory.png"
	
	def __init__(self,window,x,y):
		super().__init__(window,x,y)
		self.production_speed=580

	def produce_units(self):
		unit = LightVenicle(self.window,self.x+self.w//2+10,self.y+self.h+10)
		unit.dest=unit.x,unit.y+30
		unit.state='move'
		unit.player=self.player
		self.units.append(unit)		
