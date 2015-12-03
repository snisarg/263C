import pygame
import grid
import config
from grid import *

pygame.init()
pygame.display.set_caption('Predators attack!')
clock = pygame.time.Clock()

done = False

game_grid = grid.singleton_grid.grid

screen = pygame.display.set_mode(
    (len(game_grid)*config.cell_pixel_height(), len(game_grid[0])*config.cell_pixel_width()))
generation_size = config.get_generation_size()
generation_number = 0
print "Generation :", generation_number
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            continue

    # Move animats
    grid.singleton_world.tick()
    # Process positions

    # screen.fill((240, 240, 240))
    for rows in range(len(game_grid)):
        for columns in range(len(game_grid[rows])):
            pygame.draw.rect(screen, game_grid[rows][columns].get_colour(),
                             (rows*config.cell_pixel_height(), columns*config.cell_pixel_width(),
                              config.cell_pixel_height(), config.cell_pixel_width()))

    pygame.display.flip()
    clock.tick(config.render_refresh_clock_ticks())

    generation_size -=1
    if generation_size == 0:
        generation_number += 1
        print "Generation :", generation_number
        grid.singleton_grid = Grid()
        grid.singleton_world.new_generation(grid.singleton_grid)
        game_grid = grid.singleton_grid.grid
        generation_size = config.get_generation_size()
pygame.quit()
