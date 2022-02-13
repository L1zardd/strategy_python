#импорт необходимых библиотек
import pygame,random, math
#импорт классов из других файлов
from unit import *
from interface import Frame, in_frame
from level import Tile, Map
#главное окно программы
window = pygame.display.set_mode((1200,800),pygame.RESIZABLE)
	
#переменная, указывающая на исполнение программы
run=True

#списки юнитов и строений в игре
#все юниты попадают в этот список
units=[]
#все строения попадают в этот список
buildings=[]
#пули и снаряды
bullets=[]

#Карта (задний фон)
map1=Map(window,10,10)

#флаг для захвата
banner1=Banner(window,600,400)

#создание строений
building=GruntFactory(window,10,120)
building.units=units
buildings.append(building)

building=SniperFactory(window,410,120)
building.units=units
buildings.append(building)

building=RPGFactory(window,810,520)
building.units=units
buildings.append(building)


#рамка для выделения юнитов
frame=Frame(window,0,0)


#главный цикл программы
while run:
	#ОЧЕРЕДЬ СОБЫТИЙ
	#проверяются события
	for event in pygame.event.get():
		#выход из приложения
		if event.type == pygame.QUIT:
			run=False
		#если нажата кнопка мыши
		if event.type == pygame.MOUSEBUTTONDOWN:
			#если левая - выбранные юниты перемещаются в точку назначения
			if event.button == 1:
				for un in units:
					#Если юнит выбран
					if un.selected == True:
						#Идет в щелкнутую точку
						un.set_destination_point((event.pos[0],event.pos[1]))
						un.state="move"
			#если средняя - выбор юнитов
			elif event.button == 2:
				get_unit=False
				#выбор юнита, попавшего на курсор
				for un in units:
					if abs(un.x-event.pos[0])<un.w and abs(un.y-event.pos[1])<un.h:
						if un.selected == False:
							un.selected=True
						else:
							un.selected=False
						get_unit=True
				#выбор юнитов с помощью рамки
				if not get_unit:
					frame.x,frame.y=event.pos
					frame.h,frame.w=0,0
				
			#если правая - создание юнитов
			#Для тестовых целей, отключим потом 
			elif event.button == 3:
				units.append(Unit(window,event.pos[0],event.pos[1]))
				#юнит игрока №2
				units[-1].player=2
				units[-1].selected=False
		#если мышь движется
		if event.type==pygame.MOUSEMOTION:
			#И зажата средняя кнопка
			if event.buttons==(0,1,0):
				#Рисуем рамку
				frame.h=event.pos[1]-frame.y
				frame.w=event.pos[0]-frame.x
				#Все юниты
				for un in units:
					#попавшие в рамку
					if in_frame(frame,un):
						#выделяются
						un.selected=True
					else:
						un.selected=False
		#Отпустили мышь
		if event.type ==pygame.MOUSEBUTTONUP:
			if event.button==2:
				#Убрали рамку
				frame.x=-10
				frame.y=-10
				frame.h=0
				frame.w=0
	
	#ОТРИСОВКА
	#одноцветный фон
	window.fill((120,120,220))
	#Карта
	map1.draw()
	#Строения 
	for building in buildings:
		#отрисовываются
		building.draw()
		#производство юнитов
		building.ai()
	#Флаг
	#отрисовывается
	banner1.draw()
	
	#юниты
	for unit in units:
		#отрисовываются
		unit.draw()
		#выполняют действия
		unit.ai()
		#если расстояние до флага меньше порогового
		if banner1.distance(unit)<150:
			#если юнит другого игрока
			if banner1.capture_player!=unit.player:
				#захват флага сбрасывается
				banner1.capture=0
			#идет процесс захвата флага
			banner1.capture_banner(unit.player)
			
			
		#стрельба (переписать)
		if type(unit)==ShootingUnit:
			bullets+=unit.bullets
			if unit.hp<=0:
				units.remove(unit)
				del unit
	
	#перебираем пули
	for bullet in bullets:
		#если пуля двигается
		if bullet.state=="move":
			#отрисовывается
			bullet.draw()
			#и двигается дальше
			bullet.ai()
		else:
			#если попала - убирается
			bullets.remove(bullet)
			del bullet
	
	
	#отрисовка рамки
	frame.draw()
	
	#обновить экран
	pygame.display.update()
	#и ждать 20 миллисекунд
	pygame.time.delay(20)
