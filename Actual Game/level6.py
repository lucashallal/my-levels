import pygame
from sys import exit
from graphics import load_assets6
from player import Player
from tree import Tree

class Game6():
    def __init__(self, hitbox_shower, progressive_powerup):
        # basics
        self.hitbox_shower = hitbox_shower
        self.progressive_powerup = progressive_powerup
        self.enemy, self.mushroom, self.piranha, self.propeller, self.question_block, self.hit_block, self.spike, self.spike_ceiling, self.spike_trap, self.arrow, self.text, self.sky = load_assets6()
        pygame.init()
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption("O-Mario")
        self.clock = pygame.time.Clock()

        # ground levels
        self.ground_levels = [660, 360, 510]

        # enemies stuff
        self.enemy_rect = self.enemy.get_rect(topleft=(1225, 420))
        self.enemy_movement = 1
        self.spike_rect = self.spike.get_rect(topleft=(1240, 395))
        self.ceiling_rect = pygame.Rect(0, 0, 1500, 15)
        self.trap_rect = self.spike_trap.get_rect(topleft=(1320, 780))
        self.spike_movement = 1
        self.piranha_rect = self.piranha.get_rect(topleft=(730, 770))
        self.piranha_movement = 7
        self.piranha_movement_checker = 0
        self.piranha_movement_resetter = True
        self.piranha_movement_checker_resetter = True
        self.can_kill = [self.enemy_rect, self.piranha_rect, self.spike_rect, self.ceiling_rect, self.trap_rect]
        self.invinc_frames = 0

        # blocks and powerups stuff
        self.block_rect = self.question_block.get_rect(topleft=(80, 360))
        self.hasnt_hit_block = True
        self.powerup_command = False
        self.powerup_command_copy = False
        self.propeller_rect = self.propeller.get_rect(topleft=(55, 260))
        self.mushroom_rect = self.mushroom.get_rect(topleft=(80, 280))
        self.powerup_speed = -12
        self.invincibility = False

        # creating objects for classes
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(True))
        self.tree = Tree("tree", self.player, self.ground_levels, self.hitbox)
        self.tree2 = Tree("tree2", self.player, self.ground_levels, self.hitbox)
        self.tree3 = Tree("tree3", self.player, self.ground_levels, self.hitbox)

        # win condition stuff
        self.win_rect = pygame.Rect(1300, 800, 200, 50)

    # main loop
    def update(self):
        if not self.player.sprite.win:
            # put stuff on screen
            self.screen.blit(self.sky, (-800, -600))
            if self.hitbox_shower: self.show_hitboxes()
            self.screen.blit(self.tree.image, (-50, 600))
            self.screen.blit(self.tree2.image, (570, 350))
            self.screen.blit(self.tree3.image, (1150, 500))
            if self.powerup_command_copy:
                self.powerup_speed += 1
                if self.progressive_powerup:
                    self.screen.blit(self.propeller, self.propeller_rect)
                    if self.propeller_rect.bottom < self.block_rect.top or self.powerup_speed < 0: self.propeller_rect.y += self.powerup_speed
                    if self.player.sprite.rect.colliderect(self.propeller_rect):
                        self.player.sprite.attain_propeller()
                        self.powerup_command_copy = False
                else:
                    self.screen.blit(self.mushroom, self.mushroom_rect)
                    if self.mushroom_rect.bottom < self.block_rect.top or self.powerup_speed < 0: self.mushroom_rect.y += self.powerup_speed
                    if self.player.sprite.rect.colliderect(self.mushroom_rect):
                        self.player.sprite.attain_mushroom()
                        self.powerup_command_copy = False
            if self.hasnt_hit_block: self.screen.blit(self.question_block, self.block_rect)
            else: self.screen.blit(self.hit_block, self.block_rect)
            self.screen.blit(self.spike, self.spike_rect)
            self.screen.blit(self.spike_ceiling, (0, 0))
            self.screen.blit(self.spike_ceiling, (215, 0))
            self.screen.blit(self.spike_ceiling, (430, 0))
            self.screen.blit(self.spike_ceiling, (645, 0))
            self.screen.blit(self.spike_ceiling, (860, 0))
            self.screen.blit(self.spike_ceiling, (1075, 0))
            self.screen.blit(self.spike_ceiling, (1290, 0))
            self.screen.blit(self.enemy, self.enemy_rect)
            self.screen.blit(self.piranha, self.piranha_rect)

            # enemies movement
            if self.enemy_rect.x > 1325 or self.enemy_rect.x < 1147: self.enemy_movement *= -1; self.spike_movement *= -1
            self.piranha_movement_checker += 1
            if self.piranha_rect.x > 1130:
                self.piranha_movement = -2
                self.piranha_movement_resetter = True
                self.piranha_movement_checker_resetter = True
            if self.piranha_rect.x < 724:
                if self.piranha_movement_resetter:
                    self.piranha_movement = 0
                    self.piranha_movement_resetter = False
                if self.piranha_movement_checker_resetter:
                    self.piranha_movement_checker = 0
                    self.piranha_movement_checker_resetter = False
                if self.piranha_movement_checker > 100: self.piranha_movement = 7
            self.enemy_rect.x += self.enemy_movement
            self.spike_rect.x += self.spike_movement
            self.piranha_rect.x += self.piranha_movement

            # death
            self.player.sprite.on_death_ground = False
            for thing in self.can_kill:
                if self.player.sprite.rect.colliderect(thing):
                    if thing == self.trap_rect:
                        if self.hitbox_shower: pygame.draw.rect(self.screen, "Purple", self.trap_rect)
                        self.screen.blit(self.spike_trap, self.trap_rect)
                        self.screen.blit(self.arrow, (1150, 910))
                        pygame.display.update()
                        self.player.sprite.rect.bottom = 780
                        self.player.sprite.on_death_ground = True
                    if thing == self.ceiling_rect:
                        self.player.sprite.rect.y -= self.player.sprite.gravity
                        self.player.sprite.gravity = min(-self.player.sprite.gravity, 15)
                    if self.powerup_command or self.invincibility:
                        self.powerup_command = False
                        self.player.sprite.infinite_jump = False
                        self.invincibility = True
                    else: pygame.quit(); exit()

            # invincibility frames
            if self.invincibility:
                self.invinc_frames += 1
                if self.invinc_frames > 121: self.invincibility = False

            # block logic
            if self.player.sprite.rect.colliderect(self.block_rect):
                block_hitbox = self.hitbox(self.block_rect)
                if block_hitbox == "Top":
                    if self.hasnt_hit_block:
                        self.powerup_command = True
                        self.powerup_command_copy = True
                        self.hasnt_hit_block = False
                    self.player.sprite.rect.y -= self.player.sprite.gravity
                    self.player.sprite.gravity = 5
                elif block_hitbox == "Bottom":
                    self.player.sprite.on_ground = True
                    self.player.sprite.rect.bottom = self.block_rect.top + 1
                elif block_hitbox == "Left": self.player.sprite.rect.x -= 6
                else: self.player.sprite.rect.x += 6

            # ground collisions
            else:
                self.player.sprite.on_ground = False
                self.tree.collision()
                self.tree2.collision()
                self.tree3.collision()

        # finish loop and update stuff
        if self.player.sprite.rect.colliderect(self.win_rect): self.player.sprite.win = True
        if self.player.sprite.win: self.screen.fill("Green"); self.screen.blit(self.text, (300, 350))
        elif self.invinc_frames % 4 != 1: self.player.sprite.draw()
        self.player.sprite.update(1500)
        pygame.display.update()
        self.clock.tick(60)

    def show_hitboxes(self):
        # draw hitboxes if prompted by the user
        pygame.draw.rect(self.screen, "Purple", self.spike_rect)
        pygame.draw.rect(self.screen, "Yellow", self.enemy_rect)
        pygame.draw.rect(self.screen, "Red", self.piranha_rect)
        pygame.draw.rect(self.screen, "Green", self.player.sprite.rect)
        pygame.draw.rect(self.screen, "Blue", self.tree.rect_1)
        pygame.draw.rect(self.screen, "Light Blue", self.tree.rect_2)
        pygame.draw.rect(self.screen, "Blue", self.tree2.rect_1)
        pygame.draw.rect(self.screen, "Light Blue", self.tree2.rect_2)
        pygame.draw.rect(self.screen, "Blue", self.tree3.rect_1)
        pygame.draw.rect(self.screen, "Light Blue", self.tree3.rect_2)
        pygame.draw.rect(self.screen, "Blue", self.ceiling_rect)
        pygame.draw.rect(self.screen, "Green", self.win_rect)
        if self.powerup_command_copy:
            if self.progressive_powerup: pygame.draw.rect(self.screen, "Black", self.propeller_rect)
            else: pygame.draw.rect(self.screen, "Black", self.mushroom_rect)

    def hitbox(self, item):
        # detect type of collision of the player and any item
        if self.player.sprite.rect.top - self.player.sprite.gravity >= item.bottom: return "Top"
        elif self.player.sprite.rect.bottom - self.player.sprite.gravity <= item.top + 1: return "Bottom"
        elif self.player.sprite.rect.left < item.centerx: return "Left"
        else: return "Right"