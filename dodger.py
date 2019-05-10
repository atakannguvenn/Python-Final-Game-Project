import pygame, random, sys
from pygame.locals import *
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
TEXTCOLOR = (255, 99, 71)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 30
BADDIEMAXSIZE = 60
BADDIEMINSPEED = 4
BADDIEMAXSPEED = 10
ADDNEWBADDIERATE = 10
PLAYERMOVERATE = 10

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
start_ticks=pygame.time.get_ticks()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('dying.wav')
pygame.mixer.music.load('POL-gold-gryphons-long.mp3')

# set up images
playerImage = pygame.image.load('axemvq.png')
playerRect = playerImage.get_rect()
# trying to do animation in images
baddieImage = pygame.image.load('Rock.png')
spriteImage = pygame.image.load("wood.png")
backimage = pygame.image.load("background.png")
backimg2 = pygame.image.load("background2.png")
backimg3 = pygame.image.load("background3.png")
openingimage = pygame.image.load("opening.jpg")
level3img = pygame.image.load("scared.png")
# show the "Start" screen
windowSurface.blit(openingimage, [0, 0])
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3 + 100), (WINDOWHEIGHT / 3))
drawText('Atakan & Annie Edition', font, windowSurface, (WINDOWWIDTH / 4.2 + 60), (WINDOWHEIGHT / 3 + 50))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3 + 10) , (WINDOWHEIGHT / 3) + 100)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    baddies = []
    sprites = []
    level3 = []
    score = 0
    countdown = 30
    level = 1
    jumping = 0
    playerRect.topleft = (512 , 610)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    def player_in_air():
        if (playerRect.topleft(610)) == False:
            return True
        else:
            return False

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score
        countdown = (level * 15) - (score / 46)

        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('k'):
                    reverseCheat = True
                if event.key == ord('l'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                    """
                if event.key == K_UP or event.key == ord('w') or K_SPACE:
                    jumping = 1
                    if player_in_air() == False:
                        sprite_Y = getY() + 10
                #    moveDown = False
                #    moveUp = True
                #if event.key == K_DOWN or event.key == ord('s'):
                #    moveUp = False
                #    moveDown = True
                    """
            if event.type == KEYUP:
                if event.key == ord('k'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('l'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
            '''''''''
            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
            '''''''''
        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }
            if level >= 2:
                newsprite = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                             'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                             'surface': pygame.transform.scale(spriteImage, (baddieSize, baddieSize)),
                             }
                sprites.append(newsprite)
            if level >= 3:
                newnewsprite = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                             'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface': pygame.transform.scale(level3img, (baddieSize, baddieSize)),
                             }
                level3.append(newnewsprite)
            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        #pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for a in sprites:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(random.randint(3,10), random.randint(5,10))
            elif reverseCheat:
                a['rect'].move_ip(0, -5)
            elif slowCheat:
                a['rect'].move_ip(0, 1)

        for a in level3:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(random.randint(-10, -3), random.randint(5,10))
            elif reverseCheat:
                a['rect'].move_ip(0, -5)
            elif slowCheat:
                a['rect'].move_ip(0, 1)



         # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)
        for a in sprites[:]:
            if a['rect'].top > WINDOWHEIGHT:
                sprites.remove(a)
        for a in level3[:]:
            if a['rect'].top > WINDOWHEIGHT:
                level3.remove(a)
        if countdown == 0:
            if ADDNEWBADDIERATE == 10:
                ADDNEWBADDIERATE = ADDNEWBADDIERATE - 2
            BADDIEMAXSPEED += 2
            level = level + 1

        # Draw the game world on the window.
        if level == 1:
            windowSurface.blit(backimage, [0, 0])
        if level == 2:
            windowSurface.blit(backimg2, [0, 0])
        if level >= 3:
            windowSurface.blit(backimg3, [0, 0])


        # Draw the score and top score.
        drawText('Time: %d' % (countdown), font, windowSurface, 10, 80)
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Level %d' % (level), font, windowSurface, 450, 20)


        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
        for b in sprites:
            windowSurface.blit(b['surface'], b['rect'])
        for b in level3:
            windowSurface.blit(b['surface'], b['rect'])
        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            level = 1
            BADDIEMAXSPEED = 10
            ADDNEWBADDIERATE = 10
            if score > topScore:
                topScore = score # set new top score
            break

        if playerHasHitBaddie(playerRect, sprites):
            level = 1
            BADDIEMAXSPEED = 10
            ADDNEWBADDIERATE = 10
            if score > topScore:
                topScore = score # set new top score
            break

        if playerHasHitBaddie(playerRect, level3):
            level = 1
            BADDIEMAXSPEED = 10
            ADDNEWBADDIERATE = 10
            if score > topScore:
                topScore = score # set new top score
            break
        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 2.5))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 2.5) - 80, (WINDOWHEIGHT / 2.5) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
