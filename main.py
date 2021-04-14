import random  # for generating random numbers
import sys  # we will use sys.exit to exit the programm
import pygame
from pygame.locals import *  # basic pygame imports


# Global varieables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
# here pygame gives the display area by the given variable.
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/bird.png'
BACKGROUND = 'C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/background.png'
PIPE = 'C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/pipe.png'


def welcomeScreen():
    """
    Shows welcome images on the screen

    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2.5)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()))
    messagey = int(SCREENHEIGHT/3.7)

    basex = 0
    while True:
        for event in pygame.event.get():    # it tells which button user pressed in keyboard

            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame/quit()
                sys.exit()

            # if user presses space or up key, start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0

    # create 2 pipes for blitting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()

    #my list of upper pipes
    upperPipes=[
        {'x':SCREENWIDTH+150,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+150+SCREENWIDTH/2,'y':newPipe2[0]['y']}
    ]
    #list of lower pipes
    lowerPipes=[
        {'x':SCREENWIDTH+150,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+150+SCREENWIDTH/2,'y':newPipe2[1]['y']}
    ]

    pipeVelx=-4

    playerVely=-9
    playermaxVely=19
    playerminVely=-8
    playerAccy=0.8

    playerFlapAccv=-8   #velocity of bird while flapping
    playerFlapped=False   #it is true only when the bird is flaping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playerVely=playerFlapAccv
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()
        
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes) #this function will return true if the player is crashed
        if crashTest:
            return
        
        #check for score
        playerMidPos=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos=pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score+=1
                print(f"Your score is {score}")
                # GAME_SOUNDS['point'].play()     /////////////i am removing this sound because i didnt get score increasing sound
                

        if playerVely<playermaxVely and not playerFlapped:
            playerVely+=playerAccy
        if playerFlapped:
            playerFlapped= False

        playerHieght=GAME_SPRITES['player'].get_height()
        playery=playery+min(playerVely,GROUNDY-playery-playerHieght)

        #move pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):  #zip joins the values of 2 lists   like (1:1,5:2,2:9)
            upperPipe['x']+=pipeVelx
            lowerPipe['x']+=pipeVelx

        #Add a new pipe when the first pipe about to cross the leftmost part of the screen 
        if 0<upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])   
            lowerPipes.append(newpipe[1])



        #if the pipe is out of the screen remove it
        if upperPipes[0]['x'] <- GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
 
        #lets blit our sprites
        #background
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        #pipes blitting
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))

        #base
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        #player
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

        myDigits=[int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()
        Xoffset=(SCREENWIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)
                                                    



def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery > GROUNDY -30 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHieght=GAME_SPRITES['pipe'][0].get_height()
        if (playery<pipeHieght+pipe['y'] and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

                        
        
    for pipe in lowerPipes:
        if (playery+GAME_SPRITES['player'].get_height()> pipe['y'] and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    
        
    return False



def getRandomPipe():
    """
    generate positions of 2 pipes(one bottom straight and one top rotated) for blitting on the screen 
    """
    pipeHieght=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3.6
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex=SCREENWIDTH+10
    y1=pipeHieght-y2+offset
    pipe=[
        {'x':pipex,'y':-y1}, #upper pipe
        {'x':pipex,'y':y2}  #lower pipe
    ]
    return pipe


if __name__ == '__main__':
    # this will be the main point from where our game will start
    pygame.init()  # itintialize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird by Vaibhav NB')

    GAME_SPRITES['numbers'] =  (
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/9.png').convert_alpha(),
    )

                               

    GAME_SPRITES['message'] = pygame.image.load(
        'C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        'C:/Users/User/Desktop/pythonProject/flappy bird/gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(
            PIPE).convert_alpha(), 180),   pygame.image.load(PIPE).convert_alpha()
    )

    # game sounds

    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/audio/hit.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/audio/point.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/audio/swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:/Users/User/Desktop/pythonProject/flappy bird/gallery/audio/wing.mp3')
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()  # shows welcome screen to the user untill he presses a button
        mainGame()  # this is the main game function
