import pygame
import random

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
        if self.x < -100:
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
        self.collected = False
        self.dropped = False
        self.rect = pygame.Rect(self.x + 15, self.y + 7, 70, 87)  # Manually edited hit-box to be as perfect as possible
        self.img = pygame.image.load('Assets/egg.png').convert_alpha()

    def update_rect(self):
        """Updates our rect attribute to match co-ordinates of our Egg object x and y"""
        self.rect = pygame.Rect(self.x + 15, self.y + 7, 70, 87)

    def move_item(self, s, b):
        """This method is a work in progress, do not change anything without approval"""
        if not self.dropped:
            if not self.collected:  # If egg has not been collected by player yet
                self.x -= 2
                self.update_rect()
                # pygame.draw.rect(s, (255, 0, 0), self.rect, 2)  # Uncomment to view hit-box
                s.blit(self.img, (self.x, self.y))
                if self.x < -100:
                    return True  # Returns true if x of egg is off screen
            if self.collected:  # If the egg is collected by player, it binds x and y to directly under birb
                self.x = b.x
                self.y = b.y + 65
                self.update_rect()
                s.blit(self.img, (self.x, self.y))
        if self.dropped:  # If the player hits "m" key, and egg has been dropped, it "falls" down by y += 10
            self.y += 10
            self.update_rect()
            s.blit(self.img, (self.x, self.y))
            if self.y > 800:
                return True  # Returns true if off screen on the y axis


class Nest:
    """Nest object. This object is what the egg needs to collide with to score points"""

    def __init__(self):
        self.x = 675
        self.y = 475
        self.rect = pygame.Rect(self.x + 20, self.y + 30, 100, 5)

    def move(self, s):
        """Moves nest x -2 to keep pace with background, giving illusion of staying still"""
        self.x -= 2
        self.rect = pygame.Rect(self.x + 20, self.y + 30, 100, 5)


class Birb:
    """Our main player (birb) class"""

    def __init__(self):
        self.img = pygame.image.load('Assets/birb.png').convert_alpha()
        self.seed = pygame.image.load('Assets/seed.png').convert_alpha()
        self.x = 50
        self.y = 300
        self.vel = 10
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.bullets = []
        self.carrying_egg = False
        self.score = 0
        self.lives = 5
        self.friendly = True
        self.BLACK = (0, 0, 0)
        self.font = pygame.font.SysFont("Mono", 40)
        self.UP_KEYS = [pygame.K_w, pygame.K_UP]
        self.DOWN_KEYS = [pygame.K_s, pygame.K_DOWN]
        self.LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
        self.RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]

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
            s.blit(self.seed, (b.x, b.y))
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

        pressed = pygame.key.get_pressed()
        for key in self.LEFT_KEYS:
            if pressed[key] and self.x > 0:
                self.x -= self.vel
                self.update_rect()

        for key in self.RIGHT_KEYS:
            if pressed[key] and self.x < 800:
                self.x += self.vel
                self.update_rect()

        for key in self.UP_KEYS:
            if pressed[key] and self.y - self.vel > 0:
                self.y -= self.vel
                self.update_rect()

        for key in self.DOWN_KEYS:
            if pressed[key] and self.y + self.vel < 800 - 100:
                self.y += self.vel
                self.update_rect()

    def print_score_lives(self, screen):
        """Grabs score and lives adds it to screen"""
        score = str(self.score)
        lives = str(self.lives)
        score_surf = self.font.render(f'Score: {score}', True, self.BLACK)
        lives_surf = self.font.render(f'Lives: {lives}', True, self.BLACK)
        screen.blit(score_surf, (10, 10))
        screen.blit(lives_surf, (700, 10))
