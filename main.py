import pygame
import sys
from enum import Enum
import random

class Type(Enum):
	Empty = 0
	Planet = 1
	Sun = 2
	Nebula = 3

size = 4
board = [[]]
play_board = [[]]

W = 640
H = 640

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()

screen = pygame.display.set_mode((W, H))
# surface = pygame.Surface((W, H), pygame.SRCALPHA)
pygame.display.set_caption('Planets')

planet_imgs = [pygame.image.load('planet-' + str(i + 1) + '.png') for i in range(5)]
sun_img = pygame.image.load('sun.png')
nebula_img = pygame.image.load('black-hole2.png')

done = False
clock = pygame.time.Clock()

def get_random_lists():
	sun_spots = [i for i in range(size)]
	neb_spots = [i for i in range(size)]

	random.shuffle(sun_spots)
	random.shuffle(neb_spots)
	overlaps = [i for i in range(size) if sun_spots[i] == neb_spots[i]]
	if len(overlaps) == 0:
		return (sun_spots, neb_spots)
	elif len(overlaps) == 1:
		ind = random.randint(0, size - 1)
		while ind == overlaps[0]:
			ind = random.randint(0, size - 1)
		temp = neb_spots[ind]
		neb_spots[ind] = neb_spots[overlaps[0]]
		neb_spots[overlaps[0]] = temp
		return (sun_spots, neb_spots)
	else:
		temp = neb_spots[overlaps[0]]
		for i in range(len(overlaps) - 1):
			neb_spots[overlaps[i]] = neb_spots[overlaps[i + 1]]
		neb_spots[overlaps[-1]] = temp
		return (sun_spots, neb_spots)


def generate_board(planets=size):
	board = [[Type.Empty for col in range(size)] for row in range(size)]
	assert planets >= size and planets < size ** 2 - (2 * size), "Invalid number of planets"
	
	sun_cols, neb_cols = get_random_lists()
	for row in range(size):
		board[row][sun_cols[row]] = Type.Sun
		board[row][neb_cols[row]] = Type.Nebula

	free_spots = [i for i in range(size ** 2) if board[int(i / size)][i % size] == Type.Empty]
	for _ in range(planets):
		i = random.choice(free_spots)
		board[int(i / size)][i % size] = Type.Planet
		free_spots.remove(i)
	return board

def generate_play_board():
	play_board = [[Type.Empty for col in range(size)] for row in range(size)]
	for row in range(len(board)):
		for col in range(len(board[row])):
			if board[row][col] == Type.Planet:
				play_board[row][col] = Type.Planet
			else:
				play_board[row][col] = Type.Empty
	return play_board

def get_planet_mask_img(board, img, row, col):
	val = 120
	shadow = (val, val, val, 0)

	left = False
	right = False
	top = False
	bottom = False

	x = col - 1
	while x >= 0:
		if board[row][x] == Type.Sun:
			 left = True
			 break
		elif board[row][x] == Type.Planet or board[row][x] == Type.Nebula:
			break
		x -= 1
	if not left:
		x = col + 1
		while x < len(board[row]):
			if board[row][x] == Type.Sun:
				right = True
				break
			elif board[row][x] == Type.Planet or board[row][x] == Type.Nebula:
				break
			x += 1
	
	y = row - 1
	while y >= 0:
		if board[y][col] == Type.Sun:
			 top = True
			 break
		elif board[y][col] == Type.Planet or board[y][col] == Type.Nebula:
			break
		y -= 1
	if not top:
		y = row + 1
		while y < len(board):
			if board[y][col] == Type.Sun:
				bottom = True
				break
			elif board[y][col] == Type.Planet or board[y][col] == Type.Nebula:
				break
			y += 1
	
	w = img.get_width()
	h = img.get_height()
	if left:
		if top:
			# Suns above and to the left
			# Shadow on the bottom-right corner
			rect = img.get_rect().move(w / 2, h / 2)
			img.fill(shadow, rect=rect, special_flags=pygame.BLEND_RGBA_SUB)
		elif bottom:
			# Suns below and to the left
			# Shadow on the top-right corner
			rect = img.get_rect().inflate(-w / 2, -h / 2).move(w / 4, -h / 4)
			img.fill(shadow, rect=rect, special_flags=pygame.BLEND_RGBA_SUB)
		else:
			# Suns to the left
			# Shadow on the right half
			rect = img.get_rect().move(w / 2, 0)
			img.fill(shadow, rect=rect, special_flags=pygame.BLEND_RGBA_SUB)
	elif right:
		if top:
			# Suns above and to the right
			# Shadow on the bottom-left corner
			rect = img.get_rect().inflate(-w / 2, -h / 2).move(-w / 4, h / 4)
			img.fill(shadow, rect=rect, special_flags=pygame.BLEND_RGBA_SUB)
		elif bottom:
			# Suns below and to the right
			# Shadow on the top-left corner
			rect = img.get_rect().inflate(-w / 2, -h / 2).move(-w / 4, -h / 4)
			img.fill(shadow, rect=rect, special_flags=pygame.BLEND_RGBA_SUB)
		else:
			# Suns to the right
			# Shadow on the left half
			rect = img.get_rect().inflate(-w / 2, 0).move(-w / 4, 0)
			img.fill(shadow, rect=rect, special_flags=pygame.BLEND_RGBA_SUB)
	else:
		if top:
			# Suns above
			# Shadow on the bottom half
			rect = img.get_rect().move(0, h / 2)
			img.fill(shadow, rect=rect, special_flags=pygame.BLEND_RGBA_SUB)
		elif bottom:
			# Suns below
			# Shadow on the top half
			rect = img.get_rect().inflate(0, -h / 2).move(0, -h / 4)
			img.fill(shadow, rect=rect, special_flags=pygame.BLEND_RGB_SUB)
		else:
			# No suns
			# Everything in shadow
			img.fill(shadow, special_flags=pygame.BLEND_RGBA_SUB)
	
	return img



def update():
	pass

def draw(s):
	surface = pygame.Surface((W, H), pygame.SRCALPHA)

	# Draw board
	for row in range(size - 1):
		point1 = (W * (row + 1) / size, 0)
		point2 = (W * (row + 1) / size, H)
		pygame.draw.line(surface, GREY, point1, point2, 2)
	for col in range(size - 1):
		point1 = (0, H * (col + 1) / size)
		point2 = (W, H * (col + 1) / size)
		pygame.draw.line(surface, GREY, point1, point2, 2)
	
	img_ind = 0
	for i in range(size ** 2):
			row = int(i / size)
			col = i % size
			rect = pygame.Rect(W * (col) / size, H * row / size, W / size, H / size)
			if play_board[row][col] == Type.Planet:
				# pygame.draw.circle(surface, BLUE, rect.center, int(rect.width / 3))
				img = planet_imgs[img_ind]
				img_ind = (img_ind + 1) % len(planet_imgs)
				img = pygame.transform.scale(img, rect.size)
				img = get_planet_mask_img(board, img, row, col)
				surface.blit(img, rect.topleft)
			elif board[row][col] == Type.Sun:
				# pygame.draw.circle(surface, YELLOW, rect.center, int(rect.width / 3))
				img = pygame.transform.scale(sun_img, rect.size)
				# img.fill((100, 100, 100, 0), rect=img.get_rect().move(img.get_width()/2,0), special_flags=pygame.BLEND_RGBA_SUB)
				surface.blit(img, rect.topleft)
				# pygame.draw.rect(surface, (255, 255, 255, 128), rect)
			elif board[row][col] == Type.Nebula:
				# pygame.draw.rect(surface, RED, rect)
				img = pygame.transform.scale(nebula_img, rect.size)
				surface.blit(img, rect.topleft)
	s.blit(surface, (0, 0))

# size = 2
# board = [[Type.Sun, Type.Sun], [Type.Planet, Type.Sun]]
board = generate_board(random.randint(size, int(2.5 * size) - 5))
print(board)
play_board = generate_play_board()

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (
			event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			done = True
		elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
			size += 1
			board = generate_board(random.randint(size, int(2.5 * size) - 5))
			play_board = generate_play_board()
		elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
			if size <= 4: continue
			size -= 1
			board = generate_board(random.randint(size, int(2.5 * size) - 5))
			play_board = generate_play_board()
		elif event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
			board = generate_board(random.randint(size, int(2.5 * size) - 5))
			play_board = generate_play_board()

	# Game Logic
	update()

	# Screen Clearing
	screen.fill(BLACK)
	# surface.fill((0, 0, 0, 0))

	# Drawing Code
	draw(screen)

	# screen.blit(surface, (0, 0))

	pygame.display.flip()

	clock.tick(60)

pygame.display.quit()
pygame.quit()