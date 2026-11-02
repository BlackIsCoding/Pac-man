
import pygame
import sys
import math
from collections import deque
# -------------------- Configuration --------------------

TILE_SIZE = 32
HUD_HEIGHT = 50

WALL_COLOR = (25, 45, 160)
BACKGROUND_COLOR = (0, 0, 0)
GUM_COLOR = (255, 210, 170)
SUPER_GUM_COLOR = (255, 255, 255)

# Wall encoding
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

MAZE_GRID = [
    [9, 3, 9, 1, 5, 1, 5, 3, 9, 1, 1, 1, 1, 1, 3],
    [8, 6, 12, 4, 5, 0, 1, 2, 10, 8, 2, 10, 8, 2, 10],
    [8, 3, 9, 5, 3, 8, 2, 8, 4, 6, 10, 12, 4, 4, 2],
    [10, 12, 4, 3, 10, 10, 12, 0, 1, 5, 4, 5, 1, 3, 10],
    [8, 5, 5, 0, 4, 0, 1, 4, 4, 5, 5, 1, 4, 4, 2],
    [10, 9, 5, 6, 15, 8, 4, 3, 15, 15, 15, 8, 1, 3, 10],
    [8, 6, 9, 3, 15, 12, 5, 0, 5, 7, 15, 8, 4, 2, 10],
    [8, 1, 0, 2, 15, 15, 15, 10, 15, 15, 15, 8, 1, 2, 10],
    [10, 8, 0, 2, 9, 3, 15, 10, 15, 13, 5, 4, 6, 12, 6],
    [8, 4, 6, 8, 6, 10, 15, 10, 15, 15, 15, 9, 3, 9, 3],
    [8, 3, 9, 2, 9, 0, 3, 8, 5, 1, 5, 0, 4, 2, 10],
    [10, 8, 6, 12, 2, 10, 10, 8, 3, 12, 5, 4, 5, 2, 10],
    [8, 4, 5, 1, 4, 6, 12, 4, 0, 1, 5, 3, 9, 2, 10],
    [10, 9, 3, 8, 1, 1, 1, 5, 6, 8, 3, 8, 4, 4, 2],
    [12, 4, 6, 12, 6, 12, 4, 5, 5, 6, 12, 4, 5, 5, 6]
]

ROWS = len(MAZE_GRID)
COLS = len(MAZE_GRID[0])

SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE + HUD_HEIGHT

PLAYER_SPAWN = (7, 7)

SUPER_GUM_POSITIONS = [
    (1, 1),
    (1, 13),
    (13, 1),
    (13, 13)
]


# -------------------- Gum Classes --------------------

class Gum:
    """Represent a normal pacgum."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.x = col * TILE_SIZE + TILE_SIZE // 2
        self.y = row * TILE_SIZE + TILE_SIZE // 2 + HUD_HEIGHT

        self.radius = 3
        self.color = GUM_COLOR
        self.eaten = False

    def draw(self, screen):
        """Draw the gum if it hasn't been eaten."""
        if not self.eaten:
            pygame.draw.circle(
                screen,
                self.color,
                (self.x, self.y),
                self.radius
            )

    def eat(self):
        """Mark the gum as eaten."""
        self.eaten = True


class SuperGum(Gum):
    """Represent a super pacgum."""

    def __init__(self, row, col):
        super().__init__(row, col)

        self.radius = 8
        self.color = SUPER_GUM_COLOR


# -------------------- Maze Class --------------------

class Maze:
    """Manage the maze grid, walls and gum objects."""

    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.gums = []
        self.super_gums = []

        self.create_gums()

    def get_center(self):
        row = len(self.grid) // 2
        col = len(self.grid[0]) // 2
        return row, col

    def create_gums(self):
        """Create gum objects in available maze cells."""

        for row in range(self.rows):
            for col in range(self.cols):

                cell = self.grid[row][col]
                position = (row, col)

                # Ignore completely enclosed cells.
                if cell == 15:
                    continue

                # Don't place gums on the player spawn.
                if position == PLAYER_SPAWN:
                    continue

                # Create super gums at designated positions.
                if position in SUPER_GUM_POSITIONS:
                    self.super_gums.append(
                        SuperGum(row, col)
                    )
                else:
                    self.gums.append(Gum(row, col))

    def has_wall(self, row, col, direction):
        """Check whether a cell has a wall in a given direction."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return True
        return bool(self.grid[row][col] & direction)

    def can_move(self, row, col, direction):
        """Check whether movement to a neighboring cell is possible."""

        if self.has_wall(row, col, direction):
            return False

        if direction == NORTH:
            next_row, next_col = row - 1, col
            opposite = SOUTH

        elif direction == EAST:
            next_row, next_col = row, col + 1
            opposite = WEST

        elif direction == SOUTH:
            next_row, next_col = row + 1, col
            opposite = NORTH

        elif direction == WEST:
            next_row, next_col = row, col - 1
            opposite = EAST

        else:
            return False

        if not (0 <= next_row < self.rows):
            return False

        if not (0 <= next_col < self.cols):
            return False

        return not self.has_wall(next_row, next_col, opposite)

    def draw_walls(self, screen):
        """Draw the walls according to the numerical grid."""

        for row in range(self.rows):
            for col in range(self.cols):

                cell = self.grid[row][col]

                x = col * TILE_SIZE
                y = row * TILE_SIZE + HUD_HEIGHT

                # Top wall
                if cell & NORTH:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (x, y), (x + TILE_SIZE, y), 3
                    )

                # Right wall
                if cell & EAST:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (x + TILE_SIZE, y),
                        (x + TILE_SIZE, y + TILE_SIZE), 3
                    )

                # Bottom wall
                if cell & SOUTH:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (x, y + TILE_SIZE),
                        (x + TILE_SIZE, y + TILE_SIZE), 3
                    )

                # Left wall
                if cell & WEST:
                    pygame.draw.line(
                        screen, WALL_COLOR,
                        (x, y), (x, y + TILE_SIZE), 3
                    )

    def draw_gums(self, screen):
        """Draw all normal and super gums."""

        for gum in self.gums:
            gum.draw(screen)

        for gum in self.super_gums:
            gum.draw(screen)

    def draw(self, screen):
        """Draw the complete maze."""

        self.draw_walls(screen)
        self.draw_gums(screen)

    def bfs(self, start, target):
        """Find the shortest path between two cells using BFS."""

        queue = deque([start])
        visited = {start: None}

        directions = [
            (NORTH, "n"),
            (EAST, "e"),
            (SOUTH, "s"),
            (WEST, "w")
        ]

        while queue:

            current = queue.popleft()

            if current == target:
                break

            row, col = current

            for direction, letter in directions:

                if self.can_move(row, col, direction):

                    if direction == NORTH:
                        neighbor = (row - 1, col)
                    elif direction == EAST:
                        neighbor = (row, col + 1)
                    elif direction == SOUTH:
                        neighbor = (row + 1, col)
                    else:
                        neighbor = (row, col - 1)

                    if neighbor not in visited:
                        visited[neighbor] = (current, letter)
                        queue.append(neighbor)

        # Target was unreachable.
        if target not in visited:
            return None

        # Reconstruct the path.
        path = []
        current = target

        while current != start:
            previous, direction = visited[current]
            path.append(direction)
            current = previous

        return "".join(reversed(path))
    # -------------------- Main --------------------

def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption("Pac-Man - Development")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    maze = Maze(MAZE_GRID)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        title = font.render("PAC-MAN", True, (255, 220, 0))
        screen.blit(title, (15, 12))

        maze.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()