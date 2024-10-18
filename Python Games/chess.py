class ChessPiece:
    def __init__(self, color, name):
        self.color = color
        self.name = name

    def __str__(self):
        return self.name[0].upper() if self.color == 'white' else self.name[0].lower()


class ChessBoard:
    def __init__(self):
        self.board = self.create_board()
        self.current_turn = 'white'
        print("Whites are Capitals")

    def create_board(self):
        board = [[None] * 8 for _ in range(8)]
        for i in range(8):
            board[1][i] = ChessPiece('white', 'pawn')
            board[6][i] = ChessPiece('black', 'pawn')

        board[0][0] = board[0][7] = ChessPiece('white', 'rook')
        board[0][1] = board[0][6] = ChessPiece('white', 'knight')
        board[0][2] = board[0][5] = ChessPiece('white', 'bishop')
        board[0][3] = ChessPiece('white', 'queen')
        board[0][4] = ChessPiece('white', 'king')

        board[7][0] = board[7][7] = ChessPiece('black', 'rook')
        board[7][1] = board[7][6] = ChessPiece('black', 'knight')
        board[7][2] = board[7][5] = ChessPiece('black', 'bishop')
        board[7][3] = ChessPiece('black', 'queen')
        board[7][4] = ChessPiece('black', 'king')

        return board

    def display_board(self):
        print("  a b c d e f g h")
        for row in range(8):
            print(8 - row, end=' ')
            for col in range(8):
                piece = self.board[row][col]
                print(piece if piece else '.', end=' ')
            print(8 - row)
        print("  a b c d e f g h")

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]

        if piece is None or piece.color != self.current_turn:
            return False
        
        # Basic validation: cannot move to a square occupied by your own piece
        if self.board[end_row][end_col] and self.board[end_row][end_col].color == self.current_turn:
            return False

        # Implement piece-specific movement rules
        return self.validate_piece_move(piece, start, end)

    def validate_piece_move(self, piece, start, end):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if piece.name == 'pawn':
            direction = 1 if piece.color == 'white' else -1
            start_row_check = 1 if piece.color == 'white' else 6
            if col_diff == 0:  # Moving forward
                if row_diff == direction and not self.board[end_row][end_col]:
                    return True
                if row_diff == 2 * direction and start_row == start_row_check and not self.board[end_row][end_col] and not self.board[start_row + direction][start_col]:
                    return True
            elif abs(col_diff) == 1 and row_diff == direction:  # Capturing
                if self.board[end_row][end_col] and self.board[end_row][end_col].color != piece.color:
                    return True
            return False

        elif piece.name == 'rook':
            if col_diff == 0 or row_diff == 0:  # Move in straight line
                return self.is_path_clear(start, end)

        elif piece.name == 'knight':
            if (abs(row_diff), abs(col_diff)) in [(2, 1), (1, 2)]:  # L-shape movement
                return True

        elif piece.name == 'bishop':
            if abs(row_diff) == abs(col_diff):  # Move diagonally
                return self.is_path_clear(start, end)

        elif piece.name == 'queen':
            if abs(row_diff) == abs(col_diff) or col_diff == 0 or row_diff == 0:  # Move like rook or bishop
                return self.is_path_clear(start, end)

        elif piece.name == 'king':
            if max(abs(row_diff), abs(col_diff)) == 1:  # Move one square in any direction
                return True

        return False

    def is_path_clear(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        row_step = (end_row - start_row) // max(1, abs(end_row - start_row)) if end_row != start_row else 0
        col_step = (end_col - start_col) // max(1, abs(end_col - start_col)) if end_col != start_col else 0
        current_row, current_col = start_row + row_step, start_col + col_step

        while (current_row, current_col) != (end_row, end_col):
            if self.board[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step

        return True

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def play(self):
        while True:
            self.display_board()
            move = input(f"{self.current_turn.capitalize()}'s turn. Enter move (e.g., e2 e4): ")
            start, end = move.split()
            start_row = 8 - int(start[1])
            start_col = ord(start[0]) - ord('a')
            end_row = 8 - int(end[1])
            end_col = ord(end[0]) - ord('a')

            if self.is_valid_move((start_row, start_col), (end_row, end_col)):
                self.move_piece((start_row, start_col), (end_row, end_col))
            else:
                print("Invalid move. Try again.")


if __name__ == "__main__":
    game = ChessBoard()
    game.play()
