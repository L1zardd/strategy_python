import pygame
class Frame:
	x=0
	y=0
	w=0
	h=0
	color=(250,250,120)
	wnd=0
	
	def __init__(self,window,x,y):
		self.wnd=window
		self.x,self.y=x,y
	
	def draw(self):
		pygame.draw.rect(self.wnd,self.color,(self.x,self.y,self.w,self.h),5)

	def in_frame(self,unit):
		if (unit.x>self.x) and (unit.x<self.x+self.w):
			if (unit.y>self.y) and (unit.y<self.y+self.w):
				return True
		return False
	
