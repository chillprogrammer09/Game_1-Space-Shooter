import random
import sys
import os
import pygame

from Classes.enemy import Enemy, EnemyLaser
from Classes.explosion import Explosion
from Classes.laser import Laser
from Classes.ship import Ship
from constant import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

# Game state
is_alive = True
did_win = False
score = 0
level = 1

# Initialize pygame
pygame.init()

# Fonts
font = pygame.font.Font(None, 36)
pixel_font = pygame.font.Font("./Graphics/pixelfont.otf", 108)
pixel_font_small = pygame.font.Font("Graphics/pixelfont.otf", 50)

# Display setup
display_surf = pygame.display.set_mode((WW, WH))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Background
background_surf = pygame.image.load("./Graphics/starBackground.png").convert()
background_surf = pygame.transform.scale(background_surf, (WW, WH))

# Assets
explosion_surf = pygame.image.load("./Graphics/explosion.png").convert_alpha()

# Sprite groups
spaceship_group = pygame.sprite.GroupSingle()
player_laser_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_laser_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# Create player ship
ship = Ship(spaceship_group, player_laser_group, Laser)

# Timer events
pygame.time.set_timer(ENEMY_SHOOT, 1000)


# Create enemy formation
def create_enemy_formation():
    for row_index, color in enumerate(row_colors):
        for column_index in range(ENEMY_COLUMN):
            x = EXTRASPACE_X + column_index * ENEMY_X_SPACING
            y = EXTRASPACE_Y + row_index * ENEMY_Y_SPACING
            Enemy(
                color=color,
                pos=(x, y),
                groups=enemy_group,
                explosion_group=explosion_group,
                explosion_surf=explosion_surf,
                enemy_laser_group=enemy_laser_group,
            )


create_enemy_formation()

# UI overlays
overlay = pygame.Surface((WW, WH))
overlay.fill((128, 128, 128))

# UI text
game_over_font = pixel_font.render("GAME OVER:", False, "Red")
game_over_font_rect = game_over_font.get_rect(center=(WW / 2, WH / 2))

restart_text = pixel_font_small.render("RESTART", True, (0, 255, 0))
quit_text = pixel_font_small.render("QUIT", True, (255, 0, 0))
victory_font = pixel_font.render("VICTORY", False, (255, 223, 0))
defeat_font = pixel_font.render("DEFEAT", False, (128, 0, 128))

# UI rectangles
victory_font_rect = victory_font.get_rect(center=(WW // 2, WH // 2 - 200))
defeat_font_rect = defeat_font.get_rect(center=(WW // 2, WH // 2 - 200))
restart_rect = restart_text.get_rect(center=(WW // 2 - 100, WH // 2 + 200))
quit_rect = quit_text.get_rect(center=(WW // 2 + 100, WH // 2 + 200))


def reset_game():
    global score, level, is_alive, did_win
    score = 0
    level = 1
    is_alive = True
    did_win = False

    # Reset player
    ship.health = 3
    ship.rect.midbottom = (WW // 2, WH)
    ship.pos = pygame.math.Vector2(ship.rect.topleft)

    # Clear all sprites
    player_laser_group.empty()
    enemy_laser_group.empty()
    enemy_group.empty()
    explosion_group.empty()

    # Recreate enemies
    create_enemy_formation()


def handle_events():
    global is_alive, score, level, did_win

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == ENEMY_SHOOT and is_alive:
            if enemy_group.sprites():
                random_enemy = random.choice(enemy_group.sprites())
                random_enemy.shoot_laser()

        if event.type == pygame.MOUSEBUTTONDOWN and not is_alive:
            if restart_rect.collidepoint(event.pos):
                reset_game()
            elif quit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()


def update_game(dt):
    global is_alive, did_win, score

    # Update all sprite groups
    spaceship_group.update(dt)
    player_laser_group.update(dt)
    enemy_laser_group.update(dt)
    explosion_group.update()

    # Handle collisions
    for enemy in enemy_group.sprites():
        if enemy.check_player_laser_collision(player_laser_group):
            if enemy.color == "green":
                score += 5
            elif enemy.color == "yellow":
                score += 10
            elif enemy.color == "red":
                score += 15

    ship.check_enemy_laser_collision(enemy_laser_group)

    # Check win condition
    if len(enemy_group.sprites()) == 0:
        is_alive = False
        did_win = True


def draw_game():
    # Draw background
    display_surf.blit(background_surf, (0, 0))

    # Draw sprites
    spaceship_group.draw(display_surf)
    player_laser_group.draw(display_surf)
    enemy_group.draw(display_surf)
    enemy_laser_group.draw(display_surf)
    explosion_group.draw(display_surf)

    # Draw UI
    score_text = font.render(f"Score: {score}", True, "white")
    lives_text = font.render(f"Lives: {ship.health}", True, "yellow")
    level_text = font.render(f"Level: {level}", True, "white")

    display_surf.blit(level_text, (WW - 100, WH - 60))
    display_surf.blit(score_text, (WW - 100, WH - 96))
    display_surf.blit(lives_text, (WW - 100, WH - (96 + 36)))


def draw_victory_screen():
    display_surf.blit(overlay, (0, 0))
    display_surf.blit(victory_font, victory_font_rect)

    final_score_text = pixel_font.render(f"Final Score: {score}", True, "Black")
    final_score_rect = final_score_text.get_rect(center=(WW // 2, WH // 2 + 50))
    display_surf.blit(final_score_text, final_score_rect)
    display_surf.blit(restart_text, restart_rect)
    display_surf.blit(quit_text, quit_rect)
    pygame.draw.rect(display_surf, (0, 255, 0), restart_rect, 3)
    pygame.draw.rect(display_surf, (255, 0, 0), quit_rect, 3)


def draw_death_screen():
    display_surf.blit(overlay, (0, 0))
    display_surf.blit(game_over_font, game_over_font_rect)
    display_surf.blit(defeat_font, defeat_font_rect)

    final_score_text = pixel_font.render(f"Final Score: {score}", True, "Black")
    final_score_rect = final_score_text.get_rect(center=(WW // 2, WH // 2 + 80))
    display_surf.blit(final_score_text, final_score_rect)

    display_surf.blit(restart_text, restart_rect)
    display_surf.blit(quit_text, quit_rect)

    pygame.draw.rect(display_surf, (0, 255, 0), restart_rect, 3)
    pygame.draw.rect(display_surf, (255, 0, 0), quit_rect, 3)


# Main game loop
while True:
    # Check if player is dead
    if ship.health <= 0:
        is_alive = False

    # Handle events
    handle_events()

    if is_alive:
        dt = clock.tick(120) / 1000
        update_game(dt)
        draw_game()
    elif did_win:
        draw_victory_screen()
    else:
        draw_death_screen()

    pygame.display.update()
