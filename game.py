# import pygame
# import config
#
#
# class Game:
#
#     def __init__(self):
#         self.clock = 0
#         self.done = False
#         self.screen = None
#         self.width = config.grid_width()
#         self.height = config.grid_height()
#
# # -- Init Grid
#
#     def init_grid(self):
#         pygame.init()
#         pygame.display.set_caption('Generation 1!')
#         self.clock = pygame.time.Clock()
#         self.screen = pygame.display.set_mode((self.width*config.cell_pixel_width(), self.height*config.cell_pixel_height()))
#
#
# # -- Display Grid
#
#     def display(self , markposition):
#             for event in pygame.event.get(): # User did something
#                 if event.type == pygame.QUIT: # If user clicked close
#                     done = True  # Flag that we are done so we exit this loop
#                     continue
#
#             # Move animats
#             # Process positions
#             self.screen.fill((240, 240, 240))
#             for rows in range(self.height):
#                 for columns in range(self.width):
#                     pygame.draw.rect(self.screen, self.getcolor(markposition[rows][columns]) ,
#                              (rows*config.cell_pixel_height(), columns*config.cell_pixel_width(),
#                               config.cell_pixel_height(), config.cell_pixel_width()))
#
#             pygame.display.flip()
#
# # -- Get color (Haven't integrated grid.py yet) so manually choosing colors for now
#
#     def getcolor(self, x):
#         if x == 0.0:
#             return (0,0,0)
#         elif x == 1.0:
#             return (10,10,10)
#         elif x == 2.0:
#             return (255,0,0)
#         elif x == 3.0:
#             return (0,127,0)
#         elif x == 4.0:
#             return (0,255,0)
import pygame
import grid
import config

pygame.init()
pygame.display.set_caption('Predators attack!')
clock = pygame.time.Clock()

done = False

game_grid = grid.singleton_grid.grid

screen = pygame.display.set_mode(
    (len(game_grid)*config.cell_pixel_height(), len(game_grid[0])*config.cell_pixel_width()))

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
pygame.quit()
