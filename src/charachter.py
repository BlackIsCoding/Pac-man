import pygame
from maze import WEST, NORTH, EAST, SOUTH, TILE_SIZE, HUD_HEIGHT

class Pacman():
    def __init__(self, maze):
        self.maze = maze
        self.row, self.col = maze.get_center()
        self.direction = None
        self.move_delay = 200
        self.last_move_time = 0
        self.load_images()
        self.update_position()

    def load_images(self):
        self.assets = {
            "closed": pygame.image.load("../assets/pac_man_close.png"),
            "right": pygame.image.load("../assets/pac_man_open_right.png"),
            "left": pygame.image.load("../assets/pac_man_open_left.png"),
            "up": pygame.image.load("../assets/pac_man_open_up.png"),
            "down": pygame.image.load("../assets/pac_man_open_down.png"),
        }

        for direction in self.assets:
            self.assets[direction] = pygame.transform.smoothscale(
                self.assets[direction],
                (24, 24)
            )
        self.image = self.assets['closed']

    def update_position(self):
        self.x = (self.col * TILE_SIZE + TILE_SIZE // 2 - self.image.get_width() // 2)
        self.y = (self.row * TILE_SIZE + TILE_SIZE // 2 + HUD_HEIGHT - self.image.get_height() // 2)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        current_time = pygame.time.get_ticks()
        if self.direction is None:
            return

        if current_time - self.last_move_time < self.move_delay:
            return

        if self.maze.can_move(self.row, self.col, self.direction):
            if self.direction == EAST:
                self.col += 1
            elif self.direction == WEST:
                self.col -= 1
            elif self.direction == NORTH:
                self.row -= 1
            elif self.direction == SOUTH:
                self.row += 1
        self.last_move_time = current_time
        self.update_position()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.direction = EAST
                self.image = self.assets["right"]

            elif event.key == pygame.K_LEFT:
                self.direction = WEST
                self.image = self.assets["left"]

            elif event.key == pygame.K_UP:
                self.direction = NORTH
                self.image = self.assets["up"]

            elif event.key == pygame.K_DOWN:
                self.direction = SOUTH
                self.image = self.assets["down"]

    def respawn(self):
        self.row, self.col = self.maze.get_center()