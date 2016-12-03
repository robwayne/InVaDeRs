# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 14:29:39 2016

@author: Robert Gordon & Russell Coke
"""


import pygame
from pygame.sprite import Sprite as Sprite
import random
import sys


pygame.init()
surface = pygame.display.set_mode((640,480))
START_POS = (surface.get_width()//2, surface.get_height()-20)

class ColorWheel(Sprite):
    def __init__(self, pos, radius):
        super().__init__()
        self.pos = pos
        self.colors = {'red': [255,0,0],'green': [0,255,0], 'blue': [0,0,255], 'yellow': [255,255,0]}
        self.image = pygame.image.load('images/color-wheel.png').convert()
        self.image = pygame.transform.smoothscale(self.image, (20,20)) #reduce image size
        self.rect = pygame.Rect(pos, (radius,radius))


    def changeBallColor(self, ball):
        newColor = self.colors[['red','green','blue','yellow'][random.randrange(4)]]
        oldColor = ball.color
        while newColor == oldColor:
            newColor = self.colors[['red','green','blue','yellow'][random.randrange(4)]]
        ball.changeColor(newColor)

    def display(self, surface):
        surface.blit(self.image, self.pos)

    def move(self, direction):
        if direction.lower() == "up":
                self.pos = (self.pos[0],self.pos[1]+20)
                self.rect.move_ip(0,20)
        if direction.lower() == "down":
                self.pos = (self.pos[0],self.pos[1]-1)
                self.rect.move_ip(0,-1)

    def disappear(self, container):
        container.remove(self)

class ColorBall(Sprite):
    def __init__(self, radius):
        super().__init__()
        self.colors = {'red': [255,0,0],'green': [0,255,0], 'blue': [0,0,255], 'yellow': [0,255,255]}
        self.color = self.colors[['red', 'green','blue','yellow'][random.randrange(4)]]
        self.pos = START_POS
        self.image = pygame.Surface((radius, radius))
        self.image.fill(self.color)
        self.rect = pygame.Rect(self.pos, (radius, radius))


    def display(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.image.get_width())

    def move(self, direction):
        if direction.lower() == "up":
                self.pos = (self.pos[0],self.pos[1]-20)
                self.rect.move_ip(0,-20)

        if self.pos != START_POS:
            if direction.lower() == "down":
                self.pos = (self.pos[0],self.pos[1]+2)
                self.rect.move_ip(0,2)

    def changeColor(self, color):
        self.color = color

colorwheel = []
ball = ColorBall(7)
gravity = False

while True:
    surface.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            gravity = False
            ball.move("up")
            for i in colorwheel:
                i.move("up")
        if event.type == pygame.MOUSEBUTTONUP:
            gravity = True

    if gravity:
        ball.move("down")

    if random.randint(0,1000)>995:
        colorwheel.append(ColorWheel((surface.get_width()//2-5,0), 10))
    for i in colorwheel:
        if ball.rect.colliderect(i.rect):
            i.changeBallColor(ball)
            i.disappear(colorwheel)

    ball.display(surface)
    for i in colorwheel:
        i.display(surface)
    pygame.display.update()
pygame.display.quit()
