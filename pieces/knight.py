import chess_piece
from position import Position


class Knight(chess_piece.ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def is_valid_move(self, board, from_square, to_square):
        x_src, y_src = from_square
        x_dst, y_dst = to_square

        if (abs(x_dst - x_src) == 1 and abs(y_dst - y_src) == 2) or (
                abs(x_dst - x_src) == 2 and abs(y_dst - y_src) == 1):
            return True
        return False

    def is_check(self, king_position, board, from_square):
        return self.is_valid_move(board, from_square, king_position)

    def get_all_moves(self, board):
        src_row, src_col = self.get_position()
        moves = [(1, 2), (-1, -2), (-1, 2),
                 (1, -2), (2, 1), (-2, -1),
                 (-2, 1), (2, -1)]

        return super().get_all_valid_moves(board, src_row, src_col, moves)