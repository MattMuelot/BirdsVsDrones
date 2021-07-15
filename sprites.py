import pygame
import random

from math import cos, pi

def easeInOutSine(n):
	return -0.5 * (cos(pi * n) - 1)

egg_bob_range = 4
egg_bob_speed = 0.2

# ---------------------------------------CLASSES--------------------------------------------------- #

class Bullet(pygame.sprite.Sprite):
	"""Creates bullet object"""

	def __init__(self, x, y, game):
		self.game = game
		self.groups = game.all_sprites, game.bullets
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load('Assets/seed.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vel = 20
		
	def update(self):
		self.rect.x += 20
		if self.rect.x > 890:
			self.kill()
	
	def draw(self, screen):
		screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
	"""Base enemy class. Since most of this class just handles basic movement, I have the
	Egg class inherit from this class"""

	def __init__(self, game):
		self.game = game
		self.groups = game.all_sprites, game.enemies
		pygame.sprite.Sprite.__init__(self, self.groups)
		
		self.image = pygame.image.load('Assets/drone.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(1000, 6000)
		self.rect.y = random.randint(100, 500)
		self.vel = 3

	def update(self):
		self.rect.x -= self.vel
		if self.rect.right < 0:
			self.kill()

	def draw(self, screen):
		screen.blit(self.image, self.rect)
		
class Egg(pygame.sprite.Sprite):

	def __init__(self, game):
		self.game = game
		self.groups = game.all_sprites, game.eggs
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load('Assets/egg.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(1000, 3000)
		self.rect.y = random.randint(0, 400)
		self.vel = -2
		self.collected = False
		self.dropped = False
		self.step = 0
		self.dir = 1

	def update(self):
		"""This method is a work in progress, do not change anything without approval"""
		if not self.dropped:
			if not self.collected:  # If egg has not been collected by player yet
				offset = egg_bob_range * (easeInOutSine(self.step / egg_bob_range) - 0.5)
				self.rect.centery = self.rect.centery + offset * self.dir
				self.step += egg_bob_speed
				
				if self.step > egg_bob_range:
					self.step = 0
					self.dir *= -1

				self.rect.x -= 2

				if self.rect.right < 0:
					self.kill()
					
			if self.collected:  # If the egg is collected by player, it binds x and y to directly under birb
				self.rect.midtop = self.game.birb.rect.midbottom

		if self.dropped:  # If the player hits "m" key, and egg has been dropped, it "falls" down by y += 10
			self.rect.y += 10
			if self.rect.y > 800:
				self.kill()
						
	def draw(self, screen):
		screen.blit(self.image, self.rect)

class Nest:
	"""Nest object. This object is what the egg needs to collide with to score points"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x + 20, self.y + 30, 100, 5)

	def move(self):
		"""Moves nest x -2 to keep pace with background, giving illusion of staying still"""
		self.rect.x -= 2

class Birb(pygame.sprite.Sprite):
	"""Our main player (birb) class"""

	def __init__(self, game):
		self.game = game
		self.groups = game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load('Assets/birb.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = 50
		self.rect.y = 300
		self.vel = 10
		self.carrying_egg = False
		self.egg = None
		self.score = 0
		self.lives = 5
		self.friendly = True
		self.reloading = 0
		
		self.BLACK = (0,0,0)
		self.font = pygame.font.SysFont("Mono", 40)
		self.UP_KEYS = [pygame.K_w, pygame.K_UP]
		self.DOWN_KEYS = [pygame.K_s, pygame.K_DOWN]
		self.LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
		self.RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]

	def draw(self, screen):
		"""Draws our birb object to screen using img attribute"""
		screen.blit(self.image, self.rect)
		pygame.draw.rect(s, (255, 0, 0), self.rect, 2)  # Uncomment to show hit-box

	def crash_detection(self, item, b):
		"""Checks to see if item is colliding with our birb object, returns True"""
		if self.rect.colliderect(item.rect):
			return True

	def update(self):
		"""Gets keys pressed and moves birb if the corresponding key is pressed. Doesn't move if collision with screen
		border

		A/crsr left   is left
		D/crsr right  is right
		W/crsr up     is up
		S/crsr down   is down"""

		pressed = pygame.key.get_pressed()
		for key in self.LEFT_KEYS:
			if pressed[key] and self.rect.x > 0:
				self.rect.x -= self.vel

		for key in self.RIGHT_KEYS:
			if pressed[key] and self.rect.x < 800:
				self.rect.x += self.vel

		for key in self.UP_KEYS:
			if pressed[key] and self.rect.y - self.vel > 0:
				self.rect.y -= self.vel

		for key in self.DOWN_KEYS:
			if pressed[key] and self.rect.y + self.vel < 800 - 100:
				self.rect.y += self.vel

	def print_score_lives(self, screen):
		"""Grabs score and lives adds it to screen"""
		score = str(self.score)
		lives = str(self.lives)
		score_surf = self.font.render(f'Score: {score}', True, self.BLACK)
		lives_surf = self.font.render(f'Lives: {lives}', True, self.BLACK)
		screen.blit(score_surf, (10, 10))
		screen.blit(lives_surf, (700, 10))
