import pygame
class input_handling:
    def checkPlayerInput(player, delta_time, player_speed, position):
        keys = pygame.key.get_pressed()

        # Jump logic
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.grounded:  # Arrow up or W
            player.velocity.y = -500
            player.grounded = False

        # Horizontal movement logic
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.accelerating = False
            player.direction = 0
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Arrow left or A
            player.direction = -1
            player.accelerating = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Arrow right or D
            player.direction = 1
            player.accelerating = True
        else:
            # Stop accelerating if neither left nor right is pressed
            player.accelerating = False

    