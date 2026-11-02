import pygame
import sys
from maze import Maze, MAZE_GRID

def get_maze_corners(maze_size):
    rows , cols = maze_size
    return ([(0,0), (cols - 1, 0), (0, rows - 1), (cols - 1, rows - 1)])

class Ghost():
    def __init__(self, position, image, speed, color, maze, pacman_lastpos):
        self.png = image
        self.grid_position = position
        self.speed = speed
        self.color = color
        self.maze = maze
        self.pac_last_pos = pacman_lastpos

    def get_pixel_coordinates(self, x, y):
        from player import TILE_SIZE, HUD_HEIGHT
        x = x * TILE_SIZE + TILE_SIZE // 2
        y = y * TILE_SIZE + TILE_SIZE // 2 + HUD_HEIGHT
        return (x, y)

    def display_ghost(self, screen):
        x, y = self.get_pixel_coordinates(self.grid_position[1], self.grid_position[0])
        rect = self.png.get_rect(center=(x, y))
        screen.blit(self.png, rect)

    def intelligence(self, pacman_position):
        start = self.grid_position
        target = pacman_position
        bfs = self.maze.bfs(start, target)
        self.path = bfs

    def move(self):
        if not self.path:
            print("empty")
            sys.exit(1)
        y, x = self.grid_position
        if self.path[0] == "s":
            y += 1
        elif self.path[0] == 'n':
            y -= 1
        elif self.path[0] == 'w':
            x -= 1
        elif self.path[0] == 'e':
            x += 1
        print("Before:", self.grid_position, "Direction:", self.path[0])
        self.path = self.path[1:]
        self.grid_position = (y, x)