__author__ = 'Jason'

import math
import pygame
import  Sprite
import Level
class Projectile:

    def __init__(self, launcher, mousePos, sprite):
        self.owner = launcher
        self.image = sprite.image
        self.x = launcher.x
        self.y = launcher.y
        self.startX = launcher.x
        self.startY = launcher.y
        self.radius = sprite.width / 2
        self.damage = 4
        self.range = 1000
        self.speed = 15
        self.target = mousePos
        self.targetRect = pygame.Rect(mousePos[0] - 30, mousePos[1] - 30, 60, 60)
        self.mouseX = mousePos[0] - 20
        self.mouseY = mousePos[1] - 20
        self.theta = math.atan2(self.mouseY - self.y, self.mouseX - self.x)
        self.exploded = False
        self.complete = False
    def update(self, width, height, effects):
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            self.complete = True
        if self.targetRect.collidepoint(self.x, self.y) or Level.getDistance(self.x, self.startX, self.y, self.startY) >= self.range:
            self.exploded = True
            self.complete = True
        else:
            xCom = math.cos(self.theta) * self.speed
            yCom = math.sin(self.theta) * self.speed
            self.move(self.target, xCom, yCom)
    def move(self, target, xSpeed, ySpeed):
        for k in range(abs(int(ySpeed))):
            self.y += abs(ySpeed) / ySpeed
        for h in range(abs(int(xSpeed))):
            self.x += abs(xSpeed) / xSpeed
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
class Weapon:
    def __init__(self, owner, sprite = None):
        self.owner = owner
        self.sprite = sprite
        self.projectileSprite = None
        self.uses = 0
    def update(self, leftClicked, mousePos, projectiles):
        if leftClicked:
            self.fire(mousePos, projectiles)
    def render(self, screen):
        pass#screen.blit(self.sprite.image, (self.owner.x, self.owner.y))
    def fire(self, mousePos):
        pass
    def getProjectileSprite(self):
        return self.projectileSprite
class Flame(Weapon):
    def __init__(self, owner, sprite = None):
        self.owner = owner
        self.projectileSprite = Sprite.fireball
        self.uses = 0
    def fire(self, mousePos, projectiles):
        projectiles.append(Fireball(self.owner, mousePos))
class Thunder(Weapon):
    def __init__(self, owner, sprite = None):
        self.owner = owner
        self.projectileSprite = Sprite.bolt
        self.uses = 0
    def fire(self, mousePos, projectiles):
        projectiles.append(Bolt(self.owner, mousePos))
class Icer(Weapon):
    def __init__(self, owner, sprite = None):
        self.owner = owner
        self.projectileSprite = Sprite.icicle
        self.uses = 0
    def fire(self, mousePos, projectiles):
        projectiles.append(Icicle(self.owner, mousePos))

class Fireball(Projectile):

    def __init__(self, launcher, mousePos = (0, 0), sprite = Sprite.dynamite):
        self.owner = launcher
        self.image = sprite.image
        self.x = launcher.x
        self.y = launcher.y
        self.startX = launcher.x
        self.startY = launcher.y
        self.radius = sprite.width / 2
        self.damage = 4
        self.range = 400
        self.speed = 15
        self.target = mousePos
        self.targetRect = pygame.Rect(mousePos[0] - 30, mousePos[1] - 30, 60, 60)
        self.mouseX = mousePos[0] - 20
        self.mouseY = mousePos[1] - 20
        self.theta = math.atan2(self.mouseY - self.y, self.mouseX - self.x)
        self.exploded = False
        self.complete = False
class Bolt(Projectile):

    def __init__(self, launcher, mousePos, sprite = Sprite.bolt):
        self.owner = launcher
        self.image = sprite.image
        self.x = launcher.x
        self.y = launcher.y
        self.startX = launcher.x
        self.startY = launcher.y
        self.radius = sprite.width / 2
        self.damage = 6
        self.range = 500
        self.speed = 30
        self.target = mousePos
        self.targetRect = pygame.Rect(mousePos[0] - 30, mousePos[1] - 30, 60, 60)
        self.mouseX = mousePos[0] - 20
        self.mouseY = mousePos[1] - 20
        self.theta = math.atan2(self.mouseY - self.y, self.mouseX - self.x)
        self.exploded = False
        self.complete = False
class Icicle(Projectile):

    def __init__(self, launcher, mousePos, sprite = Sprite.icicle):
        self.owner = launcher
        self.image = sprite.image
        self.x = launcher.x
        self.y = launcher.y
        self.startX = launcher.x
        self.startY = launcher.y
        self.radius = sprite.width / 2
        self.damage = 11
        self.range = 1000
        self.speed = 7
        self.target = mousePos
        self.targetRect = pygame.Rect(mousePos[0] - 30, mousePos[1] - 30, 60, 60)
        self.mouseX = mousePos[0] - 20
        self.mouseY = mousePos[1] - 20
        self.theta = math.atan2(self.mouseY - self.y, self.mouseX - self.x)
        self.exploded = False
        self.complete = False