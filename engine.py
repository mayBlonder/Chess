"""
Restoring all the data of a game and determining the valid moves.
"""

from numpy import array
import chess_piece

WHITE = 0
BLACK = 1

BLACK_ROOK_1 = chess_piece.Rook(BLACK, 0, 0)
BLACK_KNIGHT_1 = chess_piece.Knight(BLACK, 0, 1)
BLACK_BISHOP_1 = chess_piece.Bishop(BLACK, 0, 2)
BLACK_QUEENS = [chess_piece.Queen(BLACK, 0, 3)]
BLACK_KING = chess_piece.King(BLACK, 0, 4)
BLACK_BISHOP_2 = chess_piece.Bishop(BLACK, 0, 5)
BLACK_KNIGHT_2 = chess_piece.Knight(BLACK, 0, 6)
BLACK_ROOK_2 = chess_piece.Rook(BLACK, 0, 7)
BLACK_PAWNS = [chess_piece.Pawn(BLACK, 1, i) for i in range(8)]

WHITE_ROOK_1 = chess_piece.Rook(WHITE, 7, 0)
WHITE_KNIGHT_1 = chess_piece.Knight(WHITE, 7, 1)
WHITE_BISHOP_1 = chess_piece.Bishop(WHITE, 7, 2)
WHITE_QUEENS = [chess_piece.Queen(WHITE, 7, 3)]
WHITE_KING = chess_piece.King(WHITE, 7, 4)
WHITE_BISHOP_2 = chess_piece.Bishop(WHITE, 7, 5)
WHITE_KNIGHT_2 = chess_piece.Knight(WHITE, 7, 6)
WHITE_ROOK_2 = chess_piece.Rook(WHITE, 7, 7)
WHITE_PAWNS = [chess_piece.Pawn(WHITE, 7, i) for i in range(8)]

EMPTY_ROW_1 = [chess_piece.Empty(2, i) for i in range(8)]
EMPTY_ROW_2 = [chess_piece.Empty(3, i) for i in range(8)]
EMPTY_ROW_3 = [chess_piece.Empty(4, i) for i in range(8)]
EMPTY_ROW_4 = [chess_piece.Empty(5, i) for i in range(8)]

BLACK_ROW_1 = [BLACK_ROOK_1, BLACK_KNIGHT_1, BLACK_BISHOP_1, BLACK_QUEENS[0], BLACK_KING,
               BLACK_BISHOP_2, BLACK_KNIGHT_2, BLACK_ROOK_2]
BLACK_ROW_2 = [BLACK_PAWNS[0], BLACK_PAWNS[1], BLACK_PAWNS[2], BLACK_PAWNS[3],
               BLACK_PAWNS[4], BLACK_PAWNS[5], BLACK_PAWNS[6], BLACK_PAWNS[7]]
WHITE_ROW_1 = [WHITE_PAWNS[0], WHITE_PAWNS[1], WHITE_PAWNS[2], WHITE_PAWNS[3],
               WHITE_PAWNS[4], WHITE_PAWNS[5], WHITE_PAWNS[6], WHITE_PAWNS[7]]
WHITE_ROW_2 = [WHITE_ROOK_1, WHITE_KNIGHT_1, WHITE_BISHOP_1, WHITE_QUEENS[0], WHITE_KING,
               WHITE_BISHOP_2, WHITE_KNIGHT_2, WHITE_ROOK_2]


class GameState:
    def __init__(self):
        self.is_white_turn = True
        self.move_log = []
        self.black_pieces = BLACK_ROW_1 + BLACK_ROW_2
        self.white_pieces = WHITE_ROW_1 + WHITE_ROW_2
        self.board = array(
            [BLACK_ROW_1, BLACK_ROW_2, EMPTY_ROW_1, EMPTY_ROW_2,
             EMPTY_ROW_3, EMPTY_ROW_4, WHITE_ROW_1, WHITE_ROW_2])

    def make_move(self, move):
        piece = move.piece_moved
        piece.set_position(move.dst_row, move.dst_col)
        src_col, src_row = move.source_row, move.source_col
        self.board[src_col][src_row] = chess_piece.Empty(src_col, src_row)  # Cleans source square
        self.board[move.dst_row][move.dst_col] = piece  # Moves piece to destination square
        self.move_log.append(move)

    def undo_move(self):
        if len(self.move_log) > 0:
            move = self.move_log.pop()
            piece = move.piece_moved
            piece.set_position(move.source_row, move.source_col)
            self.board[move.source_row][move.source_col] = piece  # Returns piece
            self.board[move.dst_row][move.dst_col] = move.piece_captured
            return move

    def pre_conditions(self, is_white_turn, this_color, other_color, to_print=True):
        correct_color = self.right_color(is_white_turn, this_color)
        eat_opponent_or_empty = this_color != other_color

        if not correct_color:
            if to_print:
                print("ERROR: not your turn.")
            return False
        elif not eat_opponent_or_empty:
            if to_print:
                print("ERROR: can not eat your own piece.")
            return False
        return True

    def check(self):
        if self.is_white_turn:
            for piece in self.black_pieces:
                if piece.is_check(WHITE_KING.get_position(), self.board, piece.get_position()):
                    return True
            return False
        else:  # Black's turn
            for piece in self.white_pieces:
                if piece.is_check(BLACK_KING.get_position(), self.board, piece.get_position()):
                    return True
            return False

    def mate(self):
        king_options = ((1, 0), (1, 1), (0, 1), (-1, 0),
                        (-1, -1), (0, -1), (1, -1), (-1, 1))
        if self.is_white_turn:
            king = WHITE_KING
        else:
            king = BLACK_KING

        self.undo_move()
        # check if king can not move to any square.
        king_x, king_y = king.get_position()
        for opt in king_options:
            #  if not a valid square, skip to next option.
            if (king_x + opt[0] < 0 or king_x + opt[0] > 7) or (
                    king_y + opt[1] < 0 or king_y + opt[1] > 7):
                continue

            #  if it does not meet the preconditions, skip to next option.
            dst_square = self.board[king_x + opt[0]][king_y + opt[1]]
            if not self.pre_conditions(True, WHITE, dst_square.get_color(), False):
                continue

            move = Move(king.get_position(), (king_x + opt[0], king_y + opt[1]), self.board)
            self.make_move(move)
            #  if destination square is threatened, skip to next option.
            if self.check():
                self.undo_move()
                continue
            else:
                self.undo_move()
                return False  # not mate.
        return True

    def castle(self, king, rook):
        if king.has_moved:
            print("ERROR: can not castling, king has moved.")
            return

        if rook.has_moved:
            print("ERROR: can not castling, rook has moved.")
            return

        king_location = king.get_position()
        rook_location = rook.get_position()

        if not rook.is_valid_move(self.board, rook_location, king_location):
            print("ERROR: can not castling, not a valid rook move.")
            return

        rook_x = rook_location[1]
        first_x = rook_x
        second_x = king_location[1]
        king_y = king_location[0]

        if first_x < second_x:
            first_x, second_x = first_x + 1, second_x
        else:
            first_x, second_x = second_x + 1, first_x

        # check that all squares in between are not under attack.
        for x in range(first_x, second_x):
            move = Move(king_location, (king_y, x), self.board)
            self.make_move(move)
            if self.check():
                for x_0 in range(x):
                    self.undo_move()
                print("ERROR: can not castling, square ({},{}) is threatened.".format(king_y, x))
                return
            king_location = king.get_position()

        # if success - move rook also.
        if rook_x == 7:
            rook_target_x = 5
        else:  # rook_x == 0
            move = Move(king_location, (king_y, 2), self.board)
            self.make_move(move)
            rook_target_x = 3

        move = Move(rook_location, (king_y, rook_target_x), self.board)
        self.make_move(move)

    @staticmethod
    def add_queen(color, row, col):
        queen = chess_piece.Queen(color, row, col)
        if color == WHITE:
            WHITE_QUEENS.append(queen)
        else:
            BLACK_QUEENS.append(queen)
        return queen

    @staticmethod
    def right_color(is_white_turn, color):
        if (is_white_turn and not color == WHITE) or (
                not is_white_turn and not color == BLACK):
            return False
        return True


class Move:
    def __init__(self, src_square, dst_square, board):
        self.source_row = src_square[0]
        self.source_col = src_square[1]
        self.dst_row = dst_square[0]
        self.dst_col = dst_square[1]
        self.board = board
        self.piece_moved = board[self.source_row][self.source_col]
        self.piece_captured = board[self.dst_row][self.dst_col]
        self.move_id = self.source_row * 1000 + self.source_col * 100 + self.dst_row * 10 + self.dst_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
