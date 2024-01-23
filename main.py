import pygame
import sys 
from pygame.math import Vector2
import math
from math import sqrt

pygame.init()

class Bloon:
    def __init__(self, type):
        self.type = type
        if type == 1:
            self.health = 10
            self.speed = 2
            self.prize = 10
            self.sprite = pygame.image.load("./textures/balloon1.png")
        elif type == 2:
            self.health = 5
            self.speed = 4
            self.prize = 15
            self.sprite = pygame.image.load("./textures/balloon2.png")
        elif type == 3:
            pass
        else:
            # Default values if type is not 1, 2, or 3
            self.health = 10
            self.speed = 2
            self.prize = 10
            self.sprite = pygame.image.load("./textures/balloon1.png")

        self.rect = self.sprite.get_rect()
        self.pos = [700, -50]
        self.rect.center = self.pos
        self.target = 1

class Turret:
    def __init__(self, type, pos):
        self.type = type
        if type == 1:
            self.damage = 3
            self.range = 100
            self.speed = 1
            self.sprite = pygame.image.load("./textures/turret1.png")
        elif type == 2:
            self.damage = 4
            self.range = 100
            self.speed = 3
            self.sprite = pygame.image.load("./textures/turret2.png")
        elif type == 3:
            pass
        else:
            # Default values if type is not 1, 2, or 3
            self.damage = 3
            self.range = 100
            self.speed = 1
            self.sprite = pygame.image.load("./textures/turret1.png")

        self.rect = self.sprite.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.timer = 0
        self.angle = 0
        self.target = 0

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

def createQueue():
    global bloonQueue
    for i in range(0,len(queueDict[level][wave])):
            bloonQueue.append(Bloon(int(queueDict[level][wave][i])))
    for j in range(0, len(bloonQueue)):
        bloonQueue[j].pos[1] -= j * bloonQueue[j].rect.height
        bloonQueue[j].rect.center = bloonQueue[j].pos

def bloonMove():
    if startFlag:
        for i in range(0,len(bloonQueue)):
            
            wayToTarget = Vector2(path[level][bloonQueue[i].target]) - Vector2(bloonQueue[i].pos)
            if bloonQueue[i].health > 0:
                if wayToTarget.length() <= bloonQueue[i].speed:
                    bloonQueue[i].pos = path[level][bloonQueue[i].target]
                    bloonQueue[i].rect.center = bloonQueue[i].pos
                    bloonQueue[i].target += 1

                
                bloonQueue[i].pos += bloonQueue[i].speed * wayToTarget.normalize()
                bloonQueue[i].rect.center = bloonQueue[i].pos
                
                screen.blit(bloonQueue[i].sprite, bloonQueue[i].rect)


    
def createTurret(turType, event):
    global money
    canPlace = True
    sprite1 = pygame.image.load("./textures/turret1.png")
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    spriteWidth = sprite1.get_width()
    spriteHeight = sprite1.get_height()

    for j in range(0, len(path[level])-1):
        if pygame.Rect(mouseX - spriteWidth, \
                       mouseY - 2.5*spriteHeight/2, \
                       2*spriteWidth, \
                       2.5*spriteHeight).clipline(path[level][j], path[level][j+1]) != ():
            
            canPlace = False

    for i in range(0,len(turretList)):
        if pygame.Rect(mouseX - 2*spriteWidth, \
                        mouseY - 2*spriteHeight, \
                        4*spriteWidth, \
                        4*spriteHeight).collidepoint(turretList[i].pos[0], turretList[i].pos[1]):
            
            canPlace = False
    
    if mouseX >= 775:
        canPlace = False

    if money < cost[turType]:
        canPlace = False

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and canPlace == True:
        mousePos = pygame.mouse.get_pos()
        turretList.append(Turret(turType, mousePos))
        money -= cost[turType]

def drawTurrets(turType):
    canPlace = True
    sprite1 = pygame.image.load("./textures/turret1.png")
    sprite2 = pygame.image.load("./textures/turret2.png")
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    spriteWidth = sprite1.get_width()
    spriteHeight = sprite1.get_height()

    for j in range(0, len(path[level])-1):
        if pygame.Rect(mouseX - spriteWidth, \
                       mouseY - 2.5*spriteHeight/2, \
                       2*spriteWidth, \
                       2.5*spriteHeight).clipline(path[level][j], path[level][j+1]) != ():
            canPlace = False
            #print("DOTYK")

    for i in range(0,len(turretList)):
        if pygame.Rect(mouseX - 2*spriteWidth, \
                        mouseY - 2*spriteHeight, \
                        4*spriteWidth, \
                        4*spriteHeight).collidepoint(turretList[i].pos[0], turretList[i].pos[1]):
            
            canPlace = False

    if mouseX >= 775:
        canPlace = False

    if money < cost[turType]:
        canPlace = False

    if canPlace == True:
        if turType == 1:
            screen.blit((sprite1),(mouseX - 1/2 * sprite1.get_width(), mouseY - 1/2 * sprite1.get_height()))
        if turType == 2:
            screen.blit((sprite2),(mouseX - 1/2 * sprite2.get_width(), mouseY - 1/2 * sprite2.get_height()))

    for i in range(0, len(turretList)):
        tmpIcon = pygame.transform.rotate(turretList[i].sprite, turretList[i].angle)
        screen.blit(tmpIcon, tmpIcon.get_rect(center = turretList[i].rect.center))

def shootAnimation(i, currentTime, turTime):
    tmpRECT = pygame.image.load("./textures/fire.png").get_rect()
    trajectory = Vector2(bloonQueue[turretList[i].target].pos) - Vector2(turretList[i].pos)
    
    tmpRECT.center = turretList[i].pos + 50 * trajectory.normalize()
    if (currentTime-turTime)/1000 < 1/4:
        screen.blit(pygame.image.load("./textures/fire.png"), tmpRECT)

def turretShoot():
    
    for i in range(0,len(turretList)):
        flagTMP = False
        xTur = turretList[i].pos[0]
        yTur = turretList[i].pos[1]
        for j in range(0, len(bloonQueue)): 
            xBloon = bloonQueue[j].pos[0]
            yBloon = bloonQueue[j].pos[1]
            if sqrt((xTur-xBloon)**2 + (yTur-yBloon)**2) <= turretList[i].range and bloonQueue[j].health > 0 and flagTMP == False:
                flagTMP = True
                turretList[i].target = j
                
        if sqrt((xTur-bloonQueue[turretList[i].target].pos[0])**2 + (yTur-bloonQueue[turretList[i].target].pos[1])**2) <= turretList[i].range \
                 and bloonQueue[turretList[i].target].health > 0:
            turretList[i].angle = (180 / math.pi) * math.atan2(bloonQueue[turretList[i].target].pos[0]-turretList[i].pos[0], bloonQueue[turretList[i].target].pos[1]-turretList[i].pos[1])
            if (pygame.time.get_ticks()-turretList[i].timer)/1000 > turretList[i].speed:
                bloonQueue[turretList[i].target].health -= turretList[i].damage
                turretList[i].timer = pygame.time.get_ticks()
            shootAnimation(i, pygame.time.get_ticks(), turretList[i].timer)

def showSideMenu():
    global turType
    heart = pygame.image.load('./textures/tyskie.png')
    heart_rect = heart.get_rect()

    screen.blit(pygame.image.load('./textures/hud.png'), (775, 0))
    for i in range(0, HPoints):
        heart_rect.center = (810 + i*50, 100)
        screen.blit(pygame.image.load('./textures/tyskie.png'), heart_rect)

    moneyImg = font.render(str(money), True, text_col)
    moneyRect = moneyImg.get_rect()
    moneyRect.center = (810, 200)
    screen.blit(moneyImg, moneyRect)

    waveImg = font.render('{}/{}'.format(str(wave), len(queueDict[level])), True, text_col)
    waveRect = waveImg.get_rect()
    waveRect.center = (810, 10)
    screen.blit(waveImg, waveRect)

    if turret1_button.draw():
        turType = 1
    if turret2_button.draw():
        turType = 2

def checkWin():
    global money
    global queueFlag
    global wave
    global state
    queueFlag = False
    for i in range(0, len(bloonQueue)):
        if bloonQueue[i].health <= 0 and bloonQueue[i].prize != 0:
            money += bloonQueue[i].prize
            bloonQueue[i].prize = 0

        if bloonQueue[i].health > 0:
            queueFlag = True
        
    if queueFlag == False and wave<len(queueDict[level]):
        wave += 1
    elif queueFlag == False and wave==len(queueDict[level]):
        state = 'win'

def checkDefeat():
    global HPoints
    global state
    for i in range(0,len(bloonQueue)):
        if bloonQueue[i].pos[1] > 550 and bloonQueue[i].health > 0:
            bloonQueue[i].health = 0
            bloonQueue[i].prize = 0
            HPoints -= 1


    if HPoints <= 0:
        state = 'main menu'

#health "bar" and game over screen
# def health():
#     #initial image positions
#     heart1 = pygame.image.load('./textures/tyskie.png')
#     heart2 = pygame.image.load('./textures/tyskie.png')
#     heart3 = pygame.image.load('./textures/tyskie.png')
#     game_over = pygame.image.load('game_over.png')
#     hud = pygame.image.load('./textures/hud.png')
#     heart1_rect = heart1.get_rect()
#     heart2_rect = heart2.get_rect()
#     heart3_rect = heart3.get_rect()
#     game_over_rect=game_over.get_rect()
#     heart1_rect.center = (910, 100)
#     heart2_rect.center = (860, 100)
#     heart3_rect.center = (810, 100)
#     game_over_rect.center = (-1000, -1000)

# #removing hearts when baloon makes it to the end with game over screen when all hearts are gone
#     for i in range(0, len(bloonQueue)):
#         if bloonQueue[i].pos[1] > 550 and bloonQueue[i].health > 0 and heart1_rect.center != (-800,-20):
#             heart1_rect.center = (-800,-20)
#         elif bloonQueue[i].pos[1] > 550 and bloonQueue[i].health > 0 and heart2_rect.center != (-850, -20):
#             heart2_rect.center = (-850, -20)
#         elif bloonQueue[i].pos[1] > 550 and bloonQueue[i].health > 0 and heart3_rect.center != (-900, -20):
#             heart3_rect.center = (-900, -20)
#             game_over_rect.center = (500, 250)
#     screen.blit(hud, (775, 0))
#     screen.blit(heart1, heart1_rect)
#     screen.blit(heart2, heart2_rect)
#     screen.blit(heart3, heart3_rect)
#     screen.blit(game_over, game_over_rect)


def drawPause():
    pygame.draw.rect(surface,(128,128,128,150),[0,0,1000,500])
    screen.blit(surface,(0,0))
    screen.blit(pygame.image.load('./textures/pause.png'),(0,0))

def checkPause(event):
    global pause
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if pause:
                pause = False
            else:
                pause = True

def checkQuit(event):
    #checks if the quit button has been pressed
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def restart():
    global HPoints
    global money
    global turType
    global wave
    global level
    global bloonQueue
    global turretList

    HPoints = 3
    money = 100
    turType = 1
    wave = 1
    level = 1
    bloonQueue = []
    turretList = []

#setup vaules
screen_width = 1000
screen_height = 500
fpsClock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont("Arial", 40)
text_col = (0, 0, 0)

#creation of lists of bloons and turrets
bloonQueue = []
turretList = []


#setup
screen = pygame.display.set_mode((screen_width, screen_height))
#setup of this transparent screen which appears when pause is True
surface = pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)

pygame.display.set_caption('Bloons TD 7')
#pygame.display.set_icon(pygame.image.load("panda.png"))



#setting the balloon path
path = {
    1:[
    (700, 0),
    (700, 100),
    (100, 100),
    (100, 400),
    (300, 400),
    (300, 250),
    (700, 250),
    (700, 400),
    (500, 400),
    (500, 500),
    (500, 100000)
    ]
}

#setting the balloon queues for the game levels and waves
queueDict = {
    1:{
        1:"111",
        2:"2111"
    },
    2:{
        1:"121212111111",
        2:"222222"
    }
}


#setting turret costs
cost = {
    1:30,
    2:40
}

#load background image
background = pygame.image.load("./textures/background.png")


#starting game state
state = "main menu"
play_img = pygame.image.load('./textures/play.png').convert_alpha()
set_img = pygame.image.load('./textures/option.gif').convert_alpha()
exit_img = pygame.image.load('./textures/exit.png').convert_alpha()
but_img = pygame.image.load('./textures/back.gif').convert_alpha()
#state = "game"

#global variables in control of gameplay
HPoints = 3
money = 100
turType = 1
wave = 1
level = 1



#starting pause state
pause = False

#starting queue flag state
queueFlag = False

#starting start flag state
startFlag = True


start_button = Button(350, 50, pygame.image.load('./textures/play.png').convert_alpha(), 0.7 )
exit_button = Button(320, 350, pygame.image.load('./textures/exit.png').convert_alpha(), 0.7 )
turret1_button = Button(810, 250, pygame.image.load('./textures/exit.png').convert_alpha(), 0.2 )
turret2_button = Button(810, 300, pygame.image.load('./textures/exit.png').convert_alpha(), 0.2 )


#button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
    
start_button = Button(350, 50, play_img, 0.7 )
settings_button = Button(370, 185, set_img, 0.7)
exit_button = Button(320, 350, exit_img, 0.7 )
back_button = Button(350, 350, but_img, 0.7)
#main loop
while True:

    if state == 'game':
        if not queueFlag:
            createQueue()
            queueFlag = True
        screen.blit(background, (0,0))
        #screen.fill('chocolate')
        #pygame.draw.lines(screen, 'black', False, path[level])
        #When pause = False, everything as regular
        if not pause:
            bloonMove()
            drawTurrets(turType)
            turretShoot()

        if pause:
            drawPause()
            

        showSideMenu()
        checkDefeat()
        checkWin()
        for event in pygame.event.get():
            createTurret(turType, event)
            checkQuit(event)
            checkPause(event)
            #KURWA nie dziala jak zrobilem funkcje checkPause(event,pause) wiec wrzucam tak
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pause:
                        pause = False
                    else:
                        pause = True


    elif state == 'main menu':
        screen.fill((202, 228, 241))
            
        if start_button.draw():
            state = "game"
        if settings_button.draw():
            state = 'settings'
            restart()
        if exit_button.draw():
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            checkQuit(event)

    elif state == 'game over':
        screen.fill((202, 228, 241))
            
        if start_button.draw():
            state = "game"
            restart()
        if exit_button.draw():
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            checkQuit(event)
    
    elif state == 'win':
        screen.fill((202, 228, 241))
            
        if start_button.draw():
            state = "game"
            restart()
        if exit_button.draw():
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            checkQuit(event)
            checkPause(event)
        #Pause screen
        if pause == True:
            drawPause()
            screen.blit(pygame.image.load('pause.png'),(0,0))
    elif state == 'settings':
        screen.fill((255,255,255))
        
        
        if back_button.draw():
            state = "main menu"    
        for event in pygame.event.get():
            createTurret(turType, event)
            checkQuit(event)
            checkPause(event)        
        
    fpsClock.tick(fps)
    pygame.display.update()
    