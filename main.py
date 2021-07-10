import pygame
import os
import random

# ------------------------Initialize pygame base----------------------------------- #

pygame.init()
screen = pygame.display.set_mode((900, 800))

# ----------------------Load in non class specific images-------------------------- #

bg = pygame.image.load('Assets/hillbg.png').convert_alpha()
seed = pygame.image.load('Assets/seed.png').convert_alpha()

# ----------------Initialize sound mixer and load in audio------------------------- #

pygame.mixer.init()
pygame.mixer.set_num_channels(16)
pygame.mixer.music.load('Assets/gametheme.mp3')
pygame.mixer.music.play(-1)
plink = pygame.mixer.Sound('Assets/plink.ogg')
squawk = pygame.mixer.Sound('Assets/squawk.ogg')
crack = pygame.mixer.Sound('Assets/crack.ogg')
chirp = pygame.mixer.Sound('Assets/chirp.ogg')


# ---------------------------------------CLASSES--------------------------------------------------- #
"""PLEASE NOTE: Egg class inherits from Enemy class, mostly for item movement"""


class Bullet:
    """Creates bullet object"""
    def __init__(self, x, y):
        self.img = pygame.image.load('Assets/seed.png').convert_alpha()
        self.x = x
        self.y = y
        self.vel = 20
        self.bullet_rect = pygame.Rect(self.x, self.y, 10, 10)

    def off_screen(self):
        """Check if bullet is off-screen, returns true if it is"""
        if self.x > 880:
            return True


class Enemy:
    """Base enemy class. Since most of this class just handles basic movement, I have the
    Egg class inherit from this class"""
    def __init__(self):
        self.img = pygame.image.load('Assets/drone.png').convert_alpha()
        self.x = random.randint(1000, 6000)
        self.y = random.randint(100, 500)
        self.vel = 3
        self.rect = pygame.Rect(self.x, self.y + 20, 100, 60)
        self.friendly = False

    def move_item(self, s, b):
        """When this method is called, we pass in the display(s) and our bird(b) object. The bird(b) object
        has no actual use in the Enemy class, but is used in the Egg class, so its here for inheritance"""
        self.x -= self.vel
        self.update_rect()
        # pygame.draw.rect(s, (255, 0, 0), self.rect, 2) # Un-comment for hit-box viewing
        s.blit(self.img, (self.x, self.y))
        if self.x < -50:
            return True

    def update_rect(self):
        """Updates our rect attribute to match co-ordinates of our Enemy object x and y"""
        self.rect = pygame.Rect(self.x, self.y + 20, 100, 60)


class Egg(Enemy):
    """Our Egg class, inherits from enemy (even though as you can see below we've changed a lot lol) so
    please note this is a work in progress as Im overhauling the movement"""
    def __init__(self):
        super().__init__()
        self.x = random.randint(1000, 3000)
        self.y = random.randint(0, 400)
        self.vel = -2
        self.collected = False  # If our Bird object comes into contact with egg, its collected status becomes True
        self.dropped = False  # If our Bird object drops the egg, this becomes True
        self.rect = pygame.Rect(self.x + 15, self.y + 7, 70, 87)  # Manually edited hit-box to be as perfect as possible
        self.img = pygame.image.load('Assets/egg.png').convert_alpha()

    def update_rect(self):
        """Updates our rect attribute to match co-ordinates of our Egg object x and y"""
        self.rect = pygame.Rect(self.x + 15, self.y + 7, 70, 87)

    def move_item(self, s, b):
        """This method is a work in progress, do not change anything without approval"""
        if self.collected is False:
            self.x -= 2
            self.update_rect()
            # pygame.draw.rect(s, (255, 0, 0), self.rect, 2)  # Uncomment to view hit-box
            s.blit(self.img, (self.x, self.y))
            if self.x < 50:
                return True
        if self.collected:
            if self.dropped is False:
                self.x, self.y = b.x, b.y + 60
                self.update_rect()
                s.blit(self.img, (self.x, self.y))
            else:
                # b.slot = False
                self.y += 10
                self.update_rect()
                s.blit(self.img, (self.x, self.y))


class Birb:
    """Our main player (birb) class"""
    def __init__(self):
        self.img = pygame.image.load('Assets/birb.png').convert_alpha()
        self.x = 50
        self.y = 300
        self.vel = 10
        self.slot = False  # Our birb can only hold one egg at a time, if it is currently holding an egg, slot is True
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.bullets = []
        self.score = 0
        self.lives = 5
        self.friendly = True

    def draw_birb(self, s):
        """Draws our birb object to screen using img attribute"""
        s.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(s, (255, 0, 0), self.rect, 2)  # Uncomment to show hit-box

    def shoot_bullets(self):
        """Creates a bullet object and appends that object to our bullets list"""
        bullet = pygame.Rect(self.x + 75, self.y + 35, 10, 10)
        self.bullets.append(bullet)

    def move_bullets(self, s):
        """Iterates through list of bullets and moves them, draws them to the screen, then removes them if
        they go off-screen"""
        for b in self.bullets:
            b.x += 20
            s.blit(seed, (b.x, b.y))
            if b.x > 890:
                self.bullets.remove(b)

    def bullet_detect(self, item):
        """Iterates through list of bullets and checks to see if is colliding with the item we pass in to this
        method, if it does, it removes the bullet from our list of bullets and returns True"""
        for b in self.bullets:
            if b.colliderect(item.rect):
                self.bullets.remove(b)
                return True

    def crash_detection(self, item, b):
        """Checks to see if item is colliding with our birb object, returns True"""
        if self.rect.colliderect(item.rect):
            return True

    def update_rect(self):
        """Updates our rect attribute to match co-ordinates of our Birb object x and y"""
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def move_birb(self):
        """Gets keys pressed and moves birb if the corresponding key is pressed. Doesn't move if collision with screen
        border

        A is left
        D is right
        W is up
        S is down"""

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


# --------------------------------- MAIN GAME LOOP and OBJECT INSTANCE CREATION ------------------------ #

birb = Birb()  # Create our birb object

i = 0  # This variable is used to move the screen and get that "scrolling" effect

running = True
test_rect = pygame.Rect(675, 475, 140, 50)  # This is a test rect that will eventually be used for egg baskets
enemies = [Enemy() for _ in range(30)]  # Create a list of enemies
eggs = [Egg() for _ in range(6)]  # Create a list of eggs

while running:
    clock = pygame.time.Clock()
    clock.tick(120)  # FPS Set to 120
    screen.fill((0, 0, 222))
    screen.blit(bg, (i, 0))
    screen.blit(bg, (900 + i, 0))
    i -= 2  # For every time loop is run, our background image x co-ordinate moves -2
    test_rect.x -= 2  # Our test rect also moves x -2 to keep pace with background, for illusion of staying still
    if i == -900:  # If the i value goes less than -900 (which is the width of the screen) it draws a new background
        screen.blit(bg, (900 + i, 0))
        i = 0
        test_rect.x = 675
        test_rect.y = 475
    pygame.draw.rect(screen, (255, 0, 0), test_rect, 2)  # This just draws our test rect to the screen
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
    """Goes through each egg object and runs specific checks, I know this looks confusing but hopefully when im
    done it will be a lot less confusing"""
    for p in eggs[:]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            if birb.slot is False:
                pass
            else:
                p.dropped = True
                birb.slot = False
        crash_result = birb.crash_detection(p, birb)  # Checks to see if our birb is colliding with the egg
        if crash_result:
            if birb.slot is False:  # Checks to see if slot is not filled
                p.collected = True  # Sets egg object collected to True
                birb.slot = True  # Sets our slot to True (meaning the slot is filled and we cant collect any more eggs)
        p.move_item(screen, birb)
    if len(eggs) <= 0:  # If all eggs are either destroyed, or off-screen, regenerate list of eggs
        eggs = [Egg() for _ in range(6)]
    birb.move_bullets(screen)
    birb.draw_birb(screen)
    birb.move_birb()
    pygame.display.update()
