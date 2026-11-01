import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1600, 1000))
open_pac_right = pygame.image.load("../assets/pac_man_open_right.png")
closed_pac = pygame.image.load("../assets/pac_man_close.png")
image_rect = open_pac_right.get_rect()
directions = [open_pac_right]
anime  = [closed_pac, open_pac_right]
movement = 2
x , y = 0 , 0
last_direction = None
i, count = 0, 0
key_hit = 0



screen_width, screen_height = screen.get_width(), screen.get_height()
pac_width, pac_height = closed_pac.get_width(), closed_pac.get_height()

maximum_x = screen_width - pac_width
maximum_y = screen_height - pac_height



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(1)
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if image_rect.collidepoint(event.pos):
        #         print("open_pac_right image clicked!")
        elif event.type == pygame.KEYDOWN:
            key_hit = 1
            if event.key == pygame.K_RIGHT:
                last_direction = "right"
            elif event.key == pygame.K_LEFT:
                last_direction = "left"
            elif event.key == pygame.K_UP:
                last_direction = "up"
            elif event.key == pygame.K_DOWN:
                last_direction = "down"

 
    if x < 0:
        x = 0

    if y < 0:
        y = 0

    if x > maximum_x:
        x = screen_width - pac_width
    if y > maximum_y:
        y = screen_height - pac_height

    if key_hit:
        anime[1] = pygame.image.load(f"../assets/pac_man_open_{last_direction}.png")
    if last_direction == "right":
        x += movement
    elif last_direction == "left":
        x -= movement
    elif last_direction == "up":
        y -= movement
    elif last_direction == "down":
        y += movement


    screen.fill("black")
    if count > 50:
        count = 0
        i += 1
    screen.blit(anime[i % len(anime)], (x, y))
    count += 1
    pygame.display.flip()

# clicked = False
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit(1)

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if image_rect.collidepoint(event.pos):
#                 clicked = True

#         if event.type == pygame.MOUSEBUTTONUP:
#             clicked = False

#     screen.fill("yellow")

#     if clicked:
#         scaled = pygame.transform.smoothscale(
#             berserk,
#             (int(berserk.get_width() * 0.95),
#              int(berserk.get_height() * 0.95))
#         )
#         rect = scaled.get_rect(center=image_rect.center)
#         screen.blit(scaled, rect)
#     else:
#         screen.blit(berserk, image_rect)

#     pygame.display.flip()