import pygame
import sys

def main():
	pygame.init()

	W = 640
	H = 480

	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)

	screen = pygame.display.set_mode((W, H))
	pygame.display.set_caption('Planets')

	done = False
	clock = pygame.time.Clock()


	size = 4
	board = [[0 for col in range(size)] for row in range(size)]

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (
				event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				done = True
		
		# Game Logic
		update()

		# Screen Clearing
		screen.fill(BLACK)

		# Drawing Code
		draw()

		pygame.display.flip()

		clock.tick(60)

	pygame.display.quit()
	pygame.quit()

def update():
	pass

def draw():
	

if __name__ == "__main__":
	main()