import pygame
from level5 import Game5
from level6 import Game6

if input("Show hitboxes? ") == "y": hitbox_shower = True
else: hitbox_shower = False
if input("Do you have a mushroom? ") == "y": progressive_powerup = True
else: progressive_powerup = False

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("O-Mario")
clock = pygame.time.Clock()

level5 = Game5()
next_level = False
changed = False

while True:
    if not changed: next_level = level5.update(next_level)
    else: level6.update()

    if next_level:
        next_level = False
        changed = True
        del level5
        level6 = Game6(hitbox_shower, progressive_powerup)

    pygame.display.update()
    clock.tick(60)