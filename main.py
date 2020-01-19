import pygame
import sys
from enum import Enum

class Type(Enum):
	Empty = 0
	Planet = 1
	Sun = 2
	Nebula = 3

size = 4
board = [[(row + col) % 4  for col in range(size)] for row in range(size)]

W = 640
H = 640

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Planets')

done = False
clock = pygame.time.Clock()


def update():
	pass

def draw(surface):
	# Draw board
	for row in range(size - 1):
		point1 = (W * (row + 1) / size, 0)
		point2 = (W * (row + 1) / size, H)
		pygame.draw.line(surface, WHITE, point1, point2, 2)
	for col in range(size - 1):
		point1 = (0, H * (col + 1) / size)
		point2 = (W, H * (col + 1) / size)
		pygame.draw.line(surface, WHITE, point1, point2, 2)
	
	for i in range(size ** 2):
			row = int(i / size)
			col = i % size
			rect = pygame.Rect(W * (col) / size, H * row / size, W / size, H / size)
			if Type(board[row][col]) == Type.Planet:
				pygame.draw.circle(surface, BLUE, rect.center, int(rect.width / 3))
			elif Type(board[row][col]) == Type.Sun:
				pygame.draw.circle(surface, YELLOW, rect.center, int(rect.width / 3))
			elif Type(board[row][col]) == Type.Nebula:
				pygame.draw.rect(surface, RED, rect)


while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (
			event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			done = True
		elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
			size += 1
		elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
			size -= 1
	
	# Game Logic
	update()

	# Screen Clearing
	screen.fill(BLACK)

	# Drawing Code
	draw(screen)

	pygame.display.flip()

	clock.tick(60)

pygame.display.quit()
pygame.quit()