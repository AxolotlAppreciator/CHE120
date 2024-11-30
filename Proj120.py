'''See PyGame Events documentation for a list of the events built into pygame: https://www.pygame.org/docs/ref/event.html '''
import pygame
import random

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 580   # Desired physical surface size, in pixels.

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
#     add if it falls behind it get fucked!! and lose
    #-----------------------------Program Variable Initialization----------------------------#
    # Set up some data to describe a small circle and its color
#     # Set up some data to describe a small circle and its color
    rectPos = [0, 410, 580, 400]
    gravity = 10
    rectPos2 = [0, 0, 580, 100]
    rectColor2 = (243, 218, 216)
    isJump = False
    jumpCount = 10
    x = 150
    y = 350
    width = 40
    height = 60
    x1 = -50
    y1 = 0
    widthP = 40
    heightP = 300
    gamestate = 0
#     press start tp space
#     either learn another way t hold downt he key or learn how to do both at the same
    #-----------------------------Main Program Loop---------------------------------------------#
    while True:
        pygame.time.delay(20)
        #-----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_a] and x > gravity: 
            x -= gravity
        if keys[pygame.K_d] and x < 580 - (gravity*5): 
            x += gravity
        if not(isJump): 
            if keys[pygame.K_w]:
                isJump = True
        else:
            if jumpCount >= -10:
                y -= (jumpCount * abs(jumpCount)) * 0.6
                jumpCount -= 1
            else: 
                jumpCount = 10
                isJump = False
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here... if (rectPos[1] <= pipePos1[1])
        x1 -= 3
        if(x1 <= -50):
            x1 = 550
            y1 = random.randint(300, 350)
        if (x + 30 >= x1) and (x +30 <= x1 + 60):
            if (y >= y1 - 10) and (y <= y1 + 60):
                print ('thr')
                gamestate += 1
            
        if gamestate == 1:
            pygame.draw.circle(mainSurface, (229, 107, 111), (2, 50), 20)
                

        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        mainSurface.fill((53, 80, 112))

               
        # Draw a circle on the surface
        pygame.draw.rect(mainSurface, (229, 107, 111), (x1, y1, widthP, heightP))
        #pygame.draw.rect(mainSurface, (109, 89, 122), rectPos)
#         pygame.draw.rect(mainSurface, rectColor2, rectPos2)
        pygame.draw.rect(mainSurface, (181, 101, 118), (x, y, width, height))
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

    pygame.quit()     # Once we leave the loop, close the window.

main()





