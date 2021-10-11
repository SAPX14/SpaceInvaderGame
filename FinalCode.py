import pygame 
import random
import math 
from pygame.constants import K_RIGHT
from pygame import mixer                  # for music related module

# initialization
pygame.init()
screen = pygame.display.set_mode((800 ,600))

# background
background = pygame.image.load("spaceBg.png")

# background music
mixer.music.load("background.wav")        # loads the music to be played 
mixer.music.play(-1)                      # plays music , here '-1' is used to play music in loop

# title and display
pygame.display.set_caption("Space Invaders ")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player details
playerImg = pygame.image.load("arcadeGame.png")
playerX = 370                             # X coordinate of player
playerY = 480                             # Y coordinate of player
playerX_change = 0                        # initialized counter set to increase value by 0

# enemy details
enemyImg = []                             # empty list for enemy image
enemyX = []                               # empty list for enemy X coordinate
enemyY = []                               # empty list for enemy Y coordinate
enemyX_change = []                        # empty list for enemy X coordinate increment counter
enemyY_change = []                        # empty list for enemy Y coordinate increment counter
num_of_enemies = 10                       # variable to declare number of enemies in game
for i in range(num_of_enemies):           # for loop for respawning enimies randomly
    enemyImg.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# missile details
missileImg = pygame.image.load("missile.png")
missileX = 0                              # X coordinate of missile
missileY = 480                            # Y coordinate of missile
missileX_change = 0                       # change in X coordinate of missile ,0
missileY_change = 2                       # change in Y coordinate of missile ,2, thus to control speed of missile
missile_state = False

# score
scoreVal = 0                              # initialized score counter to 0
font = pygame.font.Font("freesansbold.ttf",32)  
textX = 10                                # score value X coordinate of display
textY = 10                                # score value Y coordinate of display

game_over_font = pygame.font.Font("freesansbold.ttf",100)   # setting font for displaying 'game over'

# function for displaying score board on screen
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
    global missile_state                    # making missile state a global variable so that it can be accessed 
    missile_state = True                    # changing the state of missile from false to true so to fire it
    screen.blit(missileImg,(x+16,y+10))

# function for detecting collision    
def isCollision(enemyX,enemyY,missileX,missileY):
    # below is the formula of distance between 2 points ,to calculate dist btwn enemy and missile
    D = math.sqrt((math.pow(missileX -enemyX,2)) + (math.pow(missileY -enemyY,2))) 
    # so if dist is less than 27 pixels the enemy will explode i.e respawn to different location
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
            if event.key == pygame.K_LEFT:   # response to left arrow key pressed (player moves left)
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:  # response to right arrow key pressed (player moves right)
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:  # response to space key pressed (player shoots missile)
                if missile_state == False:

                    missileSound = mixer.Sound("laser.wav") # so if space key pressed then shooting sound heard
                    missileSound.play()

                    missileX = playerX       # value stored in missileX so missile doesn't follows spaceship
                    fire(missileX,missileY)  # fire function activated

        if event.type == pygame.KEYUP:       # response to key released i.e KEYUP
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:   
                playerX_change = 0           # when key released player stops moving
   
    # player movement boundary restriction            
    playerX += playerX_change                # increment counter of player X coordinate

    # when player touches left boundary of screen i.e towards -ve x axis then player coordinate is set to 0 again
    if playerX <= 0:
        playerX = 0
    # when player touches right boundary of screen i.e beyond 736 pixels then player coordinate is set to 736 again   
    elif playerX >=736:
        playerX = 736 
    
    # enemy restriction and downward movement mechanics  
    for i in range(num_of_enemies):         # nested for loop for making game over
        # when enemy reaches to 440 pixel Y axis towards player then the for loop makes game over 
        if enemyY[i] > 440:
            # for loop to send enemies out of screen so that they dont appear on screen when game is over 
            for j in range(num_of_enemies):
                enemyY[j] = 2000             # setting y coordinate to 2000 i.e out of screen 
            gameOver()
            break                            # break is used to come out of loop when enemy reaches beyond player
        
        # to control movement of enemy from left to right , right to left
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
            missileY = 480                   # when collision occurs & enemy is killed , missile is reset to launch
            missile_state = False            # false here indicates that missile is ready to fire mode

            # to randomly respawn enemy after collision
            enemyX[i]  = random.randint(0,735)  
            enemyY[i]  = random.randint(50,150)

            # to print and calculate score , counter increases score by 1 when missile hits enemy
            scoreVal += 1  

        enemy(enemyX[i],enemyY[i],i)         # updates the coordinates of enemy again and again
   
    # missile reload algorithm    
    if missileY <=0 :                       
        # when missile exits screen killing or without killing enemy then it is set ready to fire again
        missileY = 480                       # missile Y coordinate set to 480 i.e inside the player spaceship
        missile_state = False    
    if missile_state == True:
        # when missile is fired ,to move it upwards the counter is decreased i.e y ordinate is decreased 
        fire(missileX,missileY)
        missileY -= missileY_change   

    # to update the coordinates of player and score in scoreboard again and again   
    player(playerX,playerY)  
    scoreBoard(textX,textY)
    pygame.display.update() # updates your display contents ,vvip line