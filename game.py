#импорт необходимых библиотек
import pygame,random, math
#импорт классов из других файлов
from unit import *
from interface import Frame, in_frame
from level import Tile, Map
#главное окно программы
window = pygame.display.set_mode((1200,800),pygame.RESIZABLE)
	
run=True

units=[]


map1=Map(window,10,10)


building=Building(window,10,20)
building.units=units

frame=Frame(window,0,0)

bullets=[]


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
					if un.selected == True:
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
				
			#если правая - 
			elif event.button == 3:
				units.append(Unit(window,event.pos[0],event.pos[1]))
				units[-1].selected=False
		if event.type==pygame.MOUSEMOTION:
			if event.buttons==(0,1,0):
				frame.h=event.pos[1]-frame.y
				frame.w=event.pos[0]-frame.x
				for un in units:
					if in_frame(frame,un):
						un.selected=True
					else:
						un.selected=False
		if event.type ==pygame.MOUSEBUTTONUP:
			if event.button==2:
				frame.x=-10
				frame.y=-10
				frame.h=0
				frame.w=0
	
	#ОТРИСОВКА
	window.fill((120,120,220))
	
	map1.draw()
	building.draw()
	building.ai()
	
	for unit in units:
		unit.draw()
		unit.ai()
		if type(unit)==ShootingUnit:
			bullets+=unit.bullets
			if unit.hp<=0:
				units.remove(unit)
				del unit
	
	for bullet in bullets:
		if bullet.state=="move":
			bullet.draw()
			bullet.ai()
		else:
			bullets.remove(bullet)
			del bullet
	
	frame.draw()
	
	
	pygame.display.update()
	pygame.time.delay(20)
