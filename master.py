import pygame
import time
#This is where main stuff will go (game process). Frfr. Frfr. Crazy.
import entity
import static_object
from input import input_handling
#This is where main stuff will go (game process). Frfr. Frfr.
pygame.init()
screen = pygame.display.set_mode((800,600))
screen_width = 800
screen_height = 600
clock = pygame.time.Clock()


#Instantiate object list
objects = []
#create an object at the bottom of the screen (placeholder) and add to objects
bottom_border = static_object.object(0, screen_height-10, screen_width, 20, color=(0, 255, 255))
objects = [bottom_border]

#Instantiate player
player = entity.Entity(100,100,50,50)
player_speed = 200
player.acceleration.y = 30
running = True
while running:
    delta_time = clock.get_time() / 1000 #Time in seconds since the last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(delta_time,screen.get_rect(),objects)
    input_handling.checkPlayerInput(player,delta_time,player_speed,player.rect, player.grounded)
    screen.fill((0,0,0))
    player.render(screen)
    for a in objects:
        a.render(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
