__author__ = 'Jason'
import pygame

launchCodeFonts = pygame.init()

smallAgency = pygame.font.SysFont('agencyfb', 25)
mediumAgency = pygame.font.SysFont('agencyfb', 45)
largeAgency = pygame.font.SysFont('agencyfb', 65, 'bold')

smallArial = pygame.font.SysFont('arial', 25)
mediumArial = pygame.font.SysFont('arial', 45)
largeArial = pygame.font.SysFont('arial', 65)

smallComicSans = pygame.font.SysFont('comicsansms', 25)
mediumComicSans = pygame.font.SysFont('comicsansms', 45)
largeComicSans = pygame.font.SysFont('comicsansms', 65)

smallCambria = pygame.font.SysFont('cambria', 25)
mediumCambria = pygame.font.SysFont('cambria', 45)
largeCambria = pygame.font.SysFont('cambria', 65)

smallCalibri = pygame.font.SysFont('calibri', 25)
mediumCalibri = pygame.font.SysFont('calibri', 45)
largeCalibri = pygame.font.SysFont('calibri', 65)

smallCorbel = pygame.font.SysFont('corbel', 25)
mediumCorbel = pygame.font.SysFont('corbel', 45)
largeCorbel = pygame.font.SysFont('corbel', 65)

smallVerdana = pygame.font.SysFont('verdana', 25)
mediumVerdana = pygame.font.SysFont('verdana', 45)
largeVerdana = pygame.font.SysFont('verdana', 65)

smallSketch = pygame.font.SysFont('sketchflowprint', 25)
mediumSketch = pygame.font.SysFont('sketchflowprint', 45)
largeSketch = pygame.font.SysFont('sketchflowprint', 65)

def createTextObject(font, string, color):
    return font.render(string, True, color)