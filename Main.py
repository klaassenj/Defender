__author__ = 'Jason'
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame

import Level
import Fighter
import Sprite
import Color
import House
import Font
import PyButton
import Weapons
import random
import Save
loadData = Save.readFile()
pygame.init()

width = Level.width + 2 * Level.offset.x
height = Level.height + 2 * Level.offset.y
print(width, height)
screenSize = (width, height)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Defender v0.5")
running = True
FPS = Level.FPS
spawnCooldown = FPS * 1.8
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.mixer.music.load('res/music/menuMusic.ogg')

def gameLoop():
    if loadData is not None:
        Fighter.player.level = loadData.level
        Fighter.player.xp = loadData.xp
    musicOn = True
    if musicOn:
        pygame.mixer.music.play()
    phase = 0
    #Dynamic Menu Vars
    play = PyButton.Button(width / 2, height / 2, 300, 100, 'Play', Color.orange, Font.largeSketch)
    menuButtons = [play]
    # Dynamic Vars
    keys = []
    projectiles = []
    effects = []
    enemies = []
    houses = []
    paused = False
    for q in range(4):
        houses.append(House.House(900, 50 + q * 135 + Level.offset.y, Sprite.tower, 10))
    time = 0
    for i in range(120): keys.append(False)
    while running:
        keysPressed, leftClicked, paused = handleKeyboardInput(keys, paused, enemies)
        mousePosition = pygame.mouse.get_pos()
        if phase == 0:
            if not paused:
                updateMenu(menuButtons, leftClicked, mousePosition, phase)
                if play.pressed:
                    phase = 1
                    if musicOn:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('res/music/gameMusic.ogg')
                        pygame.mixer.music.play()
            renderMenu(screen, menuButtons)
            pygame.display.update()
            clock.tick(FPS)
        if phase == 1:
            if not pygame.mixer.music.get_busy() and musicOn:
                pygame.mixer.music.play(start=24.0)
            if not paused:
                if update(keysPressed, leftClicked, mousePosition, projectiles, effects, enemies, houses) == 'GameOver':
                    phase = 2
            render(screen, projectiles, effects, enemies, houses)
            time += 1
            if time > spawnCooldown:
                time = 0
            pygame.display.update()
            clock.tick(FPS)
        if phase == 2:
            if updateGameOver(keysPressed) == 'NewGame':
                phase = 0
                resetTheGame(projectiles, enemies, houses, keys, effects)
            renderGameOver(screen)
            pygame.display.update()
            clock.tick(FPS)

def handleKeyboardInput(keys, paused, enemies): #Enemies param for testing
     mouse = False
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Save.createFile()
                pygame.quit()
                quit()
            if event.key == pygame.K_w:
                keys[0] = True
                #Left
            elif event.key == pygame.K_s:
                keys[1] = True
                #Right
            if event.key == pygame.K_a:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True
            if event.key == pygame.K_1:
                keys[4] = True
            if event.key == pygame.K_2:
                keys[5] = True
            if event.key == pygame.K_3:
                keys[6] = True
            if event.key == pygame.K_RETURN:
                keys[7] = True
            if event.key == pygame.K_m:
                keys[8] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_s:
                keys[1] = False
            if event.key == pygame.K_a:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
            if event.key == pygame.K_1:
                keys[4] = False
            if event.key == pygame.K_2:
                keys[5] = False
            if event.key == pygame.K_3:
                keys[6] = False
            if event.key == pygame.K_RETURN:
                keys[7] = False
            if event.key == pygame.K_m:
                keys[8] = False
            if event.key == pygame.K_p: #Add pause to keys
                if not paused:
                    paused = True
                else:
                    paused = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse = True

     return keys, mouse, paused
def write(string, color = Color.brown, xOffset = 0, yOffset = 0, font = Font.largeSketch, xa = -1, ya = -1):
    text = font.render(string, True, color)
    if xa >= 0 or ya >= 0:
        screen.blit(text, (xa, ya))
    else:
        rect = text.get_rect()
        rect.center = (width / 2 + xOffset, height / 2 + yOffset)
        screen.blit(text, rect)
def updateGameOver(keysPressed):
    if keysPressed[7]:
        return 'NewGame'
def renderGameOver(screen):
    screen.fill(Color.black)
    write('Game Over...', Color.red)
    write('Score: ' + str(Fighter.player.score), Color.sky, 0, 100, Font.mediumAgency)
def updateMenu(menuButtons, leftClicked, mousePosition, phase):
    for b in menuButtons:
        b.update(mousePosition, leftClicked)
def renderMenu(screen, menuButtons):
    screen.fill(Color.sky)
    for b in menuButtons:
        b.draw(screen)
    Level.renderMouse(screen, menuButtons)
def update(keysPressed, leftClicked, mousePos, projectiles, effects, enemies, houses):
    #print(str(int(clock.get_fps())))
    Level.map.update()
    Level.shop.update(mousePos, leftClicked, Fighter.player.inv.gold)
    Level.skinsShop.update(mousePos, leftClicked, Fighter.player.level)
    #Level.towerShop.update(mousePos, leftClicked, Fighter.player.inv.gold)
    houseSum = 0
    for h in houses:
        h.update(enemies, projectiles)
        houseSum += h.hp
    Fighter.player.update(keysPressed, leftClicked, mousePos, enemies, projectiles)
    Level.wave.update(keysPressed, enemies)
    for en in enemies:
        en.update(projectiles)
        if en.defeated:
            enemies.remove(en)
            Fighter.player.inv.gold += 1
            Fighter.player.xp += 20
    for e in effects:
        e.update()
        if e.complete:
            effects.remove(e)
    for p in projectiles:
        p.update(width, height, effects)
        if p.complete:
            projectiles.remove(p)
            effects.append(Sprite.Anim(p.x, p.y, Sprite.exSprites, .5))
    if Fighter.player.hp <= 0 or houseSum <= 0:
        return 'GameOver'
        #phase = 3
def render(screen, projectiles, effects, enemies, houses):
    screen.fill(Color.black)
    Level.map.render(screen, (0, Level.offset.y)) #[camX, camY, width, height]
    for h in houses:
        h.render(screen)
    Fighter.player.render(screen)
    for en in enemies:
        en.render(screen)
    for e in effects:
        e.render(screen)
    for p in projectiles:
        p.render(screen)
    Level.bg.render(screen)
    Level.shop.render(screen)
    Level.skinsShop.render(screen)
    #Level.towerShop.render(screen)
    Level.renderMouse(screen, enemies)
    screen.blit(Sprite.gold.image, (Level.width + 10, 100))
    screen.blit(Sprite.wave.image, (Level.width + 10, 150))
    write(str(Fighter.player.inv.gold) + ' Gold', Color.yellow, Level.width / 2 + 15, -240, Font.mediumAgency)
    write('Wave ' + str(Level.wave.num), Color.sky, Level.width / 2 + 15, -190, Font.mediumAgency)
    write('Score: ' + str(Fighter.player.score), Color.sky, Level.width / 2 - 50, -130, Font.mediumAgency)
    write('Shop', Color.purple, xa = 15, ya = height - 80, font = Font.largeCambria)
    write('Price:' + str(Level.shop.hoveredButtonPrice), Color.purple, xa = 450, ya = height - 80, font = Font.largeCambria)
def resetTheGame(projectiles, enemies, houses, keys, effects):
    projectiles.clear()
    enemies.clear()
    houses.clear()
    for q in range(4):
        houses.append(House.House(900, 50 + q * 135 + Level.offset.y, Sprite.house, 10))
    Fighter.player.reset()
    for i in range(120): keys[i] = False
gameLoop()
pygame.quit()
quit()