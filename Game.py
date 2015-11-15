import pygame
from Grid import Grid

CELL_HEIGHT = 25
CELL_WIDTH = 25

pygame.init()
pygame.display.set_caption('My game!')
clock = pygame.time.Clock()

done = False

game_grid = Grid().grid

screen = pygame.display.set_mode((len(game_grid)*CELL_HEIGHT, len(game_grid[0])*CELL_WIDTH))

while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    screen.fill((240, 240, 240))
    for rows in range(len(game_grid)):
        for columns in range(len(game_grid[rows])):
            pygame.draw.rect(screen, game_grid[rows][columns].get_colour(),
                             (rows*CELL_HEIGHT, columns*CELL_WIDTH, CELL_HEIGHT, CELL_WIDTH))

    pygame.display.flip()

    clock.tick(10)

pygame.quit()
