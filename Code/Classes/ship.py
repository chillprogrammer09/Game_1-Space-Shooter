import pygame
from constant import WH, WW


class Ship(pygame.sprite.Sprite):
    def __init__(self, groups, player_laser_group, laser_class):
        super().__init__(groups)
        self.image = pygame.image.load("./Graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(WW / 2, WH))
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 300
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()

        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 500
        self.player_laser_group = player_laser_group

        self.health = 3
        self.invulenerable_time = 0
        self.invulenerable_duration = 2000
        self.laser_class = laser_class

    def shoot_laser(self):
        self.laser_class(self.rect.midtop, self.player_laser_group)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot_laser()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def recharge_laser(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.cooldown_duration:
                self.can_shoot = True

    def check_enemy_laser_collision(self, enemy_laser_group):
        if not self.is_invulnerable():
            if pygame.sprite.spritecollide(
                self, enemy_laser_group, True, pygame.sprite.collide_mask
            ):
                self.health -= 1
                self.invulenerable_time = pygame.time.get_ticks()
                return True
            return False

    def is_invulnerable(self):
        if self.invulenerable_time > 0:
            current_time = pygame.time.get_ticks()
            return (
                current_time - self.invulenerable_duration < self.invulenerable_duration
            )
        return False

    def update(self, dt):
        self.get_input()
        self.pos.x += self.direction.x * self.speed * dt
        self.recharge_laser()
        self.rect.x = round(self.pos.x)
