import random
import os
import sys
import json
from colorama import Fore, Back, Style, init

init(autoreset=True)

score = 0
history = []
high_score = 0

def initialize_game():
    board = [[0]*4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def get_tile_color(value):
    """Assign colors based on tile value."""
    if value == 2:
        return Fore.BLACK + Back.WHITE
    elif value == 4:
        return Fore.BLACK + Back.CYAN
    elif value == 8:
        return Fore.WHITE + Back.BLUE
    elif value == 16:
        return Fore.WHITE + Back.MAGENTA
    elif value == 32:
        return Fore.BLACK + Back.YELLOW
    elif value == 64:
        return Fore.BLACK + Back.RED
    elif value == 128:
        return Fore.WHITE + Back.GREEN
    elif value == 256:
        return Fore.WHITE + Back.CYAN
    elif value == 512:
        return Fore.WHITE + Back.MAGENTA
    elif value == 1024:
        return Fore.BLACK + Back.YELLOW
    elif value == 2048:
        return Fore.BLACK + Back.GREEN
    else:
        return Fore.RESET + Back.RESET

def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Score: {score} | High Score: {high_score}")
    
    for row in board:
        print('+----' * 4 + '+')
        for num in row:
            color = get_tile_color(num)
            print(f'|{color}{str(num).center(4) if num != 0 else "    "}', end="")
        print(Style.RESET_ALL + "|")
    print('+----' * 4 + '+')

def move_left(board):
    for row in board:
        compress_row(row)
    return board

def move_right(board):
    for row in board:
        row.reverse()
        compress_row(row)
        row.reverse()
    return board

def move_up(board):
    for col in range(4):
        column = [board[row][col] for row in range(4)]
        compress_row(column)
        for row in range(4):
            board[row][col] = column[row]
    return board

def move_down(board):
    for col in range(4):
        column = [board[row][col] for row in range(4)]
        column.reverse()
        compress_row(column)
        column.reverse()
        for row in range(4):
            board[row][col] = column[row]
    return board

def compress_row(row):
    global score
    new_row = [num for num in row if num != 0] + [0] * (4 - len([num for num in row if num != 0]))
    
    for i in range(3):  
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            score += new_row[i]  
            new_row[i + 1] = 0
    
    final_row = [num for num in new_row if num != 0] + [0] * (4 - len([num for num in new_row if num != 0]))
    row[:] = final_row  

def game_won(board):
    return any(2048 in row for row in board)

def game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
    return True

def save_high_score(score, filename="highscore.json"):
    global high_score
    if score > high_score:
        high_score = score
        with open(filename, 'w') as f:
            json.dump({"high_score": high_score}, f)

def load_high_score(filename="highscore.json"):
    global high_score
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            high_score = data.get("high_score", 0)
    except FileNotFoundError:
        high_score = 0

def main():
    global score, history
    
    load_high_score()  
    board = initialize_game()
    
    while True: 
        print_board(board)
        if game_won(board):
            print("Yayy, You've won the game!")
            save_high_score(score)
            break
        if game_over(board):
            print("Game Over! No more moves are possible.")
            save_high_score(score)
            break

        move = input("Enter move (ULDR for up, left, down, right, O for undo, or Q to quit): ").upper()
        if move == 'Q':
            print("Thanks for playing!")
            save_high_score(score)
            break

        original_board = [row[:] for row in board]
        history.append((original_board, score))  
        
        if move == 'O' and history:
            board, score = history.pop()  
            continue
        
        if move == 'U':
            move_up(board)
        elif move == 'L':
            move_left(board)
        elif move == 'D':
            move_down(board)
        elif move == 'R':
            move_right(board)
        else:
            print("Invalid input, please enter U, L, D, R or Q")
            continue
        
        if board != original_board:
            add_new_tile(board)
            
if __name__ == "__main__":
    main()

        