import pygame
import time
class physicsObject:
    def __init__(self,x,y,width,height,mass=1):
        #Initializes a new physics object's position, dimensions and mass. 
        self.rect = pygame.Rect(x,y,width,height)
        self.mass = mass
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)

    def applyForce(self,force):
        #Sets the acceleration of a given physics object
        self.acceleration += force/self.mass
    
    def updateObject(self, delta_time):
        self.velocity += self.acceleration * delta_time
        self.rect.x += self.velocity.x * delta_time
        self.rect.y += self.velocity.y * delta_time
        self.acceleration = pygame.Vector2(0,0)
    
    def checkCollision(self,other):
        #Checks if this object is colliding with another
        return self.rect.colliderect(other.rect)
    
    def solve_collision(self,other):
        if self.checkCollision(other):
            #Stop movement on collision

            #Checking vertical movement
            if self.velocity.y > 0: #moving downwards
                self.rect.bottom = other.rect.top
                self.velocity.y = 0
            elif self.velocity.y < 0: #moving upwards
                self.rect.top = other.rect.bottom
                self.velocity.y = 0
            #checking horizontal movement
            if self.velocity.x > 0:
                self.rect.right = other.rect.left
                self.velocity.x = 0
            elif self.velocity.x < 0:
                self.rect.left = other.rect.right
                self.velocity.x = 0            
        
        