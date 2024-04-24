import constants
import chess_piece
from position import Position

class Pawn(chess_piece.ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.has_moved = False
        if color == constants.WHITE:
            self.eat = ((1, 1), (1, -1))
            self.moves = ((-1, 0), (-2, 0))
        else:
            self.eat = ((-1, 1), (-1, -1))
            self.moves = ((1, 0), (2, 0))

    def is_valid_move(self, board, from_square, to_square):
        src = Position(from_square[0], from_square[1])
        dst = Position(to_square[0], to_square[1])
        to_piece = board[to_square[0]][to_square[1]]

        # One step
        if (src - dst == (1, 0) and self.get_color() == constants.WHITE) or (
                dst - src == (1, 0) and self.get_color() == constants.BLACK):
            # No piece in destination square
            if isinstance(to_piece, chess_piece.Empty):
                self.has_moved = True
                return True

        # Two steps
        elif (src - dst == (2, 0) and self.get_color() == constants.WHITE) or (
                dst - src == (2, 0) and self.get_color() == constants.BLACK
        ):
            # If pawn hasn't moved, can be moved two squares up.
            if not self.has_moved:
                if isinstance(to_piece, chess_piece.Empty):
                    if self.get_color() == constants.WHITE:
                        in_path = board[to_square[0] + 1][to_square[1]]
                    else:
                        in_path = board[to_square[0] - 1][to_square[1]]
                    if isinstance(in_path, chess_piece.Empty):
                        self.has_moved = True
                        return True
        # Eat
        elif src - dst in self.eat:
            # There is a piece to eat
            if not isinstance(to_piece, chess_piece.Empty):
                self.has_moved = True
                return True
        return False

    def get_all_moves(self, board):
        src_row, src_col = self.get_position()
        moves = self.moves + self.eat
        return super().get_all_valid_moves(board, src_row, src_col, moves)

