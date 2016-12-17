import os
import pygame
import random
import sys
import time

import socket

class ClientSocket():
    def __init__(self, sock=None):
        if sock == None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = sock
        self.msglen = 1024

    def connect(self, host, port):
        self.socket.connect((host, port))

    def send(self, message):
        totalSent = 0
        while totalSent < len(message):
            msg = message[totalSent:]
            sent = self.socket.send(bytes(msg, "utf_8"))
            if sent == 0:
                raise RuntimeError("Nothing sent, connection closed")
            totalSent += sent


class Background:
    def __init__(self):
        self.pos = (0,0)
        self.imageList = []
        self.time = 100
        for i in range(5):
            self.imageList.append(pygame.image.load("images/backgroundset/frame_"+str(i)+"_delay-0.25s.gif"))

    def display(self, screen):
        if self.time == 0:
            self.time = 100
        if self.time > 80:
            screen.blit(self.imageList[0],self.pos)
        elif self.time > 60:
            screen.blit(self.imageList[1],self.pos)
        elif self.time > 40:
            screen.blit(self.imageList[2],self.pos)
        elif self.time > 20:
            screen.blit(self.imageList[3],self.pos)
        elif self.time > 0:
            screen.blit(self.imageList[4],self.pos)
        self.time-=1

class Particle:
    def __init__(self, pos):
        self.position = pos
        self.velocity = [0, 3]
        self.color = (0, 0, 0)
        self.rect = pygame.Rect(self.position, (14,14))
        self.img = pygame.image.load('images/asteroid_01.png').convert()
        self.imgCentre = (self.rect.centerx-7, self.rect.centery-7)
    def display(self, screen):
        self.imgCentre = (self.rect.centerx-7, self.rect.centery-7)
        screen.blit(self.img, self.imgCentre)


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
        screen.blit(self.img, self.imgCentre)

class Explosion:
    def __init__(self, boomspot):
        self.time = 40
        self.boomspot = boomspot
        self.imgList = []
        for i in range(7):
            self.imgList.append(pygame.image.load('images/explosionset/frame_'+str(i)+'_delay-0.1s.gif').convert())

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

class Bullet:
    def __init__(self, x, y):
        position = (x, y)
        self.velocity = [0,-3]
        self.color = (255,0,0)
        self.rect = pygame.Rect(position, (4,4))
        self.img = pygame.image.load('images/bullet.png').convert_alpha()
        self.imgCentre = (self.rect.centerx-2, self.rect.centery-2)
    def display(self, screen):
        self.imgCentre = (self.rect.centerx-2, self.rect.centery-2)
        screen.blit(self.img, self.imgCentre)
    def move(self):
        self.rect.move_ip(self.velocity[0], self.velocity[1])



pygame.init()
background = Background()
pygame.mixer.music.load("sounds/starboy-8bit.mp3")
boom = pygame.mixer.Sound("sounds/boom.wav")
screen = pygame.display.set_mode((480, 640))
img = pygame.image.load('images/xwing.png').convert_alpha()
font = pygame.font.Font(None, 24)
ship = Ship(img, screen)


hiScore = 0 #write to file
cont = False
playing = False
hit = False
expl = []
replay = False
client = ClientSocket()
client.connect('',5000)
while True:
    cont = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    cont = True
        if cont:
            break
        if playing == False:
            pygame.mixer.music.play(-1)
            playing = True
        screen.fill((165,20,80))
        text = font.render("InVaDeRs", True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-40, (screen.get_height()//2)-10))
        text = font.render("Press SPACE To Ready Up", True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-110, (screen.get_height()//2)+30))
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
    timer = 0
    client.send("ready")
    message = "Waiting on other players..."
    text = font.render(message, True, (255,255,255))
    while True:
        start = client.socket.recv(7).decode('utf_8')
        background.display(screen)
        screen.blit(text ,((screen.get_width()//2)-(len(message)*4), (screen.get_height()//2)-40))
        pygame.display.update()
        if start == 'start':
            message = "Player connected."
            text = font.render(message, True, (255,255,255))
            background.display(screen)
            screen.blit(text ,((screen.get_width()//2)-(len(message)*4), (screen.get_height()//2)-40))
            pygame.display.update()
            time.sleep(0.75)
            break
    while start == 'start':
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
                    bullets.append(Bullet(ship.rect.centerx, ship.rect.centery))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False

        time.sleep(0.02)
        client.send("a")
        pos = client.socket.recv(4)
        pos = pos.decode("utf_8")
        if gameover == True:
            client.send("dead")
            time.sleep(0.05)
            break

        if left:
            if ship.rect.left>0:
                ship.left()
        if right:
            if ship.rect.right<screen.get_width():
                ship.right()
        if up:
            if ship.rect.top>0:
                ship.up()
        if down:
            if ship.rect.bottom<screen.get_height():
                ship.down()

        pos = int(pos)
        particles.append(Particle((pos, 0)))

        if playing == False:
            pygame.mixer.music.play(-1)
            playing = True

        background.display(screen)
        for i in particles:
            i.display(screen)
            i.rect.move_ip(i.velocity[0], i.velocity[1])
            if i.rect.colliderect(ship.rect):
                gameover = True
            for c in bullets:
                if i.rect.colliderect(c.rect):
                    if i in particles:
                        particles.remove(i)
                    bullets.remove(c)
                    boomspot = (c.rect.centerx-30, c.rect.centery-30)
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
            b.display(screen)
            b.move()

        ship.display(screen)
        pygame.display.update()

    message = "Waiting on other players to die..."
    text = font.render(message, True, (255,255,255))
    while True:
        bothdead = client.socket.recv(3).decode('utf_8')
        background.display(screen)
        screen.blit(text ,((screen.get_width()//2)-(len(message)*4), (screen.get_height()//2)-40))
        pygame.display.update()
        if bothdead == 'yes':
            break

    client.send(str(client.socket.getsockname())+','+str(score))
    data = client.socket.recv(80).decode("utf_8")
    y = data.split(',')
    scores = ['', '']
    for i in range(2):
        if i == 0:
            scores[i] = y[0]+','+y[1]
        elif i ==1:
            scores[i] = y[2]+','+y[3]
        scores[i] = scores[i].replace('[', '').replace(']', '').replace("'", "").replace(' ', '')
        scores[i] = scores[i].split(',')
    for i in scores:
        if i[0]==client.socket.getsockname()[0]:
            continue
        else:
            p2Score = int(i[1])

    client.send('fin')

    print("entering while")
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
        print("inside while")
        print("Player 2 Score: "+str(p2Score))
        if score>p2Score:
            message = "You Won!"
        elif p2Score>score:
            message = "You Lost!"
        else:
            message = "It's a draw!"
        background.display(screen)
        text = font.render(message, True, (255,255,255))
        screen.blit(text, ((screen.get_width()-len(message)*8)//2, (screen.get_height()//2)-60))
        msgLen, length = len("Your Score: "+str(score)), len("Your Score: ")
        text = font.render("Your Score: ", True, (255,255,255))
        pos1 = (screen.get_width()-msgLen*8)//2
        screen.blit(text, (pos1, (screen.get_height()//2)-40))
        text = font.render(str(score), True, (0,255,0))
        screen.blit(text,(pos1+(length*8), (screen.get_height()//2-40)))
        msgLen, length = len("Player 2's Score: "+str(p2Score)), len("Player 2's Score: ")
        text = font.render("Player 2's Score: ", True, (255,255,255))
        pos1 = (screen.get_width()-msgLen*8)//2
        screen.blit(text, (pos1, (screen.get_height()//2)-20))
        text = font.render(str(p2Score), True, (255,0,0))
        screen.blit(text, (pos1+(length*8), (screen.get_height()//2-20)))
        msg = "High Score: "+str(hiScore)
        text = font.render(msg, True, (255,255,255))
        screen.blit(text ,((screen.get_width()-(len(msg)*8))//2, screen.get_height()//2))
        msg = "Press SPACE To Replay"
        text = font.render(msg, True, (255,255,255))
        screen.blit(text ,((screen.get_width()-(len(msg)*8))//2, (screen.get_height()//2)+20))

        pygame.display.update()
