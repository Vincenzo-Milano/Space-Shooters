from pygame import mixer
import pygame
import random
import math
 
pygame.init()
 
#Game Screen
screen = pygame.display.set_mode((600, 600))
 
#Title and icon
pygame.display.set_caption("Space Shooters")
logo = pygame.image.load('ufo.png')
pygame.display.set_icon(logo)
 
#background
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

#Character
character = pygame.image.load('character.png')
character_x = 275
character_y = 450
character_x_change = 0
character_y_change = 0

#Enemy
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6  #can change, I chose 6 

for i in range(number_of_enemies):
    enemy.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,535))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#Missle
missle = pygame.image.load('missle.png')
missleX = 0
missleY = 450
missleX_change = 0
missleY_change = 0.4
missle_state = "hold" 

#Score and Font
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 24)

textX = 485
textY = 10

#Game over Font
overFont = pygame.font.Font('freesansbold.ttf', 72)

def game_over():
    overText = overFont.render("Game Over", True, (255, 255, 255))
    screen.blit(overText, (120, 250))

def score_display(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))
 
#for character
def player(x, y):
    screen.blit(character, (x, y))

#for enemy
def villian(x, y, i):
    screen.blit(enemy[i], (x, y))

def fire_missle(x, y):
    global missle_state
    missle_state = "go"
    screen.blit(missle, (x + 16, y + 10))

def collision(enemyX, enemyY, missleX, missleY):
    distance = math.sqrt ((math.pow(enemyX - missleX,2)) + (math.pow(enemyY - missleY,2)))
    if distance < 27:
        return True
    else:
        return False

#Keeps game running and closes game
progRunning = True
while progRunning:
    screen.fill((0,130,200))
    #background image identifier
    screen.blit(background, (0, 0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            progRunning = False
 
#Clicking of keys to provide character direction 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                character_y_change = 0.2
 
            if event.key == pygame.K_LEFT:
                character_x_change = -0.2
   
            if event.key == pygame.K_RIGHT:
                character_x_change = 0.2
   
            if event.key == pygame.K_UP:
                character_y_change = -0.2

            if event.key == pygame.K_SPACE:
                if missle_state is "hold":
                    missle_sound = mixer.Sound('pew.wav')
                    missle_sound.play()
                    missleX = character_x
                    fire_missle(missleX, missleY)
 
        if event.type == pygame.KEYUP:
            character_x_change = 0
            character_y_change = 0
 
    character_x += character_x_change
    character_y += character_y_change
 
#Character Boundaries
    if character_x <= 0:
        character_x = 0
    elif character_x >= 536:
        character_x = 536
 
    if character_y <= 450:
        character_y = 450
    elif character_y >= 536:
        character_y = 536
 
#Multiple Enemy
    for i in range(number_of_enemies):
        if enemyY[i] > 410:
            for v in range(number_of_enemies):
                enemyY[v] = 1000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.28
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 536:
            enemyX_change[i] = -0.28
            enemyY[i] += enemyY_change[i]

        #Collision and Enemy Randomizer
        collisionCheck = collision(enemyX[i], enemyY[i], missleX, missleY)
        if collisionCheck:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            missleY = 475
            missle_state = "hold"
            score_val += 1
            
            enemyX[i] = random.randint(0,535)
            enemyY[i] = random.randint(50,150)
        villian(enemyX[i], enemyY[i], i)

#Missle Part
    if missleY <= 0:
        missleY = 450
        missle_state = "hold"

    if missle_state is "go":
        fire_missle(missleX, missleY)
        missleY -= missleY_change

    player(character_x, character_y)
    score_display(textX, textY)
    pygame.display.update()