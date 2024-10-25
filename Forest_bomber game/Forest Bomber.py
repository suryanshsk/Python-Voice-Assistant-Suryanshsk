import sys
import os
import pygame
from pygame.locals import *

# Initialize Pygame and set up the display
pygame.init()
pygame.mixer.init()

# Define colors
WHITE = (255, 255, 255)
PURPLE = (96, 86, 154)
LIGHT_BLUE = (157, 220, 241)
DARK_BLUE = (63, 111, 182)
GREEN = (57, 180, 22)

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCOREBOARD_MARGIN = 4
LINE_HEIGHT = 18
BOX_WIDTH = 300
BOX_HEIGHT = 150
TOTAL_LEVELS = 4
TREE_SPACING = 40
FIRST_TREE = 140
GROUND_HEIGHT = 8
TREE_OFF_GROUND = 4
PLANE_START_X = 0
PLANE_START_Y = 54

# Setup display
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Forest Bomber')

# Load resources
background_image = pygame.image.load('background.png').convert()
tree_image = pygame.image.load('tree.png').convert_alpha()
burn_tree_image = pygame.image.load('burning_tree.png').convert_alpha()
plane_image = pygame.image.load('plane.png').convert_alpha()
burn_plane_image = pygame.image.load('burning_plane.png').convert_alpha()
bomb_image = pygame.image.load('bomb.png').convert_alpha()

# Load sounds
explosion_sound = pygame.mixer.Sound('explosion.ogg')
tree_sound = pygame.mixer.Sound('tree_explosion.ogg')

# Initialize variables
clock = pygame.time.Clock()
font = pygame.font.SysFont('Helvetica', 16)
level = 1
score = 0
hi_score = 0
speed_boost = 0
plane_exploded = False
level_cleared = False
plane_front = 0
plane_explode_sound_played = False
bomb_dropped = False
bomb = bomb_image.get_rect()
plane = plane_image.get_rect()
plane.x = PLANE_START_X
plane.y = PLANE_START_Y
tree = tree_image.get_rect()
tree.y = SCREEN_HEIGHT - tree.height - TREE_OFF_GROUND
burning_tree = 0
tree_timer = 0
burning_trees = []

# Define the forest layouts
forest_1 = ['T', '-', 'T', '-', '-', '-', 'T', '-', '-', '-', '-', 'T']
forest_2 = ['-', 'T', '-', '-', 'T', '-', 'T', '-', 'T', 'T', '-', 'T']
forest_3 = ['T', 'T', '-', '-', 'T', '-', 'T', 'T', 'T', 'T', '-', '-']
forest_4 = ['T', 'T', '-', '-', 'T', 'T', 'T', '-', 'T', 'T', 'T', '-']
forest = list(forest_1)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Check for key presses
    keys = pygame.key.get_pressed()
    
    # Space to drop bomb
    if keys[pygame.K_SPACE]:
        if not bomb_dropped and not level_cleared and not plane_exploded:
            bomb_dropped = True
            bomb.x = plane.x + 15
            bomb.y = plane.y + 10

    # Enter to restart game or move to next level
    if keys[pygame.K_RETURN]:
        if plane_exploded or (level == TOTAL_LEVELS and level_cleared):
            plane_exploded = False
            plane_explode_sound_played = False
            score = 0
            speed_boost = 0
            level = 1
            forest = list(forest_1)
            plane.x = PLANE_START_X
            plane.y = PLANE_START_Y
            level_cleared = False
        elif level_cleared:
            level += 1
            level_cleared = False
            if level == 2:
                forest = list(forest_2)
            elif level == 3:
                forest = list(forest_3)
                speed_boost = 1
            else:
                forest = list(forest_4)
                speed_boost = 1
            plane.x = PLANE_START_X
            plane.y = PLANE_START_Y

    # Update plane position
    if not level_cleared and not plane_exploded:
        plane.x += 5 + speed_boost
        if plane.x >= SCREEN_WIDTH:
            plane.x = 0
            plane.y += 100

    # Update bomb position
    if bomb_dropped:
        bomb.y += 5
        bomb.x += 3
        if bomb.y > SCREEN_HEIGHT or bomb.x > SCREEN_WIDTH:
            bomb_dropped = False
        # Check if bomb hits a tree
        for column, forest_item in enumerate(forest):
            if forest_item == 'T':
                tree.x = FIRST_TREE + column * TREE_SPACING
                if bomb.colliderect(tree):
                    forest[column] = 'B'
                    bomb_dropped = False
                    burning_trees.append(column)
                    tree_timer = 10
                    score += 10 * level
                    tree_sound.play()

    # Update burning trees
    if tree_timer > 0:
        tree_timer -= 1
        if tree_timer == 0:
            for column in burning_trees:
                forest[column] = '-'
            burning_trees.clear()

    # Check if plane crashes into tree or reaches the end of the level
    if plane.y >= SCREEN_HEIGHT - plane.height - GROUND_HEIGHT:
        plane_front = plane.x + plane.width
        if plane_front >= SCREEN_WIDTH:
            level_cleared = True
        else:
            for column, forest_item in enumerate(forest):
                if forest_item == 'T' or forest_item == 'B':
                    tree_left = FIRST_TREE + column * TREE_SPACING
                    if plane_front >= tree_left:
                        plane_exploded = True

    # Check high score
    if score > hi_score:
        hi_score = score

    # Draw background and game objects
    game_screen.blit(background_image, [0, 0])
    
    # Draw trees
    for column, forest_item in enumerate(forest):
        tree.x = FIRST_TREE + column * TREE_SPACING
        if forest_item == 'T':
            game_screen.blit(tree_image, [tree.x, tree.y])
        elif forest_item == 'B':
            game_screen.blit(burn_tree_image, [tree.x, tree.y])

    # Draw plane
    if not plane_exploded:
        game_screen.blit(plane_image, [plane.x, plane.y])
    else:
        plane.y = SCREEN_HEIGHT - burn_plane_image.get_height() - TREE_OFF_GROUND
        game_screen.blit(burn_plane_image, [plane.x, plane.y])
    
    # Draw bomb
    if bomb_dropped:
        game_screen.blit(bomb_image, [bomb.x, bomb.y])

    # Draw scoreboard
    score_text = f"Score: {score}"
    hi_text = f"Hi Score: {hi_score}"
    level_text = f"Level: {level}"
    text = font.render(score_text, True, PURPLE)
    game_screen.blit(text, [SCOREBOARD_MARGIN, SCOREBOARD_MARGIN])
    text = font.render(hi_text, True, PURPLE)
    game_screen.blit(text, [SCREEN_WIDTH - text.get_width() - SCOREBOARD_MARGIN, SCOREBOARD_MARGIN])
    text = font.render(level_text, True, PURPLE)
    game_screen.blit(text, [(SCREEN_WIDTH - text.get_width()) // 2, SCOREBOARD_MARGIN])

    # Game over or level cleared message
    if plane_exploded or level_cleared:
        if plane_exploded and not plane_explode_sound_played:
            explosion_sound.play()
            plane_explode_sound_played = True
        if plane_exploded:
            text_line_1 = font.render('GAME OVER', True, WHITE)
        elif level == TOTAL_LEVELS:
            text_line_1 = font.render('GAME OVER - ALL LEVELS CLEARED', True, WHITE)
        else:
            text_line_1 = font.render(f'LEVEL {level} CLEARED', True, WHITE)
        text_line_2 = font.render('RETURN for new game or level', True, WHITE)
        pygame.draw.rect(game_screen, DARK_BLUE, [(SCREEN_WIDTH - BOX_WIDTH) // 2, (SCREEN_HEIGHT - BOX_HEIGHT) // 2, BOX_WIDTH, BOX_HEIGHT])
        game_screen.blit(text_line_1, [(SCREEN_WIDTH - text_line_1.get_width()) // 2, SCREEN_HEIGHT // 2 - LINE_HEIGHT])
        game_screen.blit(text_line_2, [(SCREEN_WIDTH - text_line_2.get_width()) // 2, SCREEN_HEIGHT // 2 + LINE_HEIGHT])

    # Update the display and set the game FPS
    pygame.display.update()
    clock.tick(30)
