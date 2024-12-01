'''See PyGame Events documentation for a list of the events built into pygame: https://www.pygame.org/docs/ref/event.html '''
import pygame
import random
import time
#Instantiate a new player entity
class moving_entity():     
    def __init__(self,x, y, width, height, max_speed, deceleration_rate, spritePath=None):
        self.rect = pygame.Rect(x,y,width,height)
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.deceleration_rate = deceleration_rate
        self.sprite = None
        self.grounded = True
        self.accelerating = False
        self.direction = 0
        self.max_speed = max_speed
        # If there's a sprite path, load the sprite
        if spritePath:
            self.sprite = pygame.image.load(spritePath).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width, height))
    
class platform():
    def __init__(self,x,y,width,height,spritePath = None):
        self.rect = pygame.Rect(x,y,width,height)
        self.velocity = pygame.Vector2(0,0)
        if spritePath:
            self.sprite = pygame.image.load(spritePath).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width, height))
        else:
            self.sprite = None
        

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 580   # Desired physical surface size, in pixels.


    clock = pygame.time.Clock()
    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
#     add if it falls behind it get fucked!! and lose
    #-----------------------------Program Variable Initialization----------------------------#



    player = moving_entity(300,300,100,150,200,0.85,"images\player.png")

    #List of all active objects on the screen
    objects = []

    #PLACEHOLDER PLATFORM FOR THE PLAYER TO START ON
    whoops_all_platforms = platform(300,350,200,20)
    objects.append(whoops_all_platforms)
    #List of active entities that get updated each frame
    activeEntities = []
    gamestate = 0
#     press start tp space
#     either learn another way t hold downt he key or learn how to do both at the same
    #-----------------------------Main Program Loop---------------------------------------------#
    while True:
        delta_time = clock.get_time() / 1000 # Time since last frame
        #-----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break
        
        print(player.velocity.y)
        checkPlayerInput(player, delta_time, 200, objects)
        player.rect.y = 300
        updateY(player, delta_time, objects, activeEntities)  # Update Y-axis movement
        updateObjects(player, delta_time, objects)           # Update X-axis movement
        handle_collisions(player, objects)      
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here... if (rectPos[1] <= pipePos1[1])

        if gamestate == 1:
            pass

        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        mainSurface.fill((53, 80, 112))
        

        # Rendering and updating objects and entities ->
        render(player,mainSurface)
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here... if (rectPos[1] <= pipePos1[1])
        mainSurface.fill((53, 80, 112))  # Clear the screen
        render(player, mainSurface)
        for obj in objects:
            render(obj, mainSurface)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()     # Once we leave the loop, close the window.


def render(object, screen):
    if object.sprite:
        screen.blit(object.sprite, (object.rect.x, object.rect.y))
    else:
        pygame.draw.rect(screen, (255, 0, 0), object.rect)  # Placeholder red rectangle

def handle_collisions(self, objects):
    for obj in objects:
        if self.rect.colliderect(obj.rect):
            # Horizontal adjustment
            #if self.rect.right > obj.rect.left and self.rect.left < obj.rect.left:
            #    self.rect.right = obj.rect.left  # Push out from the left
            #elif self.rect.left < obj.rect.right and self.rect.right > obj.rect.right:
            #    self.rect.left = obj.rect.right  # Push out from the right

        # Vertical adjustment
            if self.rect.bottom > obj.rect.top and self.rect.top < obj.rect.top:
                obj.rect.top = self.rect.bottom  # Push out from the top
                self.grounded = True
            elif self.rect.top < obj.rect.bottom and self.rect.bottom > obj.rect.bottom:
                obj.rect.bottom = self.rect.top  # Push out from the bottom
                



def checkPlayerInput(player, delta_time, player_speed, objects):
    keys = pygame.key.get_pressed()
    
    # Jump logic
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.grounded:
        player.velocity.y = -500  # Adjust jump strength
        player.grounded = False  # Set player as airborne
    if not player.grounded:
        player.velocity.y += 500 * delta_time
    # Horizontal movement logic
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.direction = -1
        player.accelerating = True
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.direction = 1
        player.accelerating = True
    else:
        player.accelerating = False

                        

def updateObjects(self, delta_time, objects):
    if self.accelerating:
        if abs(self.velocity.x) < self.max_speed:
            self.velocity.x += self.direction * 15
    else:
        self.velocity.x *= self.deceleration_rate
        
        #Updates horizontal position and checks for valid collision (x)
    self.rect.x += self.velocity.x * delta_time
    handle_collisions(self,objects)

def updateY(self, delta_time, objects, entities):
    # Apply gravity

    # If not grounded, move objects based on the player's velocity

    vertical_offset = self.velocity.y * delta_time
    for obj in objects:
        obj.rect.y -= vertical_offset
    for entity in entities:
        entity.rect.y -= vertical_offset



main()