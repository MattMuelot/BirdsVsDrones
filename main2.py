"""SPECIAL NOTE: Im aware to more experienced programmers that there are probably much better ways to handle a
lot of the things I'm working on here, but its a learning experience. Any advice is welcome, please fork and
create a pull request if you see anything that can be changed that you think would be beneficial"""

import pygame
from pygame.locals import *
from sprites import *
import random, sys

from os import path

pygame.init()

width = 900
height = 800
FPS = 60

class Game(object):

	def __init__(self):
		
# ----------------Initialize sound mixer and load in audio------------------------- #

		pygame.mixer.init()
		pygame.mixer.set_num_channels(16)
		pygame.mixer.music.load('Assets/gametheme.ogg')
		

		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()
		self.running = True
		#self.font_name = pygame.font.match_font(font_name)
		self.load_data()

# ----------------------Load in non class specific images-------------------------- #

	def load_data(self):

		self.bg = pygame.image.load('Assets/hillbg.png').convert_alpha()

		self.plink = pygame.mixer.Sound('Assets/plink.ogg')
		self.squawk = pygame.mixer.Sound('Assets/squawk.ogg')
		self.crack = pygame.mixer.Sound('Assets/crack.ogg')
		self.chirp = pygame.mixer.Sound('Assets/chirp.ogg')


	def new(self):
		self.all_sprites = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.eggs = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		
		for _ in range(30):
			Enemy(self)
		
		for _ in range(6):
			Egg(self)
	
		self.birb = Birb(self)
		self.nest = Nest()  # Create nest object

		self.screen_offset = 0
		#pygame.mixer.music.play(-1)
		self.run()
		
	def run(self):
		self.running = True
		while self.running:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
					
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.shoot_bullets()
		
				if event.key == pygame.K_m:
					if self.birb.carrying_egg:
						self.birb.carrying_egg = False
					
						for e in self.eggs:
							if e.collected:
								e.dropped = True
								e.collected = False
								break

	def update(self):
		self.all_sprites.update()	
		
		for bullet_hit in pygame.sprite.groupcollide(self.bullets, self.enemies, True, True):
			self.plink.play()
			self.birb.score += 2
			
		enemy_hits = pygame.sprite.spritecollide(self.birb, self.enemies, True, pygame.sprite.collide_mask)
		if enemy_hits:
			self.squawk.play()
			self.birb.lives -= 1
			if self.birb.lives <= 0:
				self.running = False
		
			Enemy(self)
		
		egg_hit = pygame.sprite.spritecollide(self.birb, self.eggs, False, pygame.sprite.collide_mask)
		if egg_hit:
			if not self.birb.carrying_egg:
				egg_hit[0].collected = True
				self.birb.carrying_egg = True
				self.birb.egg = egg_hit[0]
				
		for egg_hit2 in pygame.sprite.groupcollide(self.bullets, self.eggs, True, True, pygame.sprite.collide_mask):
			self.crack.play()
			self.birb.score -= 5
			
		if self.birb.egg is not None:
			if self.birb.egg.dropped:		  
				if self.birb.egg.rect.colliderect(self.nest.rect):
					print('basket collision')
					self.birb.egg.kill()
					self.birb.score += 5
					self.chirp.play()
	
		if len(self.eggs) <= 0:
			for _ in range(6):
				Egg(self)
			
	def shoot_bullets(self):
		"""Creates a bullet object and appends that object to our bullets list"""
		bullet = Bullet(self.birb.rect.x + 75, self.birb.rect.y + 35, self)

	def draw(self):
		self.screen.fill((0, 0, 222))
		self.screen.blit(self.bg, (self.screen_offset, 0))
		self.screen.blit(self.bg, (900 + self.screen_offset, 0))
		self.screen_offset -= 2  # For every time loop is run, our background image x co-ordinate moves -2
		
		if self.screen_offset == -900:  # If the i value goes less than -900 (which is the width of the screen) it draws a new background
			self.screen.blit(self.bg, (900 + self.screen_offset, 0))
			self.screen_offset = 0
			self.nest.x = 675
			self.nest.y = 475

		
		self.all_sprites.draw(self.screen)	
		self.birb.print_score_lives(self.screen)
		pygame.display.update()

	def show_start_screen(self):
		pass
		
	def show_game_over_screen(self):
		pass
		
if __name__=="__main__":
	g = Game()
	g.show_start_screen()
	while g.running:
		g.new()
		g.show_game_over_screen()
		
pygame.quit()
sys.exit()

