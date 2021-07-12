"""SPECIAL NOTE: Im aware to more experienced programmers that there are probably much better ways to handle a
lot of the things I'm working on here, but its a learning experience. Any advice is welcome, please fork and
create a pull request if you see anything that can be changed that you think would be beneficial"""

import pygame
from pygame.locals import *
from game_classes import *
import os
import random

BLACK = (0, 0, 0)

UP_KEYS = [pygame.K_w, pygame.K_UP]
DOWN_KEYS = [pygame.K_s, pygame.K_DOWN]
LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]

# ------------------------Initialize pygame base----------------------------------- #

pygame.init()
screen = pygame.display.set_mode((900, 800))

# ----------------------Load in non class specific images-------------------------- #

bg = pygame.image.load('Assets/hillbg.png').convert_alpha()

# ----------------Initialize sound mixer and load in audio------------------------- #

pygame.mixer.init()
pygame.mixer.set_num_channels(16)
pygame.mixer.music.load('Assets/gametheme.ogg')
pygame.mixer.music.play(-1)
plink = pygame.mixer.Sound('Assets/plink.ogg')
squawk = pygame.mixer.Sound('Assets/squawk.ogg')
crack = pygame.mixer.Sound('Assets/crack.ogg')
chirp = pygame.mixer.Sound('Assets/chirp.ogg')


# --------------------------------- MAIN GAME LOOP and OBJECT INSTANCE CREATION ------------------------ #

birb = Birb()  # Create our birb object

i = 0  # This variable is used to move the screen and get that "scrolling" effect

running = True
enemies = [Enemy() for _ in range(30)]  # Create a list of enemies
eggs = [Egg() for _ in range(6)]  # Create a list of eggs

nest = Nest()  # Create nest object
while running:
    clock = pygame.time.Clock()
    clock.tick(120)  # FPS Set to 120
    screen.fill((0, 0, 222))
    screen.blit(bg, (i, 0))
    screen.blit(bg, (900 + i, 0))
    i -= 2  # For every time loop is run, our background image x co-ordinate moves -2
    if i == -900:  # If the i value goes less than -900 (which is the width of the screen) it draws a new background
        screen.blit(bg, (900 + i, 0))
        i = 0
        nest.x = 675
        nest.y = 475
    print(birb.carrying_egg)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                birb.shoot_bullets()
    for e in enemies[:]:
        result = e.move_item(screen, birb)
        shot_result = birb.bullet_detect(e)
        crash_result = birb.crash_detection(e, birb)
        if shot_result:
            try:
                enemies.remove(e)
                plink.play()
            except ValueError:
                pass
        if result:
            enemies.remove(e)
        if crash_result:
            try:
                enemies.remove(e)
                squawk.play()
                birb.lives -= 1
                if birb.lives <= 0:
                    running = False
            except ValueError:
                pass
    if len(enemies) <= 0:
        enemies = [Enemy() for _ in range(30)]
    for e in eggs[:]:
        if e.collected:
            pass
        else:
            crash_result = birb.crash_detection(e, birb)  # Checks to see if our birb is colliding with the egg
            if crash_result:
                if birb.carrying_egg is True:
                    pass
                else:
                    e.collected = True
                    birb.carrying_egg = True
        shot_result = birb.bullet_detect(e)
        if shot_result:
            eggs.remove(e)
            crack.play()
            birb.score -= 5
        off_screen = e.move_item(screen, birb)
        if off_screen:
            if e.dropped:
                birb.carrying_egg = False
                eggs.remove(e)
            else:
                eggs.remove(e)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            if e.collected:
                e.dropped = True
                print('dropper')
                e.collected = False
                birb.carrying_egg = False
        if e.dropped:
            if e.rect.colliderect(nest.rect):
                print('basket collision')
                eggs.remove(e)
                birb.score += 5
                chirp.play()
    if len(eggs) <= 1:  # If all eggs are either destroyed, or off-screen, regenerate list of eggs
        new_eggs = [Egg() for _ in range(6)]
        for n in new_eggs:
            eggs.append(n)
    nest.move(screen)
    birb.move_bullets(screen)
    birb.draw_birb(screen)
    birb.move_birb()
    birb.print_score_lives(screen)
    pygame.display.update()
