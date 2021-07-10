import pygame
import os
import random

pygame.init()
screen = pygame.display.set_mode((900, 800))
bg = pygame.image.load('Assets/hillbg.png').convert_alpha()
seed = pygame.image.load('Assets/seed.png').convert_alpha()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
pygame.mixer.music.load('Assets/gametheme.mp3')
pygame.mixer.music.play(-1)
plink = pygame.mixer.Sound('Assets/plink.ogg')
squawk = pygame.mixer.Sound('Assets/squawk.ogg')
crack = pygame.mixer.Sound('Assets/crack.ogg')
chirp = pygame.mixer.Sound('Assets/chirp.ogg')


class Bullet:
    def __init__(self, x, y):
        self.img = pygame.image.load('Assets/seed.png').convert_alpha()
        self.x = x
        self.y = y
        self.vel = 20
        self.bullet_rect = pygame.Rect(self.x, self.y, 10, 10)

    def off_screen(self):
        if self.x > 880:
            return True


class Enemy:
    def __init__(self):
        self.img = pygame.image.load('Assets/drone.png').convert_alpha()
        self.x = random.randint(1000, 6000)
        self.y = random.randint(100, 500)
        self.vel = 3
        self.rect = pygame.Rect(self.x, self.y + 20, 100, 60)
        self.friendly = False

    def move_item(self, s, b):
        self.x -= self.vel
        self.update_rect()
        # pygame.draw.rect(s, (255, 0, 0), self.rect, 2)
        s.blit(self.img, (self.x, self.y))
        if self.x < -50:
            return True

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y + 20, 100, 60)


class Power(Enemy):
    def __init__(self):
        super().__init__()
        self.x = random.randint(1000, 3000)
        self.y = random.randint(0, 400)
        self.vel = -2
        self.collected = False
        self.rect = pygame.Rect(self.x + 15, self.y + 7, 70, 87)
        self.img = pygame.image.load('Assets/egg.png').convert_alpha()

    def update_rect(self):
        self.rect = pygame.Rect(self.x + 15, self.y + 7, 70, 87)

    def move_item(self, s, b):
        if self.collected is False:
            self.x -= 2
            self.update_rect()
            # pygame.draw.rect(s, (255, 0, 0), self.rect, 2)
            s.blit(self.img, (self.x, self.y))
            if self.x < 50:
                return True
        else:
            self.x, self.y = b.x, b.y + 60
            b.slot = True
            self.update_rect()
            s.blit(self.img, (self.x, self.y))


class Birb:
    def __init__(self):
        self.img = pygame.image.load('Assets/birb.png').convert_alpha()
        self.x = 50
        self.y = 300
        self.vel = 10
        self.slot = False
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.bullets = []
        self.score = 0
        self.lives = 5
        self.friendly = True

    def draw_birb(self, s):
        s.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(s, (255, 0, 0), self.rect, 2)

    def shoot_bullets(self):
        bullet = pygame.Rect(self.x + 75, self.y + 35, 10, 10)
        self.bullets.append(bullet)

    def move_bullets(self, s):
        for b in self.bullets:
            b.x += 20
            s.blit(seed, (b.x, b.y))
            if b.x > 890:
                self.bullets.remove(b)

    def collision_detect(self, item):
        for b in self.bullets:
            if b.colliderect(item.rect):
                self.bullets.remove(b)
                return True

    def crash_detection(self, item):
        if self.rect.colliderect(item.rect):
            return True

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def move_birb(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.vel
            self.update_rect()
        if keys[pygame.K_d] and self.x < 800:
            self.x += self.vel
            self.update_rect()
        if keys[pygame.K_w] and self.y - self.vel > 0:
            self.y -= self.vel
            self.update_rect()
        if keys[pygame.K_s] and self.y + self.vel < 800 - 100:
            self.y += self.vel
            self.update_rect()


birb = Birb()

i = 0
running = True
test_rect = pygame.Rect(675, 475, 140, 50)
enemies = [Enemy() for _ in range(30)]
eggs = [Power() for _ in range(6)]

while running:
    clock = pygame.time.Clock()
    clock.tick(120)
    screen.fill((0, 0, 222))
    screen.blit(bg, (i, 0))
    screen.blit(bg, (900 + i, 0))
    i -= 2
    test_rect.x -= 2
    if i == -900:
        screen.blit(bg, (900 + i, 0))
        i = 0
        test_rect.x = 675
        test_rect.y = 475
    pygame.draw.rect(screen, (255, 0, 0), test_rect, 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                birb.shoot_bullets()
    # for e in enemies[:]:
    #     result = e.move_item(screen)
    #     shot_result = birb.collision_detect(e)
    #     crash_result = birb.crash_detection(e)
    #     if shot_result:
    #         try:
    #             enemies.remove(e)
    #             plink.play()
    #         except ValueError:
    #             pass
    #     if result:
    #         enemies.remove(e)
    #     if crash_result:
    #         try:
    #             enemies.remove(e)
    #             squawk.play()
    #             birb.lives -= 1
    #         except ValueError:
    #             pass
    # if len(enemies) <= 0:
    #     enemies = [Enemy() for _ in range(30)]
    for p in eggs[:]:
        result = p.move_item(screen, birb)
        crash_result = birb.crash_detection(p)
        shoot_result = birb.collision_detect(p)
        if result:
            try:
                eggs.remove(p)
            except ValueError:
                pass
        if crash_result:
            try:
                if p.collected is True:
                    p.move_item(screen, birb)
                    p.update_rect()
                else:
                    if birb.slot is False:
                        chirp.play()
                        p.collected = True
                    else:
                        pass
            except ValueError:
                pass
        if shoot_result:
            try:
                crack.play()
                eggs.remove(p)
            except ValueError:
                pass
    if len(eggs) <= 0:
        eggs = [Power() for _ in range(6)]
    birb.move_bullets(screen)
    birb.draw_birb(screen)
    birb.move_birb()
    pygame.display.update()
