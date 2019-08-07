__author__ = 'Jason'

import pygame
import Sprite
import math
import PyButton
import Font
import Color
import Weapons
width = 1000
height = int(width * 9 / 16)
xOffset = 125
yOffset = 75
FPS = 30
import Fighter
import House
class Offset:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tuple = (self.x, self.y)
class Map:

    def __init__(self, sprite, width = -1, height = -1):
        self.png = sprite.image
        if width < 0 or height < 0:
            self.width = self.png.get_width()
            self.height = self.png.get_height()
            self.image = self.png
        else:
            self.image = pygame.Surface((width, height))
            self.image.blit(self.png, (0, 0))
    def update(self):
        pass
    def render(self, screen, start = (0, 0)):
        # Use camRect to adjust self.image
        cam = self.image
        screen.blit(cam, start) #Always draw from (0, 0)
class Wave:
    def __init__(self, mu, sigma, num = 1):
        self.num = num
        self.enemiesToDeploy = []
        self.mu = mu
        self.sigma = sigma
        self.time = 0
        self.complete = False
        self.spawnX = 50
        self.spawnY = 200
        for q in range(self.mu):
            self.enemiesToDeploy.append(Fighter.Enemy(self.spawnX, self.spawnY, Sprite.enemy))
    def update(self, keysPressed, enemies):
        newWave = False
        xpos = []
        for q in self.enemiesToDeploy:
            xpos.append(q.x)
        if len(self.enemiesToDeploy) == 0:
            if len(enemies)== 0:
                self.complete = True
                if self.time % 60 == 0:
                    newWave = True
                    self.complete = False
                    self.mu = 5
            if keysPressed[4]:
                self.mu = 4
                self.num = 4 - 3
                newWave = True
                self.complete = False
            elif keysPressed[5]:
                self.mu = 5
                self.num = 5 - 3
                newWave = True
                self.complete = False
            elif keysPressed[6]:
                self.mu = 6
                self.num = 6 - 3
                newWave = True
                self.complete = False
            if newWave:
                for q in range(self.mu):
                    self.enemiesToDeploy.append(Fighter.Enemy(50, 200, Sprite.enemy))
        elif self.time % self.sigma == 0 and not self.complete:
            nextEnemy = self.enemiesToDeploy[0]
            enemies.append(nextEnemy)
            self.enemiesToDeploy.remove(nextEnemy)
            if len(self.enemiesToDeploy) == 0:
                self.time = 0
        self.time += 1
        if self.time > 7500:
            self.time = 0
class Table:
    def __init__(self, listA, listB):
        self.listA = listA
        self.listB = listB
        self.stock = []
        self.dictionary = zip(self.listA, self.listB)
    def update(self):
        self.dictionary = zip(self.listA, self.listB)
    def getListA(self):
        return self.listA
    def getListB(self):
        return self.listB
class Shop:
    def __init__(self, topX, topY, invList, reqList, maxButtons = 10, style = 0):
        self.xList = []
        self.yList = []
        self.bwidth = 75
        self.bheight = int(self.bwidth * 9 / 16)
        if style == 0:
            for q in range(maxButtons):
                self.xList.append(topX + 100 * (q + 2))
            for q in range(maxButtons):
                self.yList.append(topY + 35)
        elif style == 1:
            for q in range(maxButtons):
                self.xList.append(topX + 200)
            for q in range(maxButtons):
                self.yList.append(topY + (self.bheight + 10) * (q + 2))
        self.inventory = Table(invList, reqList)
        self.buttons = []
        self.hoveredButton = None
        self.hoveredButtonPrice = 0
        for q, item in enumerate(self.inventory.getListA()):
            if isinstance(item, Weapons.Weapon):
                self.buttons.append(PyButton.Button(self.xList[q], self.yList[q], self.bwidth, self.bheight, baseColor = Color.white, sprite = item.projectileSprite, font = Font.mediumAgency))
            elif isinstance(item, Sprite.Sprite):
                if item.thumbnail is not None:
                    self.buttons.append(PyButton.Button(self.xList[q], self.yList[q], self.bwidth, self.bheight, baseColor = Color.white, sprite = item.thumbnail, font = Font.mediumAgency))
                else:
                    self.buttons.append(PyButton.Button(self.xList[q], self.yList[q], self.bwidth, self.bheight, baseColor = Color.white, sprite = item, font = Font.mediumAgency))
            elif isinstance(item, House.House):
                self.buttons.append(PyButton.Button(self.xList[q], self.yList[q], self.bwidth, self.bheight, baseColor = Color.white, sprite = item.sprite.thumbnail, font = Font.mediumAgency))
    def update(self, mousePos, leftClicked, currency):
        for q, b in enumerate(self.buttons):
            b.update(mousePos, leftClicked)
            if b.highlit is True:
                self.hoveredButton = b
                self.hoveredButtonPrice = self.inventory.getListB()[q]
            if b.pressed and currency >= self.hoveredButtonPrice:
                temp = self.inventory.getListA()[q]
                if isinstance(temp, Weapons.Weapon):
                    Fighter.player.weapon = temp
                    Fighter.player.inv.gold -= self.hoveredButtonPrice
                elif isinstance(temp, Sprite.Sprite):
                    Fighter.player.image = temp.image
    def render(self, screen):
        for b in self.buttons:
            b.draw(screen)
class TowerShop(Shop):
    pass
map = Map(Sprite.map)
bg = Map(Sprite.bg)
alphabg = Map(Sprite.alphabg)
alphabg2 = Map(Sprite.greyalpha, 600, 100)

wave = Wave(5, FPS)
offset = Offset(xOffset, yOffset)
shop = Shop(0, height + yOffset, [Weapons.Flame(Fighter.player), Weapons.Thunder(Fighter.player), Weapons.Icer(Fighter.player)], [5, 10, 20])
skinsShop = Shop(width - 100, 200, [Sprite.zach, Sprite.victoriaGold, Sprite.allison, Sprite.ben], [1, 2, 3, 4], style=1)
#Examples of Bad Object Oriented Programming Below
#wave1 = Wave(5, FPS, 1)
#wave2 = Wave(10, FPS * 1.1, 2)
#wave3 = Wave(20, FPS * 1.2, 3)


#Calc Functions
def getDistance(x1, x2, y1, y2):
    xParam = (x1 - x2) * (x1 - x2)
    yParam = (y1 - y2) * (y1 - y2)
    return math.sqrt(xParam + yParam)

#def calcWaveStats()

# Extra Functions
def renderMouse(screen, enemies):
    mousePos = pygame.mouse.get_pos()
    pos = (mousePos[0] - Sprite.mouseHovering.width / 2, mousePos[1] - Sprite.mouseHovering.height / 2)
    for en in enemies:
        if en.rect.collidepoint(mousePos):
            image = Sprite.mouseHovering.image
            screen.blit(image, pos)
            break
    else:
        screen.blit(Sprite.mouse.image, pos)