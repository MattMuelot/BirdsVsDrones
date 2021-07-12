"""SPECIAL NOTE: Im aware to more experienced programmers that there are probably much better ways to handle a
lot of the things I'm working on here, but its a learning experience. Any advice is welcome, please fork and
create a pull request if you see anything that can be changed that you think would be beneficial"""

import pygame
from pygame.locals import *
from game_classes import *
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
		self.enemies = [Enemy() for _ in range(30)]  # Create a list of enemies
		self.eggs = [Egg() for _ in range(6)]  # Create a list of eggs
		self.birb = Birb()
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
					self.birb.shoot_bullets()
		
				if event.key == pygame.K_m:
					if self.birb.carrying_egg:
						for e in self.eggs:
							if e.collected:
								e.dropped = True
								print('dropper')
								e.collected = False
								self.birb.carrying_egg = False
								break

	def update(self):
		self.nest.move(self.screen)
		self.birb.move_bullets(self.screen)
		self.birb.move_birb()
	
		for e in self.enemies:
			result = e.move_item(self.screen, self.birb)
			shot_result = self.birb.bullet_detect(e)
			crash_result = self.birb.crash_detection(e, self.birb)
		
			if shot_result:
				try:
					self.enemies.remove(e)
					self.plink.play()
				except ValueError:
					pass
			if result:
				self.enemies.remove(e)
		
			if crash_result:
				try:
					self.enemies.remove(e)
					self.squawk.play()
					self.birb.lives -= 1
					if self.birb.lives <= 0:
						self.running = False
				except ValueError:
					pass
		
		if len(self.enemies) <= 0:
			self.enemies = [Enemy() for _ in range(30)]
	
		for e in self.eggs:
			if e.collected:
				pass
			else:
				crash_result = self.birb.crash_detection(e, self.birb)  # Checks to see if our birb is colliding with the egg
				if crash_result:
					if not self.birb.carrying_egg:
						e.collected = True
						self.birb.carrying_egg = True
			
			shot_result = self.birb.bullet_detect(e)
			if shot_result:
				self.eggs.remove(e)
				self.crack.play()
				self.birb.score -= 5
			
			off_screen = e.move_item(self.screen, self.birb)
			if off_screen:
				if e.dropped:
					self.birb.carrying_egg = False
					self.eggs.remove(e)
				else:
					self.eggs.remove(e)
		  
			if e.dropped:
				if e.rect.colliderect(self.nest.rect):
					print('basket collision')
					self.eggs.remove(e)
					self.birb.score += 5
					self.chirp.play()
		
		if len(self.eggs) == 0:  # If all eggs are either destroyed, or off-screen, regenerate list of eggs
			self.eggs = [Egg() for _ in range(6)]

  							
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

		
		self.birb.draw_birb(self.screen)
		
		for e in self.enemies:
			e.draw(self.screen)
		
		for e in self.eggs:
			e.draw(self.screen)
			
		for b in self.birb.bullets:
			b.draw(self.screen)
			
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

