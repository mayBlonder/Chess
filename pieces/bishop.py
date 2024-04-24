import chess_piece
from position import Position


class Bishop(chess_piece.ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def is_valid_move(self, board, from_square, to_square):
        x_src, y_src = from_square
        x_dst, y_dst = to_square

        if not abs(x_dst - x_src) == abs(y_dst - y_src):  # If not moving diagonal.
            return False

        if self.is_piece_in_the_way_diagonal(x_src, x_dst, y_src, y_dst, board)[0]:
            return False

        return True

    def is_check(self, king_position, board, from_square):
        x_src, y_src = from_square
        x_dst, y_dst = king_position
        if abs(x_dst - x_src) == abs(y_dst - y_src):
            if not self.is_piece_in_the_way_diagonal(x_src, x_dst, y_src, y_dst, board)[0]:
                return True
        return False

    def get_all_moves(self, board):
        src_row, src_col = self.get_position()
        moves = self.all_moves_diagonal()
        return super().get_all_valid_moves(board, src_row, src_col, moves)
