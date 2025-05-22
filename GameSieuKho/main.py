import pygame
import math
from player import Player
from boss import Boss
from bullet import Bullet, SpecialBullet

pygame.init()
WIN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Đánh Boss Siêu Khó")
clock = pygame.time.Clock()

player_img = pygame.image.load("assets/player.png").convert_alpha()
boss_img = pygame.image.load("assets/boss.png").convert_alpha()
bullet_img = pygame.image.load("assets/bullet.png").convert_alpha()

font = pygame.font.SysFont("Arial", 20)

player = Player(player_img)
boss = Boss(boss_img)

player_group = pygame.sprite.Group(player)
boss_group = pygame.sprite.Group(boss)
player_bullets = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()

special_cooldown = 0
SPECIAL_MAX_COOLDOWN = 300

running = True
while running:
    clock.tick(60)
    WIN.fill((30, 30, 30))

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_bullets.add(Bullet(player.rect.centerx, player.rect.top, bullet_img))
            if event.key == pygame.K_z and special_cooldown == 0:
                for i in range(10):
                    angle = (360 / 10) * i
                    dx = 8 * math.cos(math.radians(angle))
                    dy = 8 * math.sin(math.radians(angle))
                    player_bullets.add(SpecialBullet(player.rect.centerx, player.rect.centery, dx, dy))

                special_cooldown = SPECIAL_MAX_COOLDOWN

    # Update
    player.update(keys)
    boss.update()

    player_bullets.update()
    boss_bullets.update()
    boss_bullets.add(*boss.update())

    # Collision
    for bullet in player_bullets:
        if boss.rect.colliderect(bullet.rect):
            boss.hp -= 10
            bullet.kill()

    for bullet in boss_bullets:
        if player.rect.colliderect(bullet.rect):
            player.hp -= 5
            bullet.kill()

    if player.hp <= 0:
        WIN.blit(font.render("Lose!", True, (255, 255, 255)), (300, 300))
        pygame.display.update()
        pygame.time.delay(3000)
        break

    if boss.hp <= 0:
        WIN.blit(font.render("Win!", True, (255, 255, 255)), (300, 300))
        pygame.display.update()
        pygame.time.delay(3000)
        break

    # Draw
    player_group.draw(WIN)
    boss_group.draw(WIN)
    player_bullets.draw(WIN)
    boss_bullets.draw(WIN)

    pygame.draw.rect(WIN, (100, 100, 100), (10, 10, 100, 10))
    pygame.draw.rect(WIN, (0, 255, 0), (10, 10, 100 * player.hp / 100, 10))

    pygame.draw.rect(WIN, (100, 100, 100), (690, 10, 100, 10))
    pygame.draw.rect(WIN, (255, 0, 0), (690, 10, 100 * boss.hp / 300, 10))

    pygame.draw.rect(WIN, (50, 50, 50), (10, 30, 100, 10))
    pygame.draw.rect(WIN, (0, 255, 255), (10, 30, 100 * (1 - special_cooldown / SPECIAL_MAX_COOLDOWN), 10))

    if special_cooldown > 0:
        special_cooldown -= 1

    pygame.display.update()

pygame.quit()
