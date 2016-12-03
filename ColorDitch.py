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
        self.colors = {'red': [255,0,0],'green': [0,255,0], 'blue': [0,0,255], 'yellow': [0,255,255]} 
        self.image = pygame.image.load('images/color_wheel.png').convert()
        self.image = pygame.transform.smoothscale(self.image, (20,20)) #reduce image size
        self.rect = pygame.Rect(pos, (radius,radius))
        
        
    def assignColor(self):
        return self.colors[['red','green','blue','yellow'][random.randrange(4)]]
        
    def display(self, surface):
        pygame.draw.rect(surface, (255,255,255), self.rect)
        surface.blit(self.image, self.pos)
        

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
        pygame.draw.rect(surface, (255,255,255), self.rect)
        pygame.draw.circle(surface, self.color, self.pos, self.image.get_width())
        
    def move(self, direction):
        if direction.lower() == "up":
                self.pos = (self.pos[0],self.pos[1]-10)
                self.rect.move_ip(0,-10)
                print("Up: ", self.rect)
        if self.pos != START_POS:
            if direction.lower() == "down":
                self.pos = (self.pos[0],self.pos[1]+1)
                self.rect.move_ip(0,1)
                print("Down: ", self.rect)
                
    def changeColor(self, color):
        self.color = color
        
ball = ColorBall(5)
gravity = False
while True:
    surface.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            gravity = False
            ball.move("up")
        if event.type == pygame.MOUSEBUTTONUP:
            gravity = True
        
    if gravity:
        ball.move("down")
        
    colorwheel = ColorWheel((surface.get_width()//2-5,surface.get_height()//2), 10) 
    if ball.rect.colliderect(colorwheel.rect):
        print("collides")
        ball.changeColor(colorwheel.assignColor())
    
    ball.display(surface)
    colorwheel.display(surface)
    pygame.display.update()
pygame.display.quit()

        