'''See PyGame Events documentation for a list of the events built into pygame: https://www.pygame.org/docs/ref/event.html '''
import pygame
import random
import time

pygame.display.set_caption("Chill Jump")

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
        self.sprite_frames = [] # list for sprite frames
        self.animation_timer = 0
        self.current_frame = 0
        
        # If there's a sprite path, load the sprite for animation
        if spritePath:
            self.sprite = pygame.image.load(player.png).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def render(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)  # Default to a green rectangle
            
# platform class
class platform():
    def __init__(self , x, y, width, height, platform_type = "regular", spritePath = None):
        self.rect = pygame.Rect(x ,y ,width,height)
        self.sprite = None
        self.type = platform_type
        self.speed = 0 if platform_type != "moving" else random.randint(1, 3)
        self.timer = None # timer for breaking platforms
        self.active = True # breaking platforms will deactivate after breaking
        
        if spritePath:
            self.sprite = pygame.image.load(player.png).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def get_platform_colour(self):
        if self.type == "regular":
            return (0, 255, 0)  # Green for regular
        elif self.type == "breaking":
            return (255, 0, 0)  # Red for breakable
        elif self.type == "moving":
            return (0, 0, 255)  # Blue for moving
        return (255, 255, 255)  # Default to white if unknown
        
    # horizontal moving platform
    def moving(self, screen_width):
        if self.type == "moving" and self.active:
            self.rect.x += self.speed
            # change directions after hitting the edges of the screen
            if self.rect.left <= 0 or self.rect.right >= screen_width:
                self.speed = -self.speed

    def breaking_platform(self):
        if self.type == "breaking" and self.active:
            self.active = False

    def on_collision(self):
        if self.type == "breaking" and self.active:
            if not self.timer:
                self.timer = time.time()
            elif time.time() - self.timer > 1.5:
                self.break_platform()
        
    def render(self, screen):
        colour = self.get_platform_colour() if self.active else (128, 128, 128) # grey = inactive
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:     
            pygame.draw.rect(screen, colour, self.rect)
    
    def respawn(self, screen_width, screen_heigh):
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -20)

    def scroll(self, speed):
        self.rect.y += speed # move platform vertically
        if self.rect.y > 580: # if the platform goes of screen
            self.rect.y = -20 # reset to the top of the screen


def generate_platforms(objects, num_platforms, screen_width, screen_height):
    platform_width = 100
    platform_height = 20
    for _ in range(num_platforms):
        x = random.randint(0, screen_width - platform_width)
        y = random.randint(0, screen_height - platform_height)

        platform_type = random.choice(["regular", "breaking", "moving"])
        speed = random.randint(1, 3) if platform_type == "moving" else 0
        new_platform = Platform(x, y, platform_width, platform_height, platform_type, speed=speed)
        objects.append(new_platform)

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

def update_animation(self, delta_time):
        if self.sprite_frames:
            self.animation_timer += delta_time
            if self.animation_timer > 0.1:  # adjust frame speed
                self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
                self.sprite = self.sprite_frames[self.current_frame]
                self.animation_timer = 0
                
main()
