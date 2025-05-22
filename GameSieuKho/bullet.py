import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.dy = -8

    def update(self):
        self.rect.y += self.dy
        if self.rect.bottom < 0:
            self.kill()

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/bullet.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.dy = 5

    def update(self):
        self.rect.y += self.dy
        if self.rect.top > 600:
            self.kill()

class SpecialBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, owner="player"):
        super().__init__()
        color = "special_bullet.png" if owner == "player" else "bullet.png"
        self.image = pygame.image.load(f"assets/{color}").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if not pygame.Rect(0, 0, 800, 600).collidepoint(self.rect.center):
            self.kill()
