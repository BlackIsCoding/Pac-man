from maze import Maze, MAZE_GRID, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, TILE_SIZE, HUD_HEIGHT, NORTH, WEST, SOUTH, EAST
import pygame
import sys
from ghost import Ghost, get_maze_corners

maze = Maze(MAZE_GRID)
pacman_row, pacman_col = maze.get_center()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
open_pac_right = pygame.image.load("../assets/pac_man_open_right.png")
closed_pac = pygame.image.load("../assets/pac_man_close.png")

colors = ["pink", "red", "yellow", "blue"]
ghosts = {}
for color in colors:
    string = f"../assets/ghost_{color}.png"
    ghosts[color] = pygame.image.load(string)
    ghosts[color] = pygame.transform.smoothscale(ghosts[color], (24,24))
red_ghost = Ghost(get_maze_corners((maze.rows, maze.cols))[0], ghosts['red'], 200, "red", maze, maze.get_center())
blue_ghost = Ghost(get_maze_corners((maze.rows, maze.cols))[1], ghosts['blue'], 200, "blue", maze, maze.get_center())
yellow_ghost = Ghost(get_maze_corners((maze.rows, maze.cols))[2], ghosts['yellow'], 200, "yellow",maze, maze.get_center())
pink_ghost = Ghost(get_maze_corners((maze.rows, maze.cols))[3], ghosts['pink'], 200, "pink", maze, maze.get_center())
ghosts_chars = [red_ghost, blue_ghost, yellow_ghost, pink_ghost]


collision = False
image_rect = open_pac_right.get_rect()
directions = [open_pac_right]
anime  = [closed_pac, open_pac_right]
for index, photo in enumerate(anime):
    anime[index] = pygame.transform.smoothscale(anime[index], (24,24))
movement = 2
x , y = 0 , 0
last_direction = None
i, count = 0, 0
key_hit = 0
screen_width, screen_height = screen.get_width(), screen.get_height()
pac_width, pac_height = anime[0].get_width(), anime[0].get_height()

maximum_x = screen_width - pac_width
maximum_y = screen_height - pac_height

last_move_time = 0
move_delay = 200

ghost_last_move = 0
ghost_move_delay = 600


ghost_last_intelligence = 0
ghost_intelligence_delay = 500

def get_spawn_position(maze, image):
    row, col = maze.get_center()

    center_x = col * TILE_SIZE + TILE_SIZE // 2
    center_y = row * TILE_SIZE + TILE_SIZE // 2 + HUD_HEIGHT

    x = center_x - image.get_width() // 2
    y = center_y - image.get_height() // 2

    return x, y
x, y = get_spawn_position(maze, anime[0])


pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("Pac-Man - Development")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

red_ghost.intelligence(maze.get_center())
print(red_ghost.path)

running = True

while running:
    if collision:
        print("you lost")
        sys.exit(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(1)
        elif event.type == pygame.KEYDOWN:
            key_hit = 1
            if event.key == pygame.K_RIGHT:
                last_direction = EAST
                direction = "right"
            elif event.key == pygame.K_LEFT:
                last_direction = WEST
                direction = "left"
            elif event.key == pygame.K_UP:
                last_direction = NORTH
                direction = "up"
            elif event.key == pygame.K_DOWN:
                last_direction = SOUTH
                direction = "down"


    if x < 0:
        x = 0

    if y < 0:
        y = 0
    if x > maximum_x:
        x = screen_width - pac_width
    if y > maximum_y:
        y = screen_height - pac_height
    if key_hit:
        anime[1] = pygame.image.load(f"../assets/pac_man_open_{direction}.png")
        anime[1] = pygame.transform.smoothscale(anime[1], (24,24))

    current_time = pygame.time.get_ticks()

    if last_direction is not None:
        if current_time - last_move_time >= move_delay:
            if last_direction == EAST:
                if maze.can_move(pacman_row,pacman_col, EAST):
                    pacman_col += 1
            elif last_direction == WEST:
                if maze.can_move(pacman_row,pacman_col, WEST):
                    pacman_col -= 1
            elif last_direction == NORTH:
                if maze.can_move(pacman_row,pacman_col, NORTH):
                    pacman_row -= 1
            elif last_direction == SOUTH:
                if maze.can_move(pacman_row,pacman_col, SOUTH):
                    pacman_row += 1
            last_move_time = current_time
    x = pacman_col * TILE_SIZE + TILE_SIZE // 2 - pac_width // 2
    y = pacman_row * TILE_SIZE + TILE_SIZE // 2 + HUD_HEIGHT - pac_height // 2
    
    for gum in maze.gums[:]:
        if (pacman_row, pacman_col) == (gum.row, gum.col):
            maze.gums.remove(gum)
            print("+50")
    for gum in maze.super_gums[:]:
        if (pacman_row, pacman_col) == (gum.row, gum.col):
            maze.super_gums.remove(gum)
            print("+200")
    if not maze.gums and not maze.super_gums:
        print("congrats, you finished the game !")
        sys.exit(1)
    for ghost in ghosts_chars:
        if ghost.grid_position == (pacman_row, pacman_col):
            collision = True

    screen.fill(BACKGROUND_COLOR)

    title = font.render("PAC-MAN", True, (255, 220, 0))
    screen.blit(title, (15, 12))

    maze.draw(screen)

    current_time = pygame.time.get_ticks()

    if current_time - ghost_last_intelligence >= ghost_intelligence_delay:
        red_ghost.intelligence((pacman_row, pacman_col))
        ghost_last_intelligence = current_time


    current_time = pygame.time.get_ticks()

    if current_time - ghost_last_move >= ghost_move_delay:
        red_ghost.move()
        ghost_last_move = current_time


    red_ghost.display_ghost(screen)
    blue_ghost.display_ghost(screen)
    yellow_ghost.display_ghost(screen)
    pink_ghost.display_ghost(screen)

    if count > 50:
        count = 0
        i += 1
        
    screen.blit(anime[i % len(anime)], (x, y))
    count += 1
    pygame.display.flip()

pygame.quit()
sys.exit()


