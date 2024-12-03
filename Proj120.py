'''See PyGame Events documentation for a list of the events built into pygame: https://www.pygame.org/docs/ref/event.html '''
import pygame
import random
import time
import math

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
        self.grounded = False
        self.accelerating = False
        self.direction = 0
        self.max_speed = max_speed
        self.mouse_held = False 
        self.dead = False
        self.lastTouched = None
        self.type = None
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
    def __init__(self,x,y,width,height,maxDist, enemy_type = "moving", spritePath = None):
        self.rect = pygame.Rect(x,y,width,height)
        self.sprite = None
        self.type = enemy_type
        self.accelerating = True
        self.max_speed = 500
        self.direction = 0
        self.velocity = pygame.Vector2(0,0)
        self.maxDist = maxDist
        self.originalX = x
        self.theta = 0
        if spritePath:
            self.sprite = pygame.image.load(spritePath).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite,(width+30,height))

    def movementBehaviour(self,originalX,maxDist,delta_time):
        if self.type == "moving":
            if self.rect.x > originalX + maxDist:
                self.direction = -1
            elif self.rect.x > originalX - maxDist:
                self.direction = 1
        elif self.type == "spinning":
            self.theta += math.pi*delta_time
            self.rect.x += math.cos(self.theta)*3
            self.rect.y += math.sin(self.theta)*3

    def render(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)  # Default to a green rectangle
    
    def respawn(self, screen_width, vertical_gap, highest_y):
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = highest_y - vertical_gap
        movement_types = ["moving", "spinning"]
        probabilities = [0.7, 0.3]
        self.type = random.choices(movement_types, probabilities)[0]
        self.velocity = pygame.Vector2(0, 0) if self.type != "moving" else random.randint(1, 5) * random.choice([-1, 1])
        self.active = True
        self.timer = 0
        self.maxDist = random.randint(100, 300)

    def update(self, delta_time):
        self.movementBehaviour(self.originalX, self.maxDist, delta_time)

# platform class
class Platform():
    def __init__(self , x, y, width, height, platform_type = "regular", spritePath = None, speed = 0, first = False):
        self.rect = pygame.Rect(x ,y ,width,height)
        self.sprite = None
        self.type = platform_type
        self.speed = 0 if platform_type != "moving" else random.randint(1, 3)
        self.timer = 0 # timer for breaking platforms
        self.active = True # breaking platforms will deactivate after breaking
        self.first = first

        if spritePath:
            self.sprite = pygame.image.load(spritePath).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def get_platform_colour(self):
        # this could be made into a switch case
        if self.first:
            return (0, 0, 0) ## black for the first
        if self.type == "regular" and not self.first:
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

    def on_collision(self, player):
        if self.type == "breaking" and self.active and player.rect.colliderect(self.rect):
            if self.timer is None:  # Start the 1.5-second timer when touched
                self.timer = time.time()
                self.active = False  # Platform becomes inactive after 1.5 seconds

    def handle_breaking(self):
        if self.timer:
            elapsed_time = time.time() - self.timer
            if elapsed_time >= 1.5:
                self.active = False  # Platform disappears after 1.5 seconds
    

    def render(self, screen):
        colour = self.get_platform_colour() if self.active else (128, 128, 128) # grey = inactive
        
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:     
            pygame.draw.rect(screen, colour, self.rect, border_radius=10)
    
    def respawn(self, screen_width, vertical_gap, highest_y):
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = highest_y - vertical_gap
        platform_types = ["regular", "breaking", "moving"]
        probabilities = [0.7, 0.2, 0.1]
        self.type = random.choices(platform_types, probabilities)[0]
        self.speed = 0 if self.type != "moving" else random.randint(1, 3)
        self.active = True
        self.timer = 0
        vertical_gap = 175

    def generate_platforms(objects, num_platforms, screen_width, screen_height):
        platform_width = 100
        platform_height = 20
        platform_types = ["regular", 'breaking', 'moving']
        probabilities = [0.7, 0.2, 0.1]
        vertical_gap = 175
        y_position = 400
        
        for _ in range(num_platforms):
            x = random.randint(0, screen_width - platform_width)
            y = y_position
            while any(p.rect.colliderect(pygame.Rect(x, y, platform_width, platform_height)) for p in objects):
                x = random.randint(0, screen_width - platform_width)
                y = random.randint(y_position - vertical_gap, y_position)
            platform_type = random.choices(platform_types, probabilities)[0]
            new_platform = Platform(x, y, platform_width, platform_height, platform_type)
            objects.append(new_platform)
            y_position -= vertical_gap

    def platform_generation_collision():
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        super().__init__()
        self.image = pygame.Surface((10, 5))  
        self.image.fill((255, 0, 0))  
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = speed

    def update(self, objects):
        # Move bullet in the direction of  vector
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Kill bullet if the bullet goes off-screen
        if not self.rect.colliderect(pygame.Rect(0, 0, pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())):
            self.kill()  # Remove the bullet from the sprite group
    
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
    player = moving_entity(300,375,75,100,290,0.85,"images/player.png")
    player.velocity.y = 497

    #List of all active objects on the screen
    objects = []
    Platform.generate_platforms(objects, 10, surfaceSize, surfaceSize)
    first_platform = Platform(300, 600, 100, 20)  # "regular", spritePath = None, speed = 0, first=True
    objects.append(first_platform)

    #placeholder enemy
    #def __init__(self,x,y,width,height,health, enemy_type = "moving", spritePath = None):
    enemy1 = enemy(200,300,50,75,100,spritePath = "images/enemy.png")
    enemy2 = enemy(200,300,50,75,100,spritePath = "images/enemy.png",enemy_type="spinning")

    #List of active entities that get updated each frame
    activeEntities = [enemy1,enemy2]
    gamestate = 1
    score = 0
    bullets_group = pygame.sprite.Group()


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
            bullets_group = checkPlayerInput(player, delta_time, 200, objects, bullets_group)  # Update bullets group
            for bullet in bullets_group:
                bullet.update(objects)
            #print(player.velocity.y)
            checkPlayerInput(player, delta_time, 200, objects, bullets_group)
            #for obj in objects:
            #    if player.rect.y > obj.rect.y + 60:
            #        player.rect.y += 500 * delta_time
            #    else:
            #        player.rect.y = 300
            bullets_group.draw(mainSurface)  # Draw all bullets
            if player.dead == True:
                gamestate = 2
            updateY(player, delta_time, objects, activeEntities)  # Update Y-axis movement
            updateObjects(player, delta_time, objects)           # Update X-axis movement
            handle_collisions(player, objects)
            score = score + 1
            score_text = font.render(f'Score: {score}', True, (255, 255, 255))
            mainSurface.blit(score_text, (10, 10))  

            highest_y = min(obj.rect.y for obj in objects if isinstance(obj, Platform))
            for obj in objects:
                if isinstance(obj, Platform):
                    obj.moving(surfaceSize) 
                    obj.render(mainSurface)    
                    if obj.rect.y > 1400:
                        Platform.respawn(obj, surfaceSize, 175, highest_y) 
                       # if random.random() < 0.25:
                       #     new_enemy = enemy.respawn(obj, surfaceSize, 175, highest_y)
                       #     if new_enemy is not None:
                       #         objects.append(new_enemy)
            for obj in objects:
                obj.render(mainSurface)
                if obj.type == "breaking" and obj.timer != 0:
                    print(obj.timer)
                    obj.timer -= delta_time
                    if obj.timer <= 0:
                        Platform.respawn(obj, surfaceSize, 175, highest_y)
            player.render(mainSurface)

            #-----------------------------Drawing Everything-------------------------------------#
            # We draw everything from scratch on each frame.
            # So first fill everything with the background color
            

        # Rendering and updating objects and entities ->
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here... if (rectPos[1] <= pipePos1[1])  # Clear the screen
            

            for entity in activeEntities:
                entity.render(mainSurface)
                updateObjects(entity, delta_time, objects)
                entity.movementBehaviour(entity.originalX, entity.maxDist, delta_time)
            for en in activeEntities:
                checkBullet(en,bullets_group,player,activeEntities)
            pygame.display.flip()
            clock.tick(60)
            
        if gamestate == 2:
            pygame.quit() 
            print("dead")
            #For now it just kills it, yana do death screen. 
    pygame.quit()     # Once we leave the loop, close the window.

def checkBullet(self,bullet,player,enemylist):
    if self.rect.colliderect(player.rect):
        player.dead = True
    for bul in bullet:
        if self.rect.colliderect(bul.rect):
            enemylist.remove(self)
def render(object, screen):
    if object.sprite:
        screen.blit(object.sprite, (object.rect.x, object.rect.y))
    else:
        pygame.draw.rect(screen, (255, 0, 0), object.rect)  # Placeholder red rectangle

def handle_collisions(self, objects):
    for obj in objects:

        if self.rect.colliderect(obj.rect):
            # Check if the object is landing on top of the platform
            if self.velocity.y > 0 and self.rect.bottom >= obj.rect.top:
                #print(obj.rect.top)
                #print(self.rect.bottom)
                if (self.rect.bottom - obj.rect.top) < 10 * self.velocity.y/120:

                    obj.rect.top = self.rect.bottom  # Snap to the top of the platform
                    self.grounded = True
                    self.lastTouched = obj.rect
                    self.velocity.y = 0  # Reset vertical velocity when landing
                    if obj.type == "breaking":
                        print("starting breakage")
                        obj.timer = 1.5
                        print(obj.timer)
    if self.lastTouched:
        if self.lastTouched.left > self.rect.right:
            self.grounded = False
        if self.lastTouched.right < self.rect.left:
            self.grounded = False
        
                
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


def updateY(self, delta_time, objects, entities):
    # Apply gravity

    # If not grounded, move objects based on the player's velocity
    if not self.grounded:
        vertical_offset = self.velocity.y * delta_time
    else:
        vertical_offset = 0
    for obj in objects:
        if not obj.first:
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

def checkPlayerInput(player, delta_time, player_speed, objects, bullets_group):
    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    
    # Jump logic
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.grounded:
        player.velocity.y = -1200  # Adjust jump strength
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
    
    # Mouse direction calculations
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position on screen
    dx = mouse_x - player.rect.centerx 
    dy = mouse_y - player.rect.centery
    distance = math.hypot(dx, dy) # Distance from player to mouse
    
    if distance != 0:  # Avoid division by zero
        direction_vector = pygame.Vector2(dx, dy).normalize()
    else:
        direction_vector = pygame.Vector2(0, 0)
    
    # Shoot logic
    if mouse_buttons[0]:  
        if not player.mouse_held: 
            bullet = Bullet(player.rect.centerx, player.rect.centery, direction_vector, 10)  # Create bullet
            bullets_group.add(bullet)  
            player.mouse_held = True 

    # If mouse button is released, reset flag (allow next shot on next click)
    if not mouse_buttons[0]:
        player.mouse_held = False
       
    return bullets_group
                
main()