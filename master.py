import pygame
import time
#This is where main stuff will go (game process). Frfr. Frfr. Crazy.
pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
