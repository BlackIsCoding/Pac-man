from ghost import Ghost
import pygame
import random
from maze import NORTH, WEST, EAST, SOUTH

class General():
    def __init__(self, maze, state):
        self.maze = maze
        self.state = state


    def initialize_ghosts(self):
        maze = self.maze
        colors = ["pink", "red", "yellow", "blue"]
        ghosts = {}

        for color in colors:
            string = f"../assets/ghost_{color}.png"
            ghosts[color] = pygame.image.load(string)
            ghosts[color] = pygame.transform.smoothscale(ghosts[color], (24, 24))

        red_ghost = Ghost(
            self.get_maze_corners((maze.rows, maze.cols))[0],
            ghosts["red"],
            200,
            "red",
            maze
        )
        blue_ghost = Ghost(
            self.get_maze_corners((maze.rows, maze.cols))[1],
            ghosts["blue"],
            200,
            "blue",
            maze
        )
        yellow_ghost = Ghost(
            self.get_maze_corners((maze.rows, maze.cols))[2],
            ghosts["yellow"],
            200,
            "yellow",
            maze
        )
        pink_ghost = Ghost(
            self.get_maze_corners((maze.rows, maze.cols))[3],
            ghosts["pink"],
            200,
            "pink",
            maze
        )
        return {"red": red_ghost,
                "blue": blue_ghost,
                "pink": pink_ghost,
                "yellow": yellow_ghost}

    @staticmethod
    def return_random_tuple():
        grid_index = [i for i in range(15)]
        return(random.choice(grid_index), random.choice(grid_index))

    def initialize_ghosts_targets(self, ghosts):
        maze = self.maze
        center = maze.get_center()
        ghosts['red'].intelligence(center)
        ghosts['pink'].intelligence(center)
        for color in ['yellow', 'blue']:
            ghosts[color].intelligence(self.return_random_tuple())

    def update_ghosts_targets(self, ghosts, pacman_position, last_direction):
        maze = self.maze
        pacman_row, pacman_col = pacman_position
        
        target = pacman_position
        ghosts['red'].intelligence((pacman_row, pacman_col))
        
        if last_direction == NORTH:
            target = (pacman_row - 4, pacman_col)
        elif last_direction == SOUTH:
            target = (pacman_row + 4, pacman_col)
        elif last_direction == EAST:
            target = (pacman_row, pacman_col + 4)
        elif last_direction == WEST:
            target = (pacman_row, pacman_col - 4)
        target_row = min(target[0], maze.rows - 1)
        target_col = min(target[1], maze.cols - 1)
        ghosts['pink'].intelligence((target_row, target_col))

        for color in ['yellow', 'blue']:
            ghosts[color].intelligence(self.return_random_tuple())

    def move_ghosts(self, ghosts):
        for ghost in ghosts:
            ghosts[ghost].move()

    def display_ghosts(self, ghosts, screen):
        for ghost in ghosts:
            ghosts[ghost].display_ghost(screen)

    @staticmethod
    def get_maze_corners(maze_size):
        rows , cols = maze_size
        return ([(0,0), (cols - 1, 0), (0, rows - 1), (cols - 1, rows - 1)])

    @staticmethod
    def ghost_collision(pacman_position, ghosts, game):
        for ghost in ghosts:
            if ghosts[ghost].grid_position == pacman_position:
                return True

    def gums_collision(self, pacman_position, object):

        normal, super = False, False
        if object == "normal":
            gums = self.maze.gums
            normal = True
        elif object == "super":
            gums = self.maze.super_gums
            super = True

        for gum in gums[:]:
            if pacman_position == (gum.row, gum.col):
                gums.remove(gum)
                if super:
                    self.state.update_score("super")
                elif normal:
                    self.state.update_score("normal")
                print(self.state.score)
        
        return gums