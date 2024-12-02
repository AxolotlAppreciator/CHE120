'''See PyGame Events documentation for a list of the events built into pygame: https://www.pygame.org/docs/ref/event.html '''
import pygame
import random
import time

pygame.display.set_caption("Chill Jump")
## font = pygame.font.SysFont(None,25) ## change to comic sans and pick sizing and whatnot

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

        # Create a flipped version of the sprite for facing left
        self.sprite_left = pygame.transform.flip(self.sprite, True, False)  # Flip horizontally
    
    def render(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)  # Default to a green rectangle

class enemy():
    def __init__(self,x,y,width,height,health, enemy_type = "moving", spritePath = None):
        self.rect = pygame.Rect(x,y,width,height)
        self.sprite = None
        self.type = enemy_type
        self.velocity = 0
        self.health = 0
        originalX = x
        if spritePath:
            self.sprite = pygame.image.load(spritePath).convert_alpha
            self.sprite = pygame.transform.scale(self.sprite,(width,height))

    def backAndForth(self,originalX,speed,delta_time):
        if self.rect.x > originalX + 50:
            self.rect.x += speed * delta_time
        elif self.rect.x < originalX - 50:
            self.rect.x -= speed * delta_time


# platform class
class platform():
    def __init__(self , x, y, width, height, platform_type = "regular", spritePath = None, speed = 0):
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
        # this could be made into a switch case
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
            self.rect.x += self.speed * delta_time
            # change directions after hitting the edges of the screen
            if self.rect.left <= 0 or self.rect.right >= screen_width:
                self.speed = -self.speed

    def breaking_platform(self):
        if self.type == "breaking" and self.active:
            self.active = False

    def handle_breaking(self):
        if self.timer is None:
            self.timer = time.time()
        elif time.time() - self.timer > 1.5: 
            self.active = True

    def on_collision(self):
        if self.type == "breaking" and self.active:
            self.active = False
            self.timer = time.time()

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
            self.active = True
            self.timer = None

    def scroll(self, speed):
        self.rect.y += speed # move platform vertically
        if self.rect.y > 580: # if the platform goes of screen
            self.rect.y = -20 # reset to the top of the screen

    @staticmethod
    def generate_platforms(objects, num_platforms, screen_width, screen_height):
        platform_width = 100
        platform_height = 20
        platform_types = ["regular", 'breaking', 'moving']
        probabilities = [0.7, 0.2, 0.1]
        vertical_gap = 150
        y_position = screen_height - 50
        
        for _ in range(num_platforms):
            x = random.randint(0, screen_width - platform_width)
            y = y_position
            platform_type = random.choices(platform_types, probabilities)[0]
            speed = random.randint(50, 100) if platform_type == "moving" else 0
            new_platform = platform(x, y, platform_width, platform_height, platform_type, speed=speed)
            objects.append(new_platform)
            y_position -= vertical_gap

    def platform_generation_collision():
        pass

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


    font = pygame.font.Font(None, 36)
    player = moving_entity(300,290,75,100,200,0.85,"images/player.png")
    player.velocity.y = 497

    #List of all active objects on the screen
    objects = []
    platform.generate_platforms(objects, 10, surfaceSize, surfaceSize)
    first_platform = platform(300,600,100,10) ## ivy has 600 for mac
    objects.append(first_platform)

    #List of active entities that get updated each frame
    activeEntities = []
    gamestate = 1
    score = 0

    #-----------------------------Main Program Loop---------------------------------------------#
    while True:
        
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here... if (rectPos[1] <= pipePos1[1])

        if gamestate == 1:
            delta_time = clock.get_time() / 1000 # Time since last frame
            #-----------------------------Event Handling-----------------------------------------#
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    break
            mainSurface.fill((53, 80, 112))

            #print(player.velocity.y)
            checkPlayerInput(player, delta_time, 200, objects)
            for obj in objects:
                if player.rect.y > obj.rect.y + 60:
                    # player.rect.y += 500 * delta_time
                    pass
                else:
                    player.rect.y = 300

            updateY(player, delta_time, objects, activeEntities)  # Update Y-axis movement
            updateObjects(player, delta_time, objects)           # Update X-axis movement
            handle_collisions(player, objects)
            score = score + 1
            score_text = font.render(f'Score: {score}', True, (255, 255, 255))
            mainSurface.blit(score_text, (10, 10))      

            for platform in objects:
                if isinstance(platform, Platform):  
                    platform.update(surfaceSize, delta_time) 
                    platform.respawn(surfaceSize, surfaceSize)
                    if player.rect.colliderect(platform.rect):
                        if platform.active:
                            platform.on_collision()
                            player.grounded = True
                            player.rect.bottom = platform.rect.top

        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        

        # Rendering and updating objects and entities ->
            player.render(mainSurface) ## why is there two lol
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here... if (rectPos[1] <= pipePos1[1])  # Clear the screen
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
        player.velocity.y = -800  # Adjust jump strength
        player.grounded = False  # Set player as airborne
    if not player.grounded:
     player.velocity.y += 1300 * delta_time
        
    # Horizontal movement logic
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.direction = -1
        player.accelerating = True
        player.sprite = player.sprite_left  # Flip sprite to the left
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.direction = 1
        player.accelerating = True
        player.sprite = pygame.transform.flip(player.sprite_left, True, False)  # Flip sprite back to the right
    else:
        player.accelerating = False

                        

def updateObjects(self, delta_time, objects):
    if self.accelerating:
        if abs(self.velocity.x) < self.max_speed:
            self.velocity.x += self.direction * 15
    else:
        self.velocity.x *= self.deceleration_rate
    
    if self.rect.x < -70:
        self.rect.x = 550
    elif self.rect.x > 560:
        self.rect.x = -60
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