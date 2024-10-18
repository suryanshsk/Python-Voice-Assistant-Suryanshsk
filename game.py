import pygame
import time
import random
import os
import pandas as pd


# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Display settings
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Snake settings
snake_block = 10
snake_speed = 7

clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Load the dataset
def load_dataset(csv_file_path):
    return pd.read_csv(csv_file_path)

# Map the "Mean" column to BCI commands
def map_mean_to_command(mean_value):
    if mean_value < -1:  # Low values
        return 'left'
    elif mean_value > 1:  # High values
        return 'right'
    elif -1 <= mean_value <= 0:  # Medium-low values
        return 'up'
    else:  # Medium-high values
        return 'down'

# Get BCI command based on the dataset
def get_bci_command(dataset):
    mean_value = dataset['Mean'].sample().values[0]
    return map_mean_to_command(mean_value)

# Main Game Loop
def gameLoop(dataset):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(dataset)

        # Get BCI command
        bci_command = get_bci_command(dataset)

        if bci_command == 'left':
            x1_change = -snake_block
            y1_change = 0
        elif bci_command == 'right':
            x1_change = snake_block
            y1_change = 0
        elif bci_command == 'up':
            y1_change = -snake_block
            x1_change = 0
        elif bci_command == 'down':
            y1_change = snake_block
            x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:  #hit the wall
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:      # collision detection
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Paths
csv_file_path = r'C:\Users\hp\OneDrive\Desktop\pandas\FinalDataset.csv'


# Step 1: Load the dataset
dataset = load_dataset(csv_file_path)

# Start the game
gameLoop(dataset)
