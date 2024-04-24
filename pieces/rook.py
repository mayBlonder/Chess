import chess_piece
from position import Position


class Rook(chess_piece.ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.has_moved = False

    def is_valid_move(self, board, from_square, to_square):
        x_src, y_src = from_square
        x_dst, y_dst = to_square

        if not (x_src == x_dst or y_src == y_dst):
            return False

        if self.is_piece_in_the_way_straight(board, x_src, x_dst, y_src, y_dst)[0]:
            return False

        self.has_moved = True
        return True

    def get_all_moves(self, board):
        moves = self.all_moves_straight()
        src_row, src_col = self.get_position()
        return super().get_all_valid_moves(board, src_row, src_col, moves)
