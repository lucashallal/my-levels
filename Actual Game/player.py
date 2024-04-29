import pygame
from sys import exit
class Player(pygame.sprite.Sprite):
    def __init__(self, changed):
        super().__init__()
        if not changed: self.rect = pygame.Rect(90, 810, 50, 150)
        else: self.rect = pygame.Rect(90, 510, 50, 150)
        self.image = pygame.transform.scale_by(pygame.image.load('../Graphics/fox.png').convert_alpha(), 0.3)
        self.image.set_colorkey("White")
        self.gravity = 0

        self.on_ground = True
        self.on_death_ground = False
        self.infinite_jump = False
        self.win = False
        self.changed = changed
        self.screen = pygame.display.get_surface()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.infinite_jump or self.on_ground or self.on_death_ground: self.gravity = -20; self.on_ground = False
                if event.key == pygame.K_ESCAPE: pygame.quit(); exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.left > 0: self.rect.x -= 6
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.right < 1470 or not self.changed: self.rect.x += 6

    def gravity_control(self):
        if self.gravity < 25: self.gravity += 1
        self.rect.y += self.gravity

    def draw(self):
        x = self.rect.centerx - self.image.get_width() / 2
        y = self.rect.centery - self.image.get_height() / 2
        self.screen.blit(self.image, (x, y))

    def attain_mushroom(self):
        # insert sfx
        print("Got mushroom")

    def attain_propeller(self):
        # insert sfx
        print("Got propeller")
        self.infinite_jump = True

    def update(self, height):
        self.input()
        if not self.win:
            if not self.on_ground: self.gravity_control()
            else: self.gravity = 0
            if self.rect.bottom > height:
                if self.changed: pygame.quit(); exit()
                else: self.on_ground = True