#!/usr/bin/env python3
import os
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

T_SIZE = 4
TILES_N = T_SIZE*T_SIZE
PLAYING_POPES = TILES_N // 2
TILE_SIZE = 128
MARGIN = TILE_SIZE // 2
TILE_W_MARGIN = TILE_SIZE + MARGIN
SCREEN_WIDTH = T_SIZE * TILE_W_MARGIN + MARGIN
SCREEN_HEIGHT = SCREEN_WIDTH

class Tile:
	name: ""
	image: pygame.Surface
	uncovered: 0
	
	def __init__(self, name, image):
		self.name = name
		self.image = image
		self.uncovered = 0

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Pope memos")
clock = pygame.time.Clock()
done = False

while not done:
	left_to_uncover = PLAYING_POPES

	popes = []
	folder_path = os.path.join(os.getcwd(), 'img')
	imglist = [x for x in os.listdir(folder_path) if x.endswith(".jpg")]
	selected_popes = random.sample(imglist, k=TILES_N//2)
	selected_popes.extend(selected_popes)

	# print(selected_popes)

	for filename in selected_popes:
		image = pygame.image.load(os.path.join(folder_path, filename))
		scaled_image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
		popes.append(Tile(filename, scaled_image))
		
	random.shuffle(popes)
	

	mode = 0
	found = {}
	first_selected = -1
	second_selected = -1 

	while left_to_uncover > 0 or mode > 0:
	
		selected = -1
		screen.fill(GRAY)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONUP:
				if mode < 2:
					mouse_pos = pygame.mouse.get_pos()
					selected = (mouse_pos[0]-MARGIN//2)//TILE_W_MARGIN + ((mouse_pos[1]-MARGIN//2)//TILE_W_MARGIN)*T_SIZE
					if popes[selected].uncovered < 2:
						if mode == 0: first_selected = selected
						if mode == 1: second_selected = selected
						mode += 1
					print(f"lef: {left_to_uncover}")
					print(f"now: {popes[first_selected].name}")
					print(f"then {popes[second_selected].name}")
					# print(f"mode {mode}")
					print()
					
					if first_selected >=0 and second_selected >= 0 and popes[first_selected].name == popes[second_selected].name:
						popes[first_selected].uncovered = 2
						popes[second_selected].uncovered = 2
						mode = 0
						left_to_uncover -= 1
					if selected >= 0 and popes[selected].uncovered == 0:
						popes[selected].uncovered = 1
				else:
					mode = 0
					first_selected = -1
					second_selected = -1
					for i in popes:
						if i.uncovered < 2: i.uncovered = 0
			
		for i in range(TILES_N):
			x = MARGIN + i%T_SIZE*TILE_W_MARGIN
			y = i//T_SIZE*TILE_W_MARGIN + MARGIN
			if popes[i].uncovered == 0:
				pygame.draw.rect(screen, WHITE, [x, y, TILE_SIZE, TILE_SIZE], 0)
			else: screen.blit(popes[i].image, (x, y))
		pygame.display.update()
		clock.tick(60)
	
	
pygame.quit()
