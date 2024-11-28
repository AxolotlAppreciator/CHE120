import pygame
import static_object

class button(pygame.Rect):
    def __init__(self, x, y, width, height, color=(255, 255, 255), sprite=None):
        super().__init__(x, y, width, height)  # Initialize as a pygame.Rect
        self.originalY = y  # Save the original Y position
        self.color = color
        self.sprite = sprite
        self.active = False

    def handle_entity_collision(self, entity):
        """Handle interaction with an entity and update the button state."""
        if self.colliderect(entity.rect):  # Check collision with the entity's rectangle
            if (
                entity.velocity.y >= 0  # The entity is falling or stationary
                and entity.rect.bottom <= self.top + 5  # On top of the button
            ):
                self.move_ip(0, 10)  # Move the button down
                self.active = True
        else:
            # Reset the button position if no entity is on top
            self.active = False
            if self.y > self.originalY:
                self.move_ip(0, -10)


    def render(self, screen):
        """Render the button to the screen."""
        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))  # Render the sprite if available
        else:
            pygame.draw.rect(screen, self.color, self)  # Draw a placeholder