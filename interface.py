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


def in_frame(frame,unit):
	if (unit.x>frame.x) and (unit.x<frame.x+frame.w):
		if (unit.y>frame.y) and (unit.y<frame.y+frame.w):
			return True			
	return False
	
