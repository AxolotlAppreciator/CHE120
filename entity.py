import pygame
from physics import physicsObject
class Entity(physicsObject):
    def __init__(self,x,y,width,height, spritePath=None):
        super().__init__(x,y,width,height)
        self.sprite = None
        self.grounded = False
        #if there's a sprite path, load the sprite
        if spritePath:
            self.sprite = pygame.image.load(spritePath).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite,(width,height)) 
    
    def update(self, delta_time, screen_rect, objects):
        # Update the entity's position if it has a velocity
        self.velocity += self.acceleration
        self.rect.x += self.velocity.x * delta_time
        self.rect.y += self.velocity.y * delta_time 


        self.grounded = False  # Reset grounded status
        for obj in objects:
            if self.rect.colliderect(obj):  # Check for overlap with the object
                # Handle falling onto a platform (downward collision)
                if self.velocity.y > 0 and self.rect.bottom <= obj.top + self.velocity.y * delta_time:
                    self.rect.bottom = obj.top  # Position on top of the platform
                    self.velocity.y = 0  # Stop downward velocity
                    self.grounded = True  # Set grounded flag

                # Handle upward collision (colliding with the bottom of a platform)
                elif self.velocity.y < 0 and self.rect.top >= obj.bottom - self.velocity.y * delta_time:
                    self.rect.top = obj.bottom  # Prevent overlap when moving up
                    self.velocity.y = 0  # Stop upward velocity 

    
    def render(self,screen):
        #Renders the entity on the screen
        if self.sprite:
            screen.blit(self.sprite,(self.rect.x,self.rect.y))
        else:
            pygame.draw.rect(screen,(255,0,0),self.rect) #placeholder red rectangle.