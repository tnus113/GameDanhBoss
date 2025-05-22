import pygame
import math
from bullet import BossBullet, SpecialBullet

class Boss(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(400, 80))
        self.hp = 300
        self.direction = 1
        self.attack_timer = 0
        self.phase = 1

    def update(self):
        self.rect.x += self.direction * 2
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1
        self.attack_timer += 1
        bullets = []
        if self.attack_timer >= 30:
            bullets = list(self.attack())
            self.attack_timer = 1
        if self.hp < 200: self.phase = 2
        if self.hp < 50: self.phase = 3
        return bullets


    def attack(self):
        if self.phase == 1:
            yield BossBullet(self.rect.centerx, self.rect.bottom)
        elif self.phase == 2:
            for i in [-1, 0, 1]:
                yield BossBullet(self.rect.centerx + i*15, self.rect.bottom)
        elif self.phase == 3:
            for angle in range(0, 360, 30):
                dx = 5 * math.cos(math.radians(angle))
                dy = 5 * math.sin(math.radians(angle))
                yield SpecialBullet(self.rect.centerx, self.rect.centery, dx, dy, "boss")
