import math
import random
import pygame
import pygame_menu
from pygame import mixer

#initializes the game using pygame
pygame.init()

#screen size
screen = pygame.display.set_mode((800, 600))

#background image and menu bar
background = pygame.image.load("./images/Very_Black_screen.png")

#game audio
mixer.music.load("./audio/background.wav")
mixer.music.play(-1)

#name of the game and game icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./images/ufo.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("./images/Laser_Cannon.png")
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

enemy_R = 1
enemy_L = -1

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("./images/enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(20)


#the laser
laserImg = pygame.image.load("./images/laser.png")
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 10
laser_state = "ready"

#scoring

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def victory_text():
    if victory == True:
        over_text = font.render("Victory!", True, (255, 255, 255))
        screen.blit(over_text, (355, 250))

def play_again():
    if game_over == True or victory == True:
        yesNo = font.render("Press y to play again or n to quit.", True, (255, 255, 255))
        screen.blit(yesNo, (355, 200))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - laserX, 2) + (math.pow(enemyY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False


#game loop that executes the game 

running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if  laser_state is "ready":
                    laserSound = mixer.Sound("./audio/laser.wav")
                    laserSound.play()
                    # Get the current x cordinate of the spaceship
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
   


    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            game_over_text()
            game_over = True
            break


        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0: 
            enemyX_change[i] = enemy_R
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736: 
            enemyX_change[i] = enemy_L
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosionSound = mixer.Sound("./audio/explosion.wav")
            explosionSound.play() 
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state is "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
