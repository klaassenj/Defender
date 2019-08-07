__author__ = 'Jason'

import Fighter
import Sprite
import pygame
import Level
import Weapons

class House:

    def __init__(self, x, y, sprite, hp):
        self.x = x
        self.y = y
        self.width = sprite.width
        self.height = sprite.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprite = sprite
        self.image = sprite.image
        self.hp = hp
        self.healthBar = Fighter.Bar(self, self.hp, self.hp)
    def justsitthereanddonothing(self):
        pass
    def update(self, enemies, projectiles):
        self.healthBar.update(self.x, self.y, self.hp)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.hp <= 0:
            self.hp = 0
        else:
            for e in enemies:
                if e.rect.colliderect(self.rect):
                    e.stop = True
                    self.hp -= 1 / 30
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.healthBar.render(screen)
class Tower(House):
    def __init__(self, x, y, sprite, hp):
        self.x = x
        self.y = y
        self.width = sprite.width
        self.height = sprite.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprite = sprite
        self.image = sprite.image
        self.hp = hp
        self.healthBar = Fighter.Bar(self, self.hp, self.hp)
        self.radius = 50
        self.score = 0
        self.weapon = Weapons.Flame(self)
        self.time = 0
    def update(self, enemies, projectiles):
        self.time += 1
        target = None
        self.healthBar.update(self.x, self.y, self.hp)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.hp <= 0:
            self.hp = 0
        else:
            for e in enemies:
                if e.rect.colliderect(self.rect):
                    e.stop = True
                    self.hp -= 1 / 30
        for e in enemies:
            if Level.getDistance(e.x, self.x, e.y, self.y) <= 200:
                target = e
        if self.time % 30 == 0 and target is not None:
            self.weapon.fire((target.x, target.y), projectiles)

