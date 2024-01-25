import pygame
import sys 
from pygame.math import Vector2
import math
from math import sqrt

pygame.init()
pygame.mixer.init()

class Bloon:
    def __init__(self, type):
        self.type = type
        if type == 1:
            self.health = 5
            self.speed = 2
            self.prize = 5
            self.sprite = pygame.image.load("./textures/balloon1.png")
        elif type == 2:
            self.health = 7
            self.speed = 4
            self.prize = 10
            self.sprite = pygame.image.load("./textures/balloon2.png")
        elif type == 3:
            self.health = 30
            self.speed = 1
            self.prize = 30
            self.sprite = pygame.image.load("./textures/balloon3.png")
        else:
            # Default values if type is not 1, 2, or 3
            self.health = 0
            self.speed = 2
            self.prize = 0
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
            self.speed = 1
            self.sprite = pygame.image.load("./textures/turret1.png")
        elif type == 2:
            self.damage = 2
            self.speed = 0.7
            self.sprite = pygame.image.load("./textures/turret2.png")
        else:
            # Default values if type is not 1, 2, or 3
            self.damage = 3
            self.speed = 1
            self.sprite = pygame.image.load("./textures/turret1.png")

        self.rect = self.sprite.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.range = 100
        self.timer = 0
        self.angle = 0
        self.target = 0

class Button:
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
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
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

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and canPlace == True and turType!=0:
        mousePos = pygame.mouse.get_pos()
        if not mute:
                    pygame.mixer.Sound.play(place)
        turretList.append(Turret(turType, mousePos))
        money -= cost[turType]

def drawTurrets(turType):

    canPlace = True
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    spriteWidth = 50
    spriteHeight = 50

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

    if mouseX >= 775 or money < cost[turType]:
        canPlace = False

    #draw turret preview on mouse position
    if turType == 1 and canPlace == True:
        sprite = pygame.image.load("./textures/turret1.png")
    elif turType == 2 and canPlace == True:
        sprite = pygame.image.load("./textures/turret2.png")
    elif turType == 1 and canPlace == False:
        sprite = pygame.image.load("./textures/turret1_red.png")
    elif turType == 2 and canPlace == False:
        sprite = pygame.image.load("./textures/turret2_red.png")


    #display turren range when placing
    if turType != 0 and mouseX <= 775:
        surface.fill((0, 0, 0, 0))
        pygame.draw.circle(surface, (255,0,0,100), (mouseX, mouseY), 100)
        screen.blit(surface,(0,0))
        screen.blit((sprite),(mouseX - 1/2 * spriteWidth, mouseY - 1/2 * spriteHeight))

    #draw placed turrets
    for i in range(0, len(turretList)):
        tmpIcon = pygame.transform.rotate(turretList[i].sprite, turretList[i].angle)
        screen.blit(tmpIcon, tmpIcon.get_rect(center = turretList[i].rect.center))

def displayTurretRange():
    surface.fill((0, 0, 0, 0))
    for i in range(0, len(turretList)):
        pygame.draw.circle(surface, (0,0,0,80), turretList[i].pos, turretList[i].range)
    screen.blit(surface,(0,0))

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
                if not mute:
                    pygame.mixer.Sound.play(shoot)
                turretList[i].timer = pygame.time.get_ticks()
            shootAnimation(i, pygame.time.get_ticks(), turretList[i].timer)

def showSideMenu():
    global turType
    heart = pygame.image.load('./textures/heart.png')
    heart_rect = heart.get_rect()

    screen.blit(pygame.image.load('./textures/hud.png'), (775, 0))

    for i in range(0, HPoints):
        heart_rect.center = (810 + i*50, 170)
        screen.blit(pygame.image.load('./textures/heart.png'), heart_rect)

    moneyImg = font.render(str(money), True, text_col)
    moneyRect = moneyImg.get_rect()
    moneyRect.center = (920, 75)
    screen.blit(moneyImg, moneyRect)

    waveImg = font.render('{}/{}'.format(str(wave), str(len(queueDict[level]))), True, text_col)
    waveRect = waveImg.get_rect()
    waveRect.center = (900, 30)
    screen.blit(waveImg, waveRect)

    if turret1_button.draw():
        turType = 1
    if turret2_button.draw():
        turType = 2
    if turretCancel_button.draw():
        turType = 0

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
            if not mute:
                pygame.mixer.Sound.play(pop)

        if bloonQueue[i].health > 0:
            queueFlag = True
        
    if queueFlag == False and wave<len(queueDict[level]):
        wave += 1
    elif queueFlag == False and wave==len(queueDict[level]):
        if not mute:
                    pygame.mixer.Sound.play(happyWin)
        state = 'win'

def checkDefeat():
    global HPoints
    global state
    global queueFlag
    for i in range(0,len(bloonQueue)):
        if bloonQueue[i].pos[1] > 550 and bloonQueue[i].health > 0:
            bloonQueue[i].health = 0
            bloonQueue[i].prize = 0
            HPoints -= 1
            if not mute:
                pygame.mixer.Sound.play(loseHeart)


    if HPoints <= 0:
        queueFlag = False
        state = 'game over'

def drawPause():
    pygame.draw.rect(surface,(128,128,128,150),[0,0,1000,500])
    screen.blit(surface,(0,0))
    screen.blit(pygame.image.load('./textures/pause.png'),(0,0))

def checkPause(event):
    global pause
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        pause = not pause

def checkQuit(event):
    #checks if the quit button has been pressed
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

#setup of base values
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
    turType = 0
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

#set window name and icon
pygame.display.set_caption('Bloons TD 0.5')
pygame.display.set_icon(pygame.image.load("./textures/balloon1.png"))

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
        1:"11101110111",
        2:"2211111122",
        3:"322221111011110111101111",
        4:"22111311131111111111"
    },
    2:{
        1:"121212111111",
        2:"222222"
    }
}

#setting turret costs
cost = {
    0:0,
    1:30,
    2:50
}

#load background image
background = pygame.image.load("./textures/background.png")
backgroundMM = pygame.image.load("./textures/backgroundMM.png")

#load sounds
pop = pygame.mixer.Sound('./sounds/pop.mp3')
loseHeart = pygame.mixer.Sound('./sounds/bruh.mp3')
shoot = pygame.mixer.Sound('./sounds/shoot.mp3')
place = pygame.mixer.Sound('./sounds/place.mp3')
happyWin = pygame.mixer.Sound('./sounds/monkeyWin.wav')

#starting game state
state = "main menu"

#global variables in control of gameplay
# HPoints = 3
# money = 100
# turType = 0
# wave = 1
# level = 1

#starting pause state
pause = False

#starting mute state
mute = False

#starting queue flag state
queueFlag = False

#starting start flag state
startFlag = True

#main menu buttons
start_button = Button(500, 220, pygame.image.load('./textures/play.png').convert_alpha(), 0.7 )
exit_button = Button(500, 380, pygame.image.load('./textures/exit.png').convert_alpha(), 0.7 )
settings_button = Button(500, 300, pygame.image.load('./textures/settings.png').convert_alpha(), 0.7)
#settings button
back_button = Button(350, 450, pygame.image.load('./textures/back.png').convert_alpha(), 0.7)
mute_button = Button(500, 200, pygame.image.load('./textures/mute.png').convert_alpha(), 0.7)
check = pygame.image.load('./textures/mark.png')
#in game buttons
turret1_button = Button(887, 270, pygame.image.load('./textures/turretButton1.png').convert_alpha(), 1 )
turret2_button = Button(887, 350, pygame.image.load('./textures/turretButton2.png').convert_alpha(), 1 )
turretCancel_button = Button(887, 430, pygame.image.load('./textures/turretButtonCancel.png').convert_alpha(), 1 )
#win/lose buttons
retry_button = Button(350, 300, pygame.image.load('./textures/retry.png').convert_alpha(), 1 )
exitWL_button = Button(600, 300, pygame.image.load('./textures/BackMainMenu.png').convert_alpha(), 1 )

pygame.mixer.music.load("./sounds/background.mp3") 
pygame.mixer.music.play(-1,0.0)

#main loop
while True:
    if state == 'game':
        if not queueFlag:
            createQueue()
            queueFlag = True
        screen.blit(background, (0,0))
        #pygame.draw.lines(screen, 'black', False, path[level])
        #When pause = False, everything as regular
        if not pause:
            bloonMove()
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                displayTurretRange()
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

    elif state == 'main menu':
        screen.blit(backgroundMM, (0,0))
        queueFlag = False
        if start_button.draw():
            state = "game"
            restart()
        if settings_button.draw():
            state = 'settings'
        if exit_button.draw():
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            checkQuit(event)

    elif state == 'game over':
        screen.blit(background, (0,0))
        screen.blit(pygame.image.load(('./textures/lose.png')), (232,150))
        showSideMenu()
        if retry_button.draw():
            state = "game"
            restart()
        if exitWL_button.draw():
            state = "main menu"
        
        for event in pygame.event.get():
            checkQuit(event)
    
    elif state == 'win':
        screen.blit(background, (0,0))
        screen.blit(pygame.image.load(('./textures/congratulations.png')), (232,150))
        showSideMenu()
        if retry_button.draw():
            state = "game"
            restart()
        if exitWL_button.draw():
            state = "main menu"
        
        for event in pygame.event.get():
            checkQuit(event)
            
    elif state == 'settings':
        screen.blit(backgroundMM, (0,0))
        if mute_button.draw():
            mute = not mute
            
        if mute == True:
            pygame.mixer.music.pause()
            screen.blit(check, (330,150))

        else: 
            pygame.mixer.music.unpause()
        if back_button.draw():
            state = "main menu"    
        for event in pygame.event.get():
            checkQuit(event)       
        
    fpsClock.tick(fps)
    pygame.display.flip()
    