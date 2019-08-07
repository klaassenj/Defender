__author__ = 'Tim & Jason'

import pygame
import Color
import Font
import Sprite

class Button:

    def __init__(self, x, y, width, height, string = None, baseColor = Color.orange, font = Font.largeCambria, stringColor = Color.blue, sprite = None):
        self.x = x
        self.y = y
        self.font = font
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.string = string
        self.color = baseColor
        self.originalColor = baseColor
        self.stringColor = stringColor
        self.sprite = sprite
        self.pressed = False
        self.highlit = False
    def center(self):
        self.x += self.width / 2
        self.y += self.height / 2
    def update(self, mousePos, leftClicked):
        self.highlit = False
        xHalf = self.width / 2
        yHalf = self.height / 2
        self.rect = pygame.Rect(self.x - xHalf, self.y - yHalf, self.width, self.height)
        if self.rect.collidepoint(mousePos):
            self.color = Color.mint
            self.highlit = True
        else:
            self.color = self.originalColor
        if leftClicked and self.highlit:
            self.pressed = True
        else:
            self.pressed = False
    def draw(self, screen):
        xHalf = self.width / 2
        yHalf = self.height / 2
        topLeft = [self.x - xHalf, self.y - yHalf]
        topRight = (self.x + xHalf, self.y - yHalf)
        bottomLeft = (self.x - xHalf, self.y + yHalf)
        bottomRight = (self.x + xHalf, self.y + yHalf)

        pygame.draw.rect(screen, self.color, [topLeft[0], topLeft[1],  self.width, self.height])
        pygame.draw.line(screen, Color.black, topLeft, topRight, 5)
        pygame.draw.line(screen, Color.black, bottomLeft, bottomRight, 5)
        pygame.draw.line(screen, Color.black, topLeft, bottomLeft, 5)
        pygame.draw.line(screen, Color.black, topRight, bottomRight, 5)
        if self.string is not None:
            text = self.font.render(self.string, True, self.stringColor)
            rect = text.get_rect()
            rect.center = (self.x, self.y)
            screen.blit(text, rect)
        elif self.sprite is not None:
            x = self.x - self.sprite.width / 2
            y = self.y  - self.sprite.height / 2
            screen.blit(self.sprite.image, (x, y))
        else:
            print('Bug')
