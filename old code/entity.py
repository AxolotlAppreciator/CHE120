import pygame
from physics import physicsObject

class Entity(physicsObject):
    #Initializes an entity at (x,y) with a specified rectangular hitbox of width, height, a maximum movement speed of max_speed, and a deceleration rate (friction). Sprite path defaults to none. 
    def __init__(self, x, y, width, height, max_speed, deceleration_rate, spritePath=None):
        super().__init__(x, y, width, height)
        self.deceleration_rate = deceleration_rate
        self.sprite = None
        self.grounded = False
        self.accelerating = False
        self.direction = 0
        self.max_speed = max_speed
        # If there's a sprite path, load the sprite
        if spritePath:
            self.sprite = pygame.image.load(spritePath).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def update(self, delta_time, screen_rect, objects):
        # Apply gravity
        self.velocity += self.acceleration

        # If the entity is accelerating, it increases the speed based on that acceleration rate. If not, it slows down based on the deceleration rate.
        if self.accelerating:
            if abs(self.velocity.x) < self.max_speed:
                self.velocity.x += self.direction * 10
        else:
            self.velocity.x *= self.deceleration_rate
        
        #Updates horizontal position and checks for valid collision (x)
        self.rect.x += self.velocity.x * delta_time
        self.handle_collisions(objects, axis="x")

        # Update vertical position and checks for valid collision (y)
        self.rect.y += self.velocity.y * delta_time
        self.handle_collisions(objects, axis="y")

        # Clamp to screen bounds
        if screen_rect:
            self.rect.clamp_ip(screen_rect)

    def handle_collisions(self, objects, axis):
        #Checks for collisions in the X axis and Y axis seperately (could be done better) between self and all objects. 

        self.grounded = False  # Reset grounded status for vertical checks
        for obj in objects:
            if self.rect.colliderect(obj):
                if axis == "x":
                # Horizontal collision
                    if self.velocity.x > 0:  # Moving right
                       self.rect.right = obj.left
                    elif self.velocity.x < 0:  # Moving left
                        self.rect.left = obj.right
                    self.velocity.x = 0  # Stop horizontal velocity
                elif axis == "y":
                # Vertical collision
                    if self.velocity.y > 0:  # Moving down
                        overlap = self.rect.bottom - obj.top
                        if overlap > 0:
                            self.rect.bottom -= overlap  # Correct sinking into the platform
                        self.velocity.y = 0  # Stop downward velocity
                        self.grounded = True  # Entity is on the ground
                    elif self.velocity.y < 0:  # Moving up
                        overlap = obj.bottom - self.rect.top
                        if overlap > 0:
                            self.rect.top += overlap  # Correct upward overlap
                        self.velocity.y = 0  # Stop upward velocity

        
    def render(self, screen):
        """Render the entity to the screen"""
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Placeholder red rectangle