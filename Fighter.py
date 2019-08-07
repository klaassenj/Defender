__author__ = 'Jason'

import Sprite
import Color
import pygame
import random
import Level
import Weapons
import Font

class Fighter:

    def __init__(self, x, y, sprite):
        self.cooldown = 0
        self.direction = 0
        self.image = sprite.image
        self.x = x + 50 * random.gauss(0, 1)
        self.y = y + 20 * random.gauss(0, 1) + Level.yOffset
        self.width = sprite.width
        self.height = sprite.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 2
        self.hp = 10
        self.healthBar = Bar(self, self.hp, self.hp)
        self.stop = False
        self.defeated = False
        self.killer = None
        self.weapon = Weapons.Flame(self)
    def update(self, projectiles):
        self.cooldown += 1
        if not self.stop:
            self.move(self.speed, 0)
            if self.cooldown % 30 == 1:
                self.direction = random.randint(-1, 1)
            np = self.y + self.speed * self.direction
            if np > 30 + Level.offset.y and np < Level.height + Level.offset.y - 30:
                self.move(self.speed * self.direction, 1)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.healthBar.update(self.x, self.y, self.hp)
        self.takeDamge(projectiles)
        if self.hp <= 0:
            self.defeated = True
    def takeDamge(self, projectiles):
        for p in projectiles:
            pCenter = [p.x + p.radius, p.y + p.radius]
            if self.rect.collidepoint(pCenter[0], pCenter[1]):
                self.hp -= p.damage
                p.complete = True
                self.killer = p.owner
                p.owner.score += 5
    def move(self, velocity, direction):
        if direction == 1:
            self.y += velocity
        elif direction == 0:
            self.x += velocity
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.healthBar.render(screen)
class Player(Fighter):
    def __init__(self, x, y, sprite):
        self.image = sprite.image
        self.spawnX = x
        self.spawnY = y
        self.x = x
        self.y = y + Level.yOffset
        self.width = sprite.width
        self.height = sprite.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 10
        self.hp = 10
        self.score = 0
        self.xp = 0
        self.level = 0
        self.levelNum = Font.createTextObject(Font.smallCambria, str(self.level), Color.black)
        self.healthBar = Bar(self, self.hp, self.hp)
        self.levelBar = LevelBar(self, self.xp, 100, Color.purple, Color.white, yOffset= -2, height = 2)
        self.inv = Inventory(self)
        self.weapon = Weapons.Flame(self)
        self.cooldown = 0
    def update(self, keys, leftClicked, mousePos, enemies, projectiles):
        self.levelNum = Font.createTextObject(Font.smallCambria, str(self.level), Color.black) #Inefficient
        self.cooldown += 1
        if self.cooldown > 7500:
            self.cooldown = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for e in enemies:
            if e.rect.colliderect(self.rect):
                self.hp -= 3 / 30
                self.score -= 1
        if leftClicked and self.cooldown > 30:
            self.cooldown = 0
            self.weapon.fire(mousePos, projectiles)
        self.healthBar.update(self.x, self.y, self.hp)
        self.levelBar.update(self.x, self.y, self.xp)
        if keys[0]:
            self.move(-self.speed, 1)
        elif keys[1]:
            self.move(self.speed, 1)
        if keys[2]:
            self.move(-self.speed, 0)
        elif keys[3]:
            self.move(self.speed, 0)
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.healthBar.render(screen)
        self.levelBar.render(screen)

    def reset(self):
        self.hp = 10
        self.healthBar.reset()
        self.score = 0
        self.x = self.spawnX
        self.y = self.spawnY
        self.xp = 0

class Enemy(Fighter):
    pass
class Bar: #Inefficient Overlapping Drawing Method
    def __init__(self, owner, filler, fillerMax, fg = Color.sky, bg = Color.red, yOffset = -12, height = 10):
        self.owner = owner
        self.offset = yOffset
        self.x = owner.x
        self.y = owner.y + self.offset
        self.length = owner.width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.filler = filler
        self.image = pygame.Surface((self.length, self.height))
        self.image.fill(self.fg)
        self.pixelsPerUnit = self.length / fillerMax
        self.unitsPerPixel = int(fillerMax / self.length)
        self.max = fillerMax
    def update(self, nx, ny, filler):
        self.x = nx
        self.y = ny + self.offset
        width = filler * self.pixelsPerUnit
        rect = (0, 0, width, self.height)
        self.image.fill(self.bg)
        self.image.fill(self.fg, rect)
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def reset(self):
        pass
class LevelBar(Bar):
    def update(self, nx, ny, filler):
         if filler >= self.max:
            self.owner.xp -= self.max
            self.owner.level += 1
            self.owner.levelNum = Font.createTextObject(Font.smallCambria, str(self.owner.level), Color.black)
         self.x = nx
         self.y = ny + self.offset
         width = filler * self.pixelsPerUnit
         rect = (0, 0, width, self.height)
         self.image.fill(self.bg)
         self.image.fill(self.fg, rect)
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.owner.levelNum, (self.x - self.owner.levelNum.get_width(), self.y - 20))
class Inventory:
    def __init__(self, owner, gold = 0, items = []):
        self.owner = owner
        self.gold = gold
        self.items = items
    def update(self):
        pass
    def render(self, screen):
        pass


player = Player(500, 276, Sprite.ben)
enemy = Enemy(50, 300, Sprite.enemy)