import chess_piece
from position import Position



class King(chess_piece.ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.has_moved = False
        self.in_check = False

    def set_in_check(self, in_check):
        self.in_check = in_check

    def is_valid_move(self, board, from_square, to_square):
        x_src, y_src = from_square
        x_dst, y_dst = to_square

        if abs(x_dst - x_src) <= 1 and abs(y_dst - y_src) <= 1:
            self.has_moved = True
            return True
        return False

    def get_all_moves(self, board):
        src_row, src_col = self.get_position()
        moves = ((1, 0), (1, 1), (0, 1), (-1, 0),
                 (-1, -1), (0, -1), (1, -1), (-1, 1))
        return super().get_all_valid_moves(board, src_row, src_col, moves)
