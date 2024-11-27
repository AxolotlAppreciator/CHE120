import pygame
class Entity(physicsObject):
    def __init__(self,x,y,width,height,color):
        super().__init__(x,y,width,height)
        self.color = color
    
    def render(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)