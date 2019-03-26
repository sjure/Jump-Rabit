import pygame

class Kanin():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 133
        self.velocity = 0
        self.speed = 4
        self.bakken = True
        self.falling = False
        self.gravity = -0.5
        self.hopp = 0
        self.coins = 0
    def update(self):
        if self.velocity < 0:
            self.falling = True
        else:
            self.falling = False
        self.velocity += self.gravity
        self.y -= self.velocity
    def render(self,kanin_img, display):
        display.blit(kanin_img.img, (self.x, self.y))

class Kanin_img_class():
    def __init__(self,img):
        self.img = img

class Planet():
    def __init__(self,x,y,img, speed):
        self.x = x
        self.y = y
        self.width = 240
        self.height = 10
        self.img = img
        self.speed = speed
    def render(self,display):
        pygame.draw.rect(display, (0,0,0,), (self.x, self.y, self.width, self.height))
        display.blit(self.img,(self.x - 5 , self.y - 125))

class Coin():
    def __init__(self,x, y, img, xspeed, yspeed):
        self.x = x
        self.y = y
        self.img = img
        self.width = 80
        self.height = 80
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.taken = False
    def render(self, display):
        if not self.taken:
            display.blit(self.img,(self.x,self.y))

class Lock():
    def __init__(self,x,y,img,price,rabit_img, name):
        self.x = x
        self.img = img
        self.y = y
        self.locked = True
        self.width = 115
        self.height = 115
        self.name = name
        self.price = price
        self.rabit_img = rabit_img
    def render(self, display):
        if self.locked:
            display.blit(self.img, (self.x, self.y))

class Scores():
    def __init__(self):
        self.coins = 0
        self.lock = 0
        self.highscore = 0

class Checkmark():
    def __init__(self,img):
        self.img = img
        self.x = -100
        self.y = -100
    def render(self, display, var = None):
        if var != None:
            if var == "lock1":
                self.x = 150
                self.y = 500
            elif var == "lock2":
                self.x = 460
                self.y = 500
            elif var == "lock3":
                self.x = 800
                self.y = 500
        display.blit(self.img, (self.x, self.y))




