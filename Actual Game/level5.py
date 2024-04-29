import pygame
from graphics import load_assets5
from player import Player

class Game5():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.get_surface()
        self.brick_block, self.thwomp, self.wing, self.pipe, self.enemy, self.mushroom, self.question_block, self.hit_block, self.spike_trap, self.sky = load_assets5()
        pygame.display.set_caption("O-Mario")
        self.clock = pygame.time.Clock()

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(False))

        self.sky_rect = self.sky.get_rect(topleft=(-800, -600))
        self.brick_block_rect = self.brick_block.get_rect(topleft=(0, 0))
        self.thwomp_rect = self.thwomp.get_rect(topleft=(200, 0))
        self.wing_rect = self.wing.get_rect(topleft=(400, 0))
        self.pipe_rect = self.pipe.get_rect(topleft=(600, 0))
        self.enemy_rect = self.enemy.get_rect(topleft=(800, 0))
        self.mushroom_rect = self.mushroom.get_rect(topleft=(0, 200))
        self.question_block_rect = self.question_block.get_rect(topleft=(0, 400))
        self.hit_block_rect = self.hit_block.get_rect(topleft=(0, 600))
        self.spike_trap_rect = self.spike_trap.get_rect(topleft=(400, 400))

        self.rects = [self.brick_block_rect,
                 self.thwomp_rect,
                 self.wing_rect,
                 self.pipe_rect,
                 self.enemy_rect,
                 self.mushroom_rect,
                 self.question_block_rect,
                 self.hit_block_rect,
                 self.spike_trap_rect]

    def update(self, next_level):
        self.screen.blit(self.sky, self.sky_rect)
        self.screen.blit(self.brick_block, self.brick_block_rect)
        self.screen.blit(self.thwomp, self.thwomp_rect)
        self.screen.blit(self.wing, self.wing_rect)
        self.screen.blit(self.pipe, self.pipe_rect)
        self.screen.blit(self.enemy, self.enemy_rect)
        self.screen.blit(self.mushroom, self.mushroom_rect)
        self.screen.blit(self.question_block, self.question_block_rect)
        self.screen.blit(self.hit_block, self.hit_block_rect)
        self.screen.blit(self.spike_trap, self.spike_trap_rect)

        self.player.sprite.draw()
        self.player.sprite.update(self.screen.get_height())

        if self.player.sprite.rect.left > self.screen.get_width(): next_level = True

        pygame.display.update()
        self.clock.tick(60)

        return next_level