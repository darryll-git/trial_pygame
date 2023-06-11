import pygame
import random
import math
from pygame import mixer
# initialize pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800,600))
#background
background = pygame.image.load('forest.png')
#background sound
mixer.music.load('back-music.wav')
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("the quest of chu")
icon = pygame.image.load('pikachu.png')
pygame.display.set_icon(icon)

#enemy
pikaimg = []
pikaX = []
pikaY = []
pikaX_change = []
pikaY_change = []
num_pika = 6

for i in range(num_pika):
    pikaimg.append(pygame.image.load('pikach.png'))
    pikaX.append(random.randint(0, 736))
    pikaY.append(random.randint(20, 150))
    pikaX_change.append(2)
    pikaY_change.append(40)


def pika(x,y,i):
    screen.blit(pikaimg[i] , (x,y))

#banana
#ready - you cant see the bullet on the screen
#fire - the bullet is moving
bananaimg = pygame.image.load('banana.png')
bananaX = 0
bananaY = 480
bananaX_change = 0
bananaY_change = 5
banana_state = 'ready'
def banana(x,y):
    global banana_state
    banana_state = 'fire'
    screen.blit(bananaimg,(x+16,y+10))

score = 0

#player
playerimg = pygame.image.load('monkey.png')
playerX = 370
playerY = 480
playerX_change = 0
def player(x,y):
    screen.blit(playerimg , (x,y))

def collision(pikaX,pikaY,bananaX,bananaY):
    distance = math.sqrt(math.pow(pikaX-bananaX,2)+math.pow(pikaY-bananaY,2))
    if distance < 30:
        return True
    else:
        return False

#font
score_val = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render('score:'+ str(score_val),True ,(255,155,0))
    screen.blit(score,(x,y))

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 155, 155))
    screen.blit(over_text, (200, 250))


# Game Loop
running = True
while running:
    # RGB - red , green , blue
    screen.fill((135, 206, 235))
    #background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whther left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if banana_state == "ready":
                 banana_sound = mixer.Sound('laser.wav')
                 banana_sound.play()
                 bananaX = playerX
                 banana(bananaX,bananaY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    #boundary and movement player
    playerX += playerX_change
    if playerX<=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    #boundary and movement pika
    for i in range(num_pika):
        #Game over
        if pikaY[i] > 440:
            for j in range(num_pika):
                pikaY[j] = 2000
            game_over_text()
            break
        pikaX[i] += pikaX_change[i]
        if pikaX[i] <= 0:
            pikaX_change[i] = 2
            pikaY[i] += pikaY_change[i]
        elif pikaX[i] >= 736:
            pikaX_change[i] = -1
            pikaY[i] += pikaY_change[i]
        # collision
        colli = collision(pikaX[i], pikaY[i], bananaX, bananaY)
        if colli:
            colli_sound = mixer.Sound('explosion.wav')
            colli_sound.play()
            bananaY = 480
            banana_state = 'ready'
            score_val += 1
            pikaX[i] = random.randint(0, 736)
            pikaY[i] = random.randint(20, 150)

        pika(pikaX[i], pikaY[i],i)

    #bullet movement
    if bananaY <= 0:
        bananaY = 480
        banana_state = 'ready'
    if banana_state == "fire":
        banana(bananaX,bananaY)
        bananaY -= bananaY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
