import pygame
import sys
from pygame.math import Vector2

pygame.init()

class Bloon:
    def __init__(self, type):
        self.type = type
        if type == 1:
            self.health = 10
            self.speed = 2
            self.sprite = pygame.image.load("./textures/balloon1.png")
        elif type == 2:
            self.health = 2
            self.speed = 4
            self.sprite = pygame.image.load("./textures/balloon2.png")
        elif type == 3:
            pass
        else:
            # Default values if type is not 1, 2, or 3
            self.health = 10
            self.speed = 5
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
            self.range = 50
            self.speed = 4
            self.sprite = pygame.image.load("./textures/turret1.png")
        elif type == 2:
            self.damage = 3
            self.range = 50
            self.speed = 5
            self.sprite = pygame.image.load("./textures/turret1.png")
        elif type == 3:
            pass
        else:
            # Default values if type is not 1, 2, or 3
            self.damage = 3
            self.range = 50
            self.speed = 5
            self.sprite = pygame.image.load("./textures/turret1.png")

        self.rect = self.sprite.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.target = 0

    
def createQueue():
    global bloonQueue
    for i in range(0,len(queue)):
            bloonQueue.append(Bloon(int(queue[i])))
    for j in range(0, len(bloonQueue)):
        bloonQueue[j].pos[1] -= j * bloonQueue[j].rect.height
        bloonQueue[j].rect.center = bloonQueue[j].pos

def bloonMove():
    
    
    for i in range(0,len(bloonQueue)):
        
        #wayToTarget = Vector2([0,0]) --- residue

        wayToTarget = Vector2(path[bloonQueue[i].target]) - Vector2(bloonQueue[i].pos)
        
        if wayToTarget.length() <= bloonQueue[i].speed:
            bloonQueue[i].pos = path[bloonQueue[i].target]
            bloonQueue[i].rect.center = bloonQueue[i].pos
            bloonQueue[i].target += 1

        
        bloonQueue[i].pos += bloonQueue[i].speed * wayToTarget.normalize()
        bloonQueue[i].rect.center = bloonQueue[i].pos

        screen.blit(bloonQueue[i].sprite, bloonQueue[i].rect)
    
def createTurret(turType, event):
    canPlace = True
    sprite1 = pygame.image.load("./textures/turret1.png")
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    spriteWidth = sprite1.get_width()
    spriteHeight = sprite1.get_height()

    for j in range(0, len(path)-1):
        if pygame.Rect(mouseX - spriteWidth, \
                       mouseY - 2.5*spriteHeight/2, \
                       2*spriteWidth, \
                       2.5*spriteHeight).clipline(path[j], path[j+1]) != ():
            canPlace = False

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and canPlace == True:
        mousePos = pygame.mouse.get_pos()
        turretList.append(Turret(turType, mousePos))

def drawTurrets(turType):
    canPlace = True
    sprite1 = pygame.image.load("./textures/turret1.png")
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    spriteWidth = sprite1.get_width()
    spriteHeight = sprite1.get_height()

    for j in range(0, len(path)-1):
        if pygame.Rect(mouseX - spriteWidth, \
                       mouseY - 2.5*spriteHeight/2, \
                       2*spriteWidth, \
                       2.5*spriteHeight).clipline(path[j], path[j+1]) != ():
            canPlace = False
            #print("DOTYK")

    if canPlace == True:
        if turType == 1:
            screen.blit((sprite1),(mouseX - 1/2 * sprite1.get_width(), mouseY - 1/2 * sprite1.get_height()))

    for i in range(0, len(turretList)):
        screen.blit(turretList[i].sprite, turretList[i].rect)

def checkQuit(event):
    #checks if the quit button has been pressed
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

#setup vaules
screen_width = 1000
screen_height = 500
fpsClock = pygame.time.Clock()
fps = 60

bloonQueue = []
turretList = []


#setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bloons TD 7')
#pygame.display.set_icon(pygame.image.load("panda.png"))


#setting the balloon path
path = [
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

#setting the balloon queue for the game
queue = "211111111112"


#load background image
#background = pygame.image.load("background.png")

#starting game state
state = "game"
turType = 1


createQueue()
print(bloonQueue[0].rect.h, bloonQueue[0].rect.w)

#main loop
while True:
    if state == 'game':
        #screen.blit(background, (0,0))
        screen.fill('chocolate')
        pygame.draw.lines(screen, 'black', False, path)
        bloonMove()
        drawTurrets(turType)
        for event in pygame.event.get():
            createTurret(turType, event)
            checkQuit(event)

    fpsClock.tick(fps)
    pygame.display.update()
    