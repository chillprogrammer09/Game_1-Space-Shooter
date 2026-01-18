import pygame

WW, WH = 1280, 800

ENEMY_ROW = 3
ENEMY_COLUMN = 11
ENEMY_X_SPACING = 111
ENEMY_Y_SPACING = 121
EXTRASPACE_X = 95
EXTRASPACE_Y = 80

row_colors = ["red", "yellow", "green"]

# Timer events
ENEMY_SHOOT = pygame.USEREVENT + 1
