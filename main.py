import pygame
import random
import math 
from pygame.constants import K_RIGHT
from pygame import mixer 
# initialization
pygame.init()
screen = pygame.display.set_mode((800 ,600))

# background
background = pygame.image.load("spaceBg.png")

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and display
pygame.display.set_caption("Space Invaders ")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player details
playerImg = pygame.image.load("arcadeGame.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy details
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# missile details
missileImg = pygame.image.load("missile.png")
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 2
missile_state = False

# score
scoreVal = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

game_over_font = pygame.font.Font("freesansbold.ttf",100)

def scoreBoard(x,y):
    score = font.render("SCORE :" + str(scoreVal) , True , (255,0,0))
    screen.blit(score ,(x,y))

# game over 
def gameOver():
    game_over = game_over_font.render("GAME OVER" , True , (255,255,255))
    screen.blit(game_over ,(80,250))

# player and enemy coordinate definition function
def player(x,y):
    screen.blit(playerImg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))       

# function for firing missile
def fire(x,y):
    global missile_state
    missile_state = True
    screen.blit(missileImg,(x+16,y+10))

# function for detecting collision    
def isCollision(enemyX,enemyY,missileX,missileY):
    D = math.sqrt((math.pow(missileX -enemyX,2)) + (math.pow(missileY -enemyY,2))) 
    if D <= 27:
        return True

# game loop
run=True
while run:
   
    # screen background color
    screen.fill((0,0,0))
    # background image to be persistent , so placed in while loop
    screen.blit(background,(0,0))
   
    # Control for all events happening
    for event in pygame.event.get():
        if event.type == pygame.QUIT:        # closes game if u press close button
            run=False
        if event.type == pygame.KEYDOWN:     # on press key response
            if event.key == pygame.K_LEFT:   # response to left arrow key pressed
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:  # response to right arrow key pressed
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:  # response to space key pressed
                if missile_state == False:
                    missileSound = mixer.Sound("laser.wav")
                    missileSound.play()
                    missileX = playerX       # value stored in missileX so missile doesn't follows spaceship
                    fire(missileX,missileY)    
        if event.type == pygame.KEYUP:       ## response to key released i.e KEYUP
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:   
                playerX_change = 0
   
    # player movement boundary restriction            
    playerX += playerX_change 
    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736 
    
    # enemy boundary restiction and downward movement mechanics  
    for i in range(num_of_enemies):  
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  
            gameOver()
            break   
        enemyX[i] += enemyX_change[i] 
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i] 
        # collision approval algorithm
        collision = isCollision(enemyX[i] ,enemyY[i] ,missileX ,missileY)
        if collision:
            collisionSound = mixer.Sound("explosion.wav")
            collisionSound.play()
            missileY = 480
            missile_state = False 
            # to respawn enemy
            enemyX[i]  = random.randint(0,735)  
            enemyY[i]  = random.randint(50,150)
            # to print and calculate score
            scoreVal += 1    
        enemy(enemyX[i],enemyY[i],i)  
   
    # missile reload algorithm    
    if missileY <=0 :
        missileY = 480
        missile_state = False    
    if missile_state == True:
        fire(missileX,missileY)
        missileY -= missileY_change   

    

    # to update the coordinates of enemy and player again and again   
    player(playerX,playerY)  
    scoreBoard(textX,textY)
    pygame.display.update() # updates your display contents ,vvip line