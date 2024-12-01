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
        self.grounded = True
        self.accelerating = False
        self.direction = 0
        self.max_speed = max_speed
        # If there's a sprite path, load the sprite
        if spritePath:
            self.sprite = pygame.image.load(spritePath).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width+30, height))
    
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
            self.sprite = pygame.image.load(spritePath).convert_alpha()
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
    
    def respawn(self, screen_width, screen_height):
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



    player = moving_entity(300,300,100,150,200,0.85,"images\player.png")
    player.velocity.y = 497

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
        player.render(mainSurface)
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here... if (rectPos[1] <= pipePos1[1])
        mainSurface.fill((53, 80, 112))  # Clear the screen
        player.render(mainSurface)
        for obj in objects:
            obj.render(mainSurface)
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



def update_animation(self, delta_time):
        if self.sprite_frames:
            self.animation_timer += delta_time
            if self.animation_timer > 0.1:  # adjust frame speed
                self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
                self.sprite = self.sprite_frames[self.current_frame]
                self.animation_timer = 0
                
main()
