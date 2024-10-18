M = 9
#This function prints the Sudoku grid in a readable format.
def puzzle(a):
    for i in range(M):
        for j in range(M):
            print(a[i][j], end=" ")
        print()

def solve(grid, row, col, num):
    # Check if the number is not present in the current row
    for x in range(9):
        if grid[row][x] == num:
            return False

    # Check if the number is not present in the current column
    for x in range(9):
        if grid[x][col] == num:
            return False

    # Check if the number is not present in the current 3x3 subgrid
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False

    return True

def Suduko(grid, row, col):
    # If we have reached the end of the grid, return True
    if row == M - 1 and col == M:
        return True

    # Move to the next row if we are at the end of the current row
    if col == M:
        row += 1
        col = 0

    # Skip cells that are already filled
    if grid[row][col] > 0:
        return Suduko(grid, row, col + 1)

    # Try placing numbers 1-9 in the empty cell and check for validity
    for num in range(1, M + 1, 1):
        if solve(grid, row, col, num):
            grid[row][col] = num
            if Suduko(grid, row, col + 1):
                return True
        grid[row][col] = 0  # Reset if no valid number is found

    return False

grid = [[2, 5, 0, 0, 3, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 4, 0, 0, 0],
        [4, 0, 7, 0, 0, 0, 2, 0, 8],
        [0, 0, 5, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 8, 1, 0, 0],
        [0, 4, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 3, 6, 0, 0, 7, 2],
        [0, 7, 0, 0, 0, 0, 0, 0, 3],
        [9, 0, 3, 0, 0, 0, 6, 0, 4]]

if Suduko(grid, 0, 0):
    puzzle(grid)
else:
    print("Solution does not exist :(")

