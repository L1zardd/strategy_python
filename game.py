#импорт необходимых библиотек
import pygame,random, math
#импорт классов из других файлов
from unit import *
from interface import Frame
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
#флаги
banners=[]

#Карта (задний фон)
map1=Map(window,50,50)
map1.open_level_file("level.lvl")


#создание строений
building1=GruntFactory(window,10,120)
#всех юнитов, произведенных строением, приписывать к общему списку юнитов
building1.units=units
building1.player=1

building2=SniperFactory(window,410,120)
building2.units=units
building2.player=0

building3=RPGFactory(window,810,140)
building3.units=units
building3.player=0


building4=SniperFactory(window,410,520)
building4.units=units
building4.player=0


building5=RPGFactory(window,50,626)
building5.units=units
building5.player=0


building6=GruntFactory(window,900,620)
#всех юнитов, произведенных строением, приписывать к общему списку юнитов
building6.units=units
building6.player=2
#Строение добавлено в общий список строений


#флаг для захвата
banner1=Banner(window,200,200)
banner1.connected_factory=building1

banner1.change_player(1)
banners.append(banner1)

banner2=Banner(window,600,200)

banner2.connected_factory=building2
banners.append(banner2)


banner3=Banner(window,1000,200)
banners.append(banner3)
banner3.connected_factory=building3

banner4=Banner(window,600,600)
banners.append(banner4)
banner4.connected_factory=building4

banner5=Banner(window,200,600)
banners.append(banner5)
banner5.connected_factory=building5


banner6=Banner(window,1000,600)
banner6.connected_factory=building6
banner6.change_player(2)
banners.append(banner6)

buildings.append(building1)

buildings.append(building2)

buildings.append(building3)

buildings.append(building4)

buildings.append(building5)

buildings.append(building6)



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
					if un.selected == True and un.player==1:
						#Идет в щелкнутую точку
						un.set_destination_point((event.pos[0],event.pos[1]))
						un.state="move"
			#если правая - выбор юнитов
			elif event.button == 3:
				get_unit=False
				#выбор юнита, попавшего на курсор
				for un in units:
					if un.player==1:
						#если щелкнули в юнит
						if abs(un.x-event.pos[0])<un.w and abs(un.y-event.pos[1])<un.h:
							if un.selected == False:
								un.selected=True
							else:
								un.selected=False
							get_unit=True
				#выбор юнитов с помощью рамки
				#если щелкнули на свободное место - создаем в этом месте рамку
				if not get_unit:
					frame.x,frame.y=event.pos
					frame.h,frame.w=0,0
				
			#если средняя - создание юнитов
			#Для тестовых целей, отключим потом 
			elif event.button == 2:
				units.append(GruntRobot(window,event.pos[0],event.pos[1]))
				#юнит игрока №2
				units[-1].player=2
				units[-1].selected=False
		#если мышь движется
		if event.type==pygame.MOUSEMOTION:
			#И зажата правая кнопка
			if event.buttons==(0,0,1):
				#Рисуем рамку
				frame.h=event.pos[1]-frame.y
				frame.w=event.pos[0]-frame.x
				#Все юниты
				for un in units:
					if un.player==1:
						#попавшие в рамку
						if frame.in_frame(un):
							#выделяются
							un.selected=True
						else:
							un.selected=False
		#Отпустили мышь
		if event.type ==pygame.MOUSEBUTTONUP:
			if event.button==3:
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
	banners_player1=0
	banners_player2=0
	for banner in banners:
		banner.draw()
		if banner.player==1:
			banners_player1+=1
		if banner.player==2:
			banners_player2+=1
	if banners_player2==0:
		print("Вы победили!")
		run=False
	if banners_player1==0:
		print("Вы проиграли!")
		run=False
	
	#юниты
	for unit in units:
		#отрисовываются
		unit.draw()
		#выполняют действия
		unit.ai()
		#если расстояние до флага меньше порогового
		for banner in banners:
			if banner.distance(unit)<150:
				#если юнит другого игрока
				if banner.capture_player!=unit.player:
					#захват флага сбрасывается
					banner.capture=0
				#идет процесс захвата флага
				banner.capture_banner(unit.player)
			
			
		#стрельба		
		#перебираем всех врагов
		for en_unit in units:
			#если игроки разные
			if en_unit.player!=unit.player:
				#и если до врага расстояние меньше дистанции стрельбы
				if unit.distance(en_unit)<unit.shooting_radius:
					unit.state="shoot"
					unit.set_target(en_unit)
					bullets+=unit.bullets
					
		if unit.player==2:
			for banner in banners:
				if banner.player!=unit.player:
					unit.set_destination_point((banner.x,banner.y))
					unit.set_state="move"
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
