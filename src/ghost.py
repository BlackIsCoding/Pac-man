import pygame
import sys
from maze import Maze, MAZE_GRID



class Ghost():
    def __init__(self, position, image, speed, color, maze):
        self.png = image
        self.speed = speed
        self.color = color
        
        self.grid_position = position
        self.maze = maze
        self.respawn = position
        
        self.ghost_last_move = 0
        self.ghost_move_delay = 600
        self.ghost_last_intelligence = 0
        self.ghost_intelligence_delay = 500

    

    def get_pixel_coordinates(self, x, y):
        from maze import TILE_SIZE, HUD_HEIGHT
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
            return
        y, x = self.grid_position
        if self.path[0] == "s":
            y += 1
        elif self.path[0] == 'n':
            y -= 1
        elif self.path[0] == 'w':
            x -= 1
        elif self.path[0] == 'e':
            x += 1
        self.path = self.path[1:]
        self.grid_position = (y, x)