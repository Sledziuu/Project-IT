import pygame#gowno123
import sys
#lol
pygame.init()

class Bloon:
    def __init__(self, type):
        self.type = type
        if type == 1:
            self.health = 10
            self.speed = 5
        elif type == 2:
            pass
        elif type == 3:
            pass
        else:
            # Default values if type is not 1, 2, or 3
            self.health = 10
            self.speed = 5
        self.sprite = pygame.image.load()
        self.pos = (0, 0)

    


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


#setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bloons TD 7')
#pygame.display.set_icon(pygame.image.load("panda.png"))

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
    (500, 500)
]

targets = {
    1 : (700, 100),
    2 : (100, 100),
    3 : (100, 400),
    4 : (300, 400),
    5 : (300, 250),
    6 : (700, 250),
    7 : (700, 400),
    8 : (500, 400),
    9 : (500, 500)
}

#load background image
#background = pygame.image.load("background.png")

#starting game state
state = "game"



#main loop
while True:
    
    if state == 'game':
        #screen.blit(background, (0,0))
        screen.fill('chocolate')
        pygame.draw.lines(screen, 'black', False, path)
        for event in pygame.event.get():
            checkQuit(event)

    fpsClock.tick(fps)
    pygame.display.update()
    