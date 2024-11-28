import pygame
class object(pygame.Rect):
    def __init__(self, x, y, width, height, color=(255,0,0), sprite=None):
        super().__init__(x, y, width, height)
        self.color = color
        self.sprite = sprite

    def render(self, screen):
        if self.sprite:
            # If a sprite is provided, render it at the position of the object
            screen.blit(self.sprite, (self.x, self.y))
        else:
            # Otherwise, draw the object as a filled rectangle with the specified color
            pygame.draw.rect(screen, self.color, self)