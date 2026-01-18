import pygame
from constant import WH

from Classes.explosion import Explosion


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self, groups, color, pos, explosion_group, explosion_surf, enemy_laser_group
    ):
        super().__init__(groups)

        self.color = color
        self.explosion_group = explosion_group
        self.explosion_surf = explosion_surf
        self.enemy_laser_group = enemy_laser_group

        if color == "green":
            self.image = pygame.image.load(
                "./Graphics/enemyUFO_grn.png"
            ).convert_alpha()
            self.rect = self.image.get_rect(center=pos)
            self.mask = pygame.mask.from_surface(self.image)
        elif color == "yellow":
            self.image = pygame.image.load(
                "./Graphics/enemyUFO_ylw.png"
            ).convert_alpha()
            self.rect = self.image.get_rect(center=pos)
            self.mask = pygame.mask.from_surface(self.image)
        elif color == "red":
            self.image = pygame.image.load(
                "./Graphics/enemyUFO_red.png"
            ).convert_alpha()
            self.rect = self.image.get_rect(center=pos)
            self.mask = pygame.mask.from_surface(self.image)

    def shoot_laser(self):
        EnemyLaser(pos=self.rect.midbottom, groups=self.enemy_laser_group)

    def check_player_laser_collision(self, player_laser_group):
        if pygame.sprite.spritecollide(
            self, player_laser_group, True, pygame.sprite.collide_mask
        ):
            Explosion(self.rect.center, self.explosion_group, self.explosion_surf)
            self.kill()
            return True


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./Graphics/laserRed.png").convert_alpha()
        self.rect = self.image.get_rect(midtop=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 300

    def update(self, dt):
        self.rect.y += self.speed * dt
        if self.rect.top > 800:
            self.kill()
