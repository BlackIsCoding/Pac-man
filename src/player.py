import random
import sys

import pygame

from maze import (
    BACKGROUND_COLOR,
    MAZE_GRID,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    Maze,
)
from general import General
from charachter import Pacman
from state import System


# ---------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------

pygame.init()
maze = Maze(MAZE_GRID)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man - Development")
font = pygame.font.Font(None, 30)
game = System()
general = General(maze, game)
pacman = Pacman(maze)
ghosts_chars = general.initialize_ghosts()
general.initialize_ghosts_targets(ghosts_chars)

collision = False
running = True

while running:
    # Check whether Pac-Man has collided with a ghost.
    if collision:
        game.lose_life()
        pacman.respawn()

    if game.is_game_over():
        print(game.lives)
        print("you lost")
        exit(1)

    # Handle player input.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(1)
        pacman.handle_event(event)

    pacman.move()

    # Collect normal gums and super gums.
    normal = general.gums_collision((pacman.row, pacman.col), "normal")
    super = general.gums_collision((pacman.row, pacman.col), "super")

    # Check whether all gums have been collected.
    if not normal and not super:
        print("congrats, you finished the game !")
        sys.exit(1)

    # Check collisions with ghosts.
    collision = general.ghost_collision((pacman.row, pacman.col), ghosts_chars, game)

    # Draw the background, title, and maze.
    screen.fill(BACKGROUND_COLOR)
    title = font.render("PAC-MAN", True, (255, 220, 0))
    screen.blit(title, (15, 12))

    maze.draw(screen)

    # Update ghost targets.
    current_time = pygame.time.get_ticks()
    if current_time - ghosts_chars['red'].ghost_last_intelligence >= ghosts_chars['red'].ghost_intelligence_delay:
        general.update_ghosts_targets(
            ghosts_chars, (pacman.row, pacman.col), pacman.direction)
        ghosts_chars['red'].ghost_last_intelligence = current_time

    # Move ghosts at their movement interval.
    current_time = pygame.time.get_ticks()
    if current_time - ghosts_chars['red'].ghost_last_move >= ghosts_chars['red'].ghost_move_delay:
        general.move_ghosts(ghosts_chars)
        ghosts_chars['red'].ghost_last_move = current_time

    # Draw ghosts.
    general.display_ghosts(ghosts_chars, screen)


    pacman.draw(screen)
    pygame.display.flip()


pygame.quit()
sys.exit()
