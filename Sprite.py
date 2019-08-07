__author__ = 'Jason'

import pygame

fps = 30

class Sprite:

    def __init__(self, path = None, thumbnailPath = None, image = None):
        if path is not None:
            self.image = pygame.image.load(path)
        else:
            self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        if thumbnailPath is not None:
            image = pygame.image.load(thumbnailPath)
            self.thumbnail = Sprite(image = image)
    def grayScale(self):
        for h in range(self.height):
            for w in range(self.width):
                rgb = tuple(self.image.get_at((w, h)))
                lum = int(0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2])
                alpha = rgb[3]
                self.image.set_at((w, h), (lum, lum, lum, alpha))
    def revert(self):
        for h in range(self.height):
            for w in range(self.width):
                self.image.set_at((w, h), self.pixels[w + h * self.image.get_width()])
class Anim:

    def __init__(self, x, y, sprites, dur):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.images = []
        self.totalFrames = len(sprites)
        self.frame = 0
        self.counter = 0
        self.fpi = int(dur * fps / self.totalFrames)
        self.complete = False
        for sprite in self.sprites:
            self.images.append(sprite.image)
    def update(self):
        self.counter += 1
        if self.counter == self.fpi:
            self.counter = 0
            self.frame += 1
        if self.frame >= self.totalFrames:
            self.complete = True

    def render(self, screen):
        screen.blit(self.images[self.frame], (self.x, self.y))

victoria = Sprite("res/victoria.png")
victoriaGold = Sprite("res/victoriaGold.png", "res/thumbnails/vg.png")
zach = Sprite("res/zach.png", "res/thumbnails/zb.png")
allison = Sprite("res/allison.png", "res/thumbnails/ap.png")
alyssa = Sprite("res/alyssa.png", "res/thumbnails/ar.png")
ben = Sprite("res/ben.png", "res/thumbnails/ar.png")
enemy = Sprite("res/enemy.png")
map = Sprite("res/grassmap.png")
house  = Sprite("res/house.png", "res/thumbnails/hb.png")
tower = Sprite("res/tower.png", "res/thumbnails/tg.png")
fireball = Sprite("res/fireball.png")
dynamite= Sprite("res/dynamite.png")
bolt = Sprite("res/bolt.png")
icicle = Sprite("res/icicle.png")
fire01 = Sprite("res/fire01.png")
fire02 = Sprite("res/fire02.png")
fire03 = Sprite("res/fire03.png")

mouse = Sprite("res/target.png")
mouseHovering = Sprite("res/targetRed.png")
gold = Sprite("res/gold.png")
wave = Sprite("res/wave.png")
bg = Sprite("res/snowbg.png")
alphabg = Sprite("res/alphabg.png")
greyalpha = Sprite("res/greyalpha.png")
exSprites = [fire01, fire02, fire03]
