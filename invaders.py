import pygame
import random
import sys

class Particle:
    def __init__(self, width):
        position = (random.randint(0, width), 0)
        self.velocity = [0, 3]
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(position, (4,4))
        
    def display(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ship:
    def __init__(self, img, screen):
        self.img = img
        self.rect = pygame.Rect(screen.get_width()//2, screen.get_height()-40, 40, 40)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)
        
    def left(self):
        self.rect.move_ip(-3, 0)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)
        
    def right(self):
        self.rect.move_ip(3, 0)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)
        
    def up(self):
        self.rect.move_ip(0, -3)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)
    
    def down(self):
        self.rect.move_ip(0, 6)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)
        
    def display(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect)
        screen.blit(self.img, self.imgCentre)

class Explosion:
    def __init__(self, boomspot):
        self.time = 40
        self.boomspot = boomspot
        self.imgList = []
        for i in range(7):
            self.imgList.append(pygame.image.load('explosionset/frame_'+str(i)+'_delay-0.1s.gif').convert())
    
    def explode(self, screen):
        if self.time>35:
            screen.blit(self.imgList[0], self.boomspot)
        elif self.time>30:
            screen.blit(self.imgList[1], self.boomspot)
        elif self.time>25:
            screen.blit(self.imgList[2], self.boomspot)
        elif self.time>20:
            screen.blit(self.imgList[3], self.boomspot)
        elif self.time>15:
            screen.blit(self.imgList[4], self.boomspot)
        elif self.time>10:
            screen.blit(self.imgList[5], self.boomspot)
        elif self.time>5:
            screen.blit(self.imgList[6], self.boomspot)
        self.time-=1
              
pygame.init()
pygame.mixer.music.load("The Weeknd ft. Daft Punk - Starboy (8-Bit NES remake).mp3")
boom = pygame.mixer.Sound("/Users/russellcoke/anaconda/lib/python3.5/site-packages/pygame/examples/data/boom.wav")
screen = pygame.display.set_mode((480, 640))
img = pygame.image.load('space-ship.png').convert()
font = pygame.font.Font(None, 24)
ship = Ship(img, screen)
hiScore = 0
cont = False
playing = False
hit = False
expl = []

while True:
    cont = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    difficulty = 100
                    cont = True
                if event.key==pygame.K_2:
                    difficulty = 150
                    cont = True
                if event.key==pygame.K_3:
                    difficulty = 200
                    cont = True
        if cont:
            break
        if playing == False:
            pygame.mixer.music.play(-1)
            playing = True
        screen.fill((0,0,0))
        text = font.render("InVaDeRs", True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-40, screen.get_height()//2))
        text = font.render("Select Difficulty: 1. Easy  2. Medium  3. Hard", True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-160, (screen.get_height()//2)+40))
        pygame.display.update()
    
    left = False
    right = False
    up = False
    down = False
    particles = []
    bullets = []
    gameover = False
    score = 0
    replay = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_DOWN:
                    down = True    
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(ship.rect.centerx, ship.rect.centery, 4, 4))
                   
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False
                    
        if left:
            ship.left()
        if right:
            ship.right()
        if up:
            ship.up()
        if down:
            ship.down()
                            
        if random.randint(0,1000) <= difficulty:
            particles.append(Particle(screen.get_width()))
        
        if gameover == True:
            break

        if playing == False:
            pygame.mixer.music.play(-1)
            playing = True
        
        screen.fill((0,0,0))
        for i in particles:
            i.display(screen)
            i.rect.move_ip(i.velocity[0], i.velocity[1])
            if i.rect.colliderect(ship.rect):
                gameover = True  
            for c in bullets:
                if i.rect.colliderect(c):
                    particles.remove(i)
                    bullets.remove(c)
                    boomspot = (c.centerx-30, c.centery-30)
                    expl.append(Explosion(boomspot))
                    boom.play()
                    score+=1
        if expl:
            for i in expl:
                if i.time == 0:
                    expl.remove(i)
                else:
                    i.explode(screen)   
                
        for b in bullets:
            pygame.draw.rect(screen, (255,0,0), b)
            b.move_ip(0, -3)
            
        
        ship.display(screen)
        pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    replay = True
        if replay == True:
            break
        if playing == True:
            pygame.mixer.music.stop()
            playing=False
        if hiScore<score:
            hiScore = score
            
        screen.fill((0,0,0))
        text = font.render("Game Over", True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-50, (screen.get_height()//2)-40))
        text = font.render("Score: "+str(score), True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-40, (screen.get_height()//2)-20))
        text = font.render("High Score: "+str(hiScore), True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-60, (screen.get_height()//2)+0))
        text = font.render("Press SPACE To Replay", True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-90, (screen.get_height()//2)+20))
        
        pygame.display.update()
    
