import pygame,random, math
from unit import Unit
window = pygame.display.set_mode((1200,800),pygame.RESIZABLE)
	
run=True

units=[]
for i in range(1):
	unit=Unit(window,random.randint(100,1100),random.randint(100,700))
	units.append(unit)
	
while run:
	#ОЧЕРЕДЬ СОБЫТИЙ
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run=False
		if event.type == pygame.MOUSEBUTTONDOWN:
			unit.set_destination_point(event.pos)
			unit.state="move"
	
	#ОТРИСОВКА
	window.fill((120,120,220))
	
	for unit in units:
		unit.draw()
		unit.ai()
	
	pygame.display.update()
	pygame.time.delay(20)
