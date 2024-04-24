import chess_piece
from position import Position


class Queen(chess_piece.ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def is_valid_move(self, board, from_square, to_square):
        x_src, y_src = from_square
        x_dst, y_dst = to_square

        if x_src == x_dst or y_src == y_dst:  # Moving straight - up/ down/ left/ right
            if self.is_piece_in_the_way_straight(board, x_src, x_dst, y_src, y_dst)[0]:
                return False
            return True
        elif abs(x_dst - x_src) == abs(y_dst - y_src):  # Moving diagonal
            if self.is_piece_in_the_way_diagonal(x_src, x_dst, y_src, y_dst, board)[0]:
                return False
            return True
        return False

    def is_check(self, king_position, board, from_square):
        x_src, y_src = from_square
        x_dst, y_dst = king_position
        if abs(x_dst - x_src) == abs(y_dst - y_src):  # Diagonal
            if not self.is_piece_in_the_way_diagonal(x_src, x_dst, y_src, y_dst, board)[0]:
                return True
        elif x_src == x_dst or y_src == y_dst:  # Straight
            if not self.is_piece_in_the_way_straight(board, x_src, x_dst, y_src, y_dst)[0]:
                return True
        return False

    def get_all_moves(self, board):
        src_row, src_col = self.get_position()
        moves = self.all_moves_diagonal() + self.all_moves_straight()
        return super().get_all_valid_moves(board, src_row, src_col, moves)
