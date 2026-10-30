import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
berserk = pygame.image.load("berserk.jpeg")
image_rect = berserk.get_rect()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit(1)
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if image_rect.collidepoint(event.pos):
#                 print("Berserk image clicked!")
#     screen.fill("yellow")
#     # screen.blit(berserk, (100, 100))
#     pygame.display.flip()

clicked = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if image_rect.collidepoint(event.pos):
                clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

    screen.fill("yellow")

    if clicked:
        scaled = pygame.transform.smoothscale(
            berserk,
            (int(berserk.get_width() * 0.95),
             int(berserk.get_height() * 0.95))
        )
        rect = scaled.get_rect(center=image_rect.center)
        screen.blit(scaled, rect)
    else:
        screen.blit(berserk, image_rect)

    pygame.display.flip()