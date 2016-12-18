
"""Authors: russellcoke & robwayne"""
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
        '''
        Loads the images for the background into a list, takes no argument
        '''
        self.pos = (0,0)
        self.imageList = []
        self.time = 100
        for i in range(5):
            self.imageList.append(pygame.image.load("images/backgroundset/frame_"+str(i)+"_delay-0.25s.gif"))

    def display(self, screen):
        '''
        displays the background as an animated image, takes the surface of the game
        as an argument.
        '''
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
        '''
        Takes a tuple and sets that as the particles position, creates the rectangle for
        the particle and also loads the image for the particle
        '''
        self.position = pos
        self.velocity = [0, 3]
        self.color = (0, 0, 0)
        self.rect = pygame.Rect(self.position, (14,14))
        self.img = pygame.image.load('images/asteroid_01.png').convert()
        self.imgCentre = (self.rect.centerx-7, self.rect.centery-7)


    def display(self, screen):
        '''
        Blits the image to the screen in the position of the rectangle object
        '''
        self.imgCentre = (self.rect.centerx-7, self.rect.centery-7)
        screen.blit(self.img, self.imgCentre)


class Ship:
    def __init__(self, img, screen):
        '''
        creates the rectangle for the ship an sets the image that was loaded in the main
        function of the game as the image of the ship
        '''
        self.img = img
        self.rect = pygame.Rect(screen.get_width()//2, screen.get_height()-40, 40, 40)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)

    def left(self):
        '''
        moves the ship to the left, takes no arguments
        '''
        self.rect.move_ip(-3, 0)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)

    def right(self):
        '''
        moves the ship to the right, takes no arguments
        '''
        self.rect.move_ip(3, 0)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)

    def up(self):
        '''
        moves the ship up, takes no arguments
        '''
        self.rect.move_ip(0, -3)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)

    def down(self):
        '''
        moves the ship down, takes no arguments
        '''
        self.rect.move_ip(0, 6)
        self.imgCentre = (self.rect.centerx-20, self.rect.centery-20)

    def display(self, screen):
        '''
        blits the ship to the screen, takes the surface of the game as the argument
        '''
        screen.blit(self.img, self.imgCentre)

class Explosion:
    def __init__(self, boomspot):
        '''
        Loads the images for the explosions into a list, takes a position tuple
        as the argument
        '''
        self.time = 40
        self.boomspot = boomspot
        self.imgList = []
        for i in range(7):
            self.imgList.append(pygame.image.load('images/explosionset/frame_'+str(i)+'_delay-0.1s.gif').convert())

    def explode(self, screen):
        '''
        displays the explosion as an animated image on the screen for a certain number of
        time, takes game surface as the argument
        '''
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
        '''
        creates a rectangle and loads an image for the bullet, takes two integers as
        the arguments
        '''
        position = (x, y)
        self.velocity = [0,-3]
        self.color = (255,0,0)
        self.rect = pygame.Rect(position, (4,4))
        self.img = pygame.image.load('images/bullet.png').convert_alpha()
        self.imgCentre = (self.rect.centerx-2, self.rect.centery-2)

    def display(self, screen):
        '''
        blits the bullet image to the screen, takes game surface as the argument
        '''
        self.imgCentre = (self.rect.centerx-2, self.rect.centery-2)
        screen.blit(self.img, self.imgCentre)

    def move(self):
        '''
        moves the bullet according to the velocity attribute, takes no arguments
        '''
        self.rect.move_ip(self.velocity[0], self.velocity[1])



pygame.init()
background = Background()
pygame.mixer.music.load("sounds/starboy-8bit.mp3")
boom = pygame.mixer.Sound("sounds/boom.wav")
screen = pygame.display.set_mode((480, 640))
img = pygame.image.load('images/xwing.png').convert_alpha()
font = pygame.font.Font(None, 24)
ship = Ship(img, screen)


try:
    fp = open("data/hiscore.txt", "r")
    if fp:
        line = fp.readline().strip()
        if line.isnumeric():
            Hscore = int(line)
except IOError:
    print("Creating hiscore file...")
    try:
        Hscore = 0
        fp =  open("data/hiscore.txt", "w")
        fp.write(str(Hscore))
    except IOError:
        raise Exception("Could not write to or open file: ")

fp.close()


hiScore = Hscore
cont = False
playing = False
hit = False
expl = []
replay = False
client = ClientSocket()
client.connect('',5000) #if not host, enter host's IP address as a string in the first parameter
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p','q','r','s','t','u','v','w','x','y','z']
name = []

#this loop handles replayability, so all game functions are within
while True:
    cont = False
    #this loop is for the home screen, allows entry of name
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    cont = True
                if str(pygame.key.name(event.key)) in letters:
                    name.append(str(pygame.key.name(event.key)))
                elif event.key == pygame.K_BACKSPACE:
                    if len(name)>0:
                        del name[-1]
        if cont:
            break
        if playing == False:
            pygame.mixer.music.play(-1)
            playing = True
        background.display(screen)
        text = font.render("InVaDeRs", True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-40, (screen.get_height()//2)-30))
        namestring = ''
        namestring = namestring.join(name)
        data = font.render(namestring, True, (255,255,255))
        enterthing = font.render("Enter name:", True, (255,255,255))
        screen.blit(enterthing, (190,320))
        screen.blit(data, (150,350))
        text = font.render("Press ENTER To Ready Up", True, (255,255,255))
        screen.blit(text ,((screen.get_width()//2)-110, (screen.get_height()//2)+60))
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
    client.send("ready") #tells server this player is ready
    message = "Waiting on other players..."
    text = font.render(message, True, (255,255,255))
    #this is an intermediate screen while the server waits for second player to connect
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
    #main game loop, receives particle position from server and adds to the particle list
    #when player dies it send a message to the server
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
        #sends 'a' meaning alive so server knows this player hasn't died yet
        client.send("a")
        #receives integer from server and stores it in pos variable used to generate a new particle
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
                boomspot = (ship.rect.centerx-30, ship.rect.centery-30)
                expl.append(Explosion(boomspot))
                boom.play()
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

        if not gameover:
            ship.display(screen)
        text = font.render('Score: '+str(score), True, (255,255,255))
        screen.blit(text, (400,10))
        pygame.display.update()

    message = "Waiting on other players to die..."
    text = font.render(message, True, (255,255,255))
    #intermediate screen that displays while server is waiting for other player to connect
    while True:
        bothdead = client.socket.recv(3).decode('utf_8')
        background.display(screen)
        screen.blit(text ,((screen.get_width()//2)-(len(message)*4), (screen.get_height()//2)-40))
        pygame.display.update()
        if bothdead == 'yes':
            break
    #when both players have died, sends the client's IP, score and nickname to the server
    client.send(str(client.socket.getsockname())+','+str(score)+','+namestring)
    #receive scores from the server and breaks them down into lists containing the IP, score and nickname of all players
    data = client.socket.recv(80).decode("utf_8")
    y = data.split(',')
    scores = ['', '']
    for i in range(2):
        if i == 0:
            scores[i] = y[0]+','+y[1]+','+y[2]
        elif i ==1:
            scores[i] = y[3]+','+y[4]+','+y[5]
        scores[i] = scores[i].replace('[', '').replace(']', '').replace("'", "").replace(' ', '')
        scores[i] = scores[i].split(',')
    for i in scores:
        if i[0]==client.socket.getsockname()[0]:
            continue
        else:
            p2Score = int(i[1])
            p2Name = i[2]
    #send fin to the server to signify it has received the scores
    client.send('fin')

    #final loop that displays the who won the match nd each players scores
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
        if hiScore<p2Score:
            hiScore = p2Score
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
        msgLen, length = len(p2Name+"'s Score: "+str(p2Score)), len("Player 2's Score: ")
        text = font.render(p2Name+"'s Score: ", True, (255,255,255))
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

        fp = open("data/hiscore.txt", "w")
        if fp:
            fp.write(str(hiScore))
        fp.close()
        pygame.display.update()
