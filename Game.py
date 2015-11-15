import pygame
from Grid import Grid

pygame.init()
pygame.display.set_caption('My game!')
clock = pygame.time.Clock()
pygame.display.set_mode((200, 200))
done = False

while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    clock.tick(1)

pygame.quit()