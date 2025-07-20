import pygame, random

pygame.init()
pygame.display.set_caption("Spongebob Run")

# Global Constants ----------------------------------------------
SCREEN_HEIGHT = 300
SCREEN_WIDTH = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
GAME_SPEED = 5

# Surfaces ------------------------------------------------------
ground = pygame.Rect(0, 250, 900, 60)

# obstacles
obs1 = pygame.image.load('obs1.png')
obs1 = pygame.transform.scale(obs1, 
                                 (obs1.get_width() / 6,
                                  obs1.get_height() / 6))
obs2 = pygame.image.load('obs2.png')
obs2 = pygame.transform.scale(obs2, 
                                 (obs2.get_width() / 6,
                                  obs2.get_height() / 6))
obs3 = pygame.image.load('obs3.png')
obs3 = pygame.transform.scale(obs3, 
                                 (obs3.get_width() / 6,
                                  obs3.get_height() / 6))
barnacle_imgs_a = [obs1, obs2, obs3]

obs4 = pygame.image.load('obs4.png')
obs4 = pygame.transform.scale(obs4, 
                                 (obs4.get_width() / 6,
                                  obs4.get_height() / 6))
obs5 = pygame.image.load('obs5.png')
obs5 = pygame.transform.scale(obs5, 
                                 (obs5.get_width() / 6,
                                  obs5.get_height() / 6))
obs6 = pygame.image.load('obs6.png')
obs6 = pygame.transform.scale(obs6, 
                                 (obs6.get_width() / 6,
                                  obs6.get_height() / 6))
barnacle_imgs_b = [obs4, obs5, obs6]

# bob
bob_img = pygame.image.load('bob.png').convert_alpha()
bob_img = pygame.transform.scale(bob_img, 
                                 (bob_img.get_width() / 5,
                                  bob_img.get_height() / 5))
bob_x_pos = 100
bob_y_pos = 220

jumping = False
y_gravity = 1
jump_height = 15
y_velocity = jump_height

# text
font = pygame.font.Font(None, size=30)

# sound
jump_sound = pygame.mixer.Sound('jump_sound.mp3')
hit_sound = pygame.mixer.Sound('hit_sound.wav')

class Obstacle:
    def __init__(self, image, type):        
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= GAME_SPEED
        if self.rect.x < -self.rect.width:
            obstacles.pop()
          
    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class BarnacleA(Obstacle):
        def __init__(self, image):  
            self.type = random.randint(0,2)    
            super().__init__(image, self.type) 
            self.rect.y = 200

class BarnacleB(Obstacle):
        def __init__(self, image):  
            self.type = random.randint(0,2)    
            super().__init__(image, self.type) 
            self.rect.y = 230

# Game Loop ------------------------------------------------------
def main (): 
    global GAME_SPEED, jumping, bob_x_pos, bob_y_pos, obstacles, y_velocity, points
    running = True
    obstacles = []
    points = 0
    death_count = 0

    def score():
        global points, GAME_SPEED
        points+=1
        if points % 100 == 0:
            GAME_SPEED += 0.0025

        points_text = font.render("Points: " + str(points), True, (255,255,255))
        points_text_rect = points_text.get_rect()
        points_text_rect.center = (800, 30)
        SCREEN.blit(points_text, points_text_rect)
        
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_sound.play()
                    jumping = True

        SCREEN.fill((13,152,186))

        pygame.draw.rect(SCREEN, (231, 215, 190), ground)

        score()

        if jumping:
            bob_y_pos -= y_velocity
            y_velocity -= y_gravity
            if y_velocity < -jump_height:
                jumping = False
                y_velocity = jump_height
            bob_rect = bob_img.get_rect(center = (bob_x_pos, bob_y_pos))
            bob_rect.width = 50
            bob_rect.height = 60
            SCREEN.blit(bob_img, bob_rect)
        else:
            bob_rect = bob_img.get_rect(center = (bob_x_pos, bob_y_pos))
            bob_rect.width = 50
            bob_rect.height = 60
            SCREEN.blit(bob_img, bob_rect)

        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(BarnacleA(barnacle_imgs_a))
            if random.randint(0,2) == 0:
                obstacles.append(BarnacleB(barnacle_imgs_b))
            
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if bob_rect.colliderect(obstacle.rect):
                hit_sound.play()
                barnacles_text = font.render("OH BARNACLES!", True, (255,255,255))
                barnacles_text_rect = barnacles_text.get_rect()
                barnacles_text_rect.center = (450, 150)
                SCREEN.blit(barnacles_text, barnacles_text_rect)
                pygame.display.update()
                pygame.time.delay(2000)
                running = False
                death_count +=1
                menu(death_count)

        pygame.display.flip()
        CLOCK.tick(60)

def menu(death_count):
    global points, font
    running = True
    while running:
        SCREEN.fill((234,153,153))
        
        # start menu 
        if death_count == 0:
            start_text = font.render("Press the Space Bar to Start", True, (255,255,255))
        # end game menu
        elif death_count > 0:
            start_text = font.render("Press the Space Bar to Try Again", True, (255,255,255))
            score_text = font.render("Points: " + str(points), True, (255,255,255))
            score_rect = score_text.get_rect()
            score_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70)
            SCREEN.blit(score_text, score_rect)
        start_rect = start_text.get_rect()
        start_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
        SCREEN.blit(start_text, start_rect)
        SCREEN.blit(bob_img, ((SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 100)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_sound.play()
                    running = False
                    main()

menu(death_count=0)

