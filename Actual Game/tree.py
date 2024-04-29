import pygame
class Tree:
    def __init__(self, name, player, ground_levels, hitbox):
        self.player = player
        self.ground_levels = ground_levels
        self.hitbox = hitbox

        if name == "tree":
            self.image = pygame.transform.scale(pygame.image.load('../Graphics/tree.png').convert_alpha(), (645, 800))
            self.rect_1 = pygame.Rect(0, 645, 550, 25)
            self.rect_2 = pygame.Rect(200, 790, 145, 1000)
            self.i = 0
        elif name == "tree2":
            self.image = pygame.transform.scale(pygame.image.load('../Graphics/tree2.png').convert_alpha(), (250, 1000))
            self.rect_1 = pygame.Rect(570, 345, 250, 25)
            self.rect_2 = pygame.Rect(650, 500, 90, 1000)
            self.i = 1
        else:
            self.image = pygame.transform.scale(pygame.image.load('../Graphics/tree2.png').convert_alpha(), (250, 1000))
            self.rect_1 = pygame.Rect(1150, 495, 250, 25)
            self.rect_2 = pygame.Rect(1230, 650, 90, 300)
            self.i = 2

    def collision(self):
        if (self.rect_1.collidepoint(self.player.sprite.rect.bottomright) or self.rect_1.collidepoint(self.player.sprite.rect.bottomleft)) and self.player.sprite.gravity >= 0:
            self.player.sprite.on_ground = True
            self.player.sprite.rect.bottom = self.ground_levels[self.i]
        if self.rect_2.colliderect(self.player.sprite.rect):
            tree_hitbox = self.hitbox(self.rect_2)
            if tree_hitbox == "Bottom":
                self.player.sprite.on_ground = True
                self.player.sprite.rect.bottom = self.rect_2.top + 1
            elif tree_hitbox == "Top":
                self.player.sprite.rect.y -= self.player.sprite.gravity
                self.player.sprite.gravity = 5
            elif tree_hitbox == "Left": self.player.sprite.rect.x -= 6
            else: self.player.sprite.rect.x += 6