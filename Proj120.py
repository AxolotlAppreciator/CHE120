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
        self.grounded = False
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



    player = moving_entity(300,300,50,150,200,0.85)

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
        
        checkPlayerInput(player,delta_time, 200,player.rect,objects)
        handle_collisions(player,objects,'x')
        handle_collisions(player,objects,'y')
        updateEntity(player,delta_time,objects)
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
        print(delta_time)
        for a in objects:
            render(a,mainSurface)
        for b in activeEntities:
            render(b,mainSurface)
            updateEntity(b,delta_time,objects)  
            handle_collisions(b,objects,'x')
            handle_collisions(b,objects,'y') 
        
        if gamestate == 1:
            pass
        
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()     # Once we leave the loop, close the window.


def render(object, screen):
    if object.sprite:
        screen.blit(object.sprite, (object.rect.x, object.rect.y))
    else:
        pygame.draw.rect(screen, (255, 0, 0), object.rect)  # Placeholder red rectangle

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
                        self.rect.left = obj.rect.right
                    self.velocity.x = 0  # Stop horizontal velocity
                elif axis == "y":
                # Vertical collision
                    if self.velocity.y > 0:  # Moving down
                        overlap = self.rect.bottom - obj.rect.top
                        if overlap > 0:
                            self.rect.bottom -= overlap  # Correct sinking into the platform
                        self.velocity.y = 0  # Stop downward velocity
                        self.grounded = True  # Entity is on the ground
                    elif self.velocity.y < 0:  # Moving up
                        overlap = obj.bottom - self.rect.top
                        if overlap > 0:
                            self.rect.top += overlap  # Correct upward overlap
                        self.velocity.y = 0  # Stop upward velocity

def checkPlayerInput(player, delta_time, player_speed, objects):
        keys = pygame.key.get_pressed()
        # Jump logic
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.grounded:  # Arrow up or W
            #sets vertical velocity to 500 (can be changed, temporary)
            player.velocity.y = -15/delta_time
            print("jump")
            player.grounded = False

        # Horizontal movement logic

        # If a key is pressed, enables acceleration and sets the direction based on key pressed. 

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.accelerating = False
            

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Arrow left or A
            player.direction = -1
            player.accelerating = True
            print("left")
            #moving left

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Arrow right or D
            player.direction = 1
            player.accelerating = True
            print("right")
            #moving right

        else:
            # Stop accelerating if neither left nor right is pressed
            player.accelerating = False

                        

def updateEntity(self, delta_time, objects):
        # Apply gravity
        self.velocity.y += 25

        # If the entity is accelerating, it increases the speed based on that acceleration rate. If not, it slows down based on the deceleration rate.
        if self.accelerating:
            if abs(self.velocity.x) < self.max_speed:
                self.velocity.x += self.direction * 15
        else:
            self.velocity.x *= self.deceleration_rate
        
        #Updates horizontal position and checks for valid collision (x)
        self.rect.x += self.velocity.x * delta_time
        handle_collisions(self,objects, axis="x")

        # Update vertical position and checks for valid collision (y)
        self.rect.y += self.velocity.y * delta_time
        handle_collisions(self,objects, axis="y")

main()