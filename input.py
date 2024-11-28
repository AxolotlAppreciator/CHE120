import pygame
class input_handling:


    def checkPlayerInput(player,delta_time,player_speed, position, grounded):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w] and grounded:  # Arrow up or W
            player.velocity.y = -500 
            grounded = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Arrow left or A
            position.x -= player_speed * delta_time
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Arrow right or D
          position.x += player_speed * delta_time