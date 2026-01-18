import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lasts = 300

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.lasts:
            self.kill()
