"""
Restoring all the data of a game and determining the valid moves.
"""

import chess_piece
import pieces.bishop as bishop
import pieces.king as king
import pieces.knight as knight
import pieces.pawn as pawn
import pieces.queen as queen
import pieces.rook as rook

WHITE = 0
BLACK = 1

BLACK_ROOK_1 = rook.Rook(BLACK, 0, 0)
BLACK_KNIGHT_1 = knight.Knight(BLACK, 0, 1)
BLACK_BISHOP_1 = bishop.Bishop(BLACK, 0, 2)
BLACK_QUEENS = [queen.Queen(BLACK, 0, 3)]
BLACK_KING = king.King(BLACK, 0, 4)
BLACK_BISHOP_2 = bishop.Bishop(BLACK, 0, 5)
BLACK_KNIGHT_2 = knight.Knight(BLACK, 0, 6)
BLACK_ROOK_2 = rook.Rook(BLACK, 0, 7)
BLACK_PAWNS = [pawn.Pawn(BLACK, 1, i) for i in range(8)]

WHITE_ROOK_1 = rook.Rook(WHITE, 7, 0)
WHITE_KNIGHT_1 = knight.Knight(WHITE, 7, 1)
WHITE_BISHOP_1 = bishop.Bishop(WHITE, 7, 2)
WHITE_QUEENS = [queen.Queen(WHITE, 7, 3)]
WHITE_KING = king.King(WHITE, 7, 4)
WHITE_BISHOP_2 = bishop.Bishop(WHITE, 7, 5)
WHITE_KNIGHT_2 = knight.Knight(WHITE, 7, 6)
WHITE_ROOK_2 = rook.Rook(WHITE, 7, 7)
WHITE_PAWNS = [pawn.Pawn(WHITE, 6, i) for i in range(8)]

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
        self.board = [BLACK_ROW_1, BLACK_ROW_2, EMPTY_ROW_1, EMPTY_ROW_2,
                      EMPTY_ROW_3, EMPTY_ROW_4, WHITE_ROW_1, WHITE_ROW_2]

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

    def pre_conditions(self, this_color, other_color, to_print=True):
        """
        Checks if the piece chosen is the right color- if it's turn,
        also checks that a player is not trying to eat his own piece.
        :return: True if meets the conditions.
        """
        correct_color = self.right_color(self.is_white_turn, this_color)
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
        """
        :return: True if there is a piece that checks the king, else, False
        """
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
        """
        :return: True if king is in mate, else: False.
        """
        if self.is_white_turn:
            pieces = self.white_pieces
            color = WHITE
        else:
            pieces = self.black_pieces
            color = BLACK
        self.undo_move()

        for piece in pieces:
            for move in piece.get_all_moves(self.board):
                dst_row, dst_col = move
                dst_square = self.board[dst_row][dst_col]
                if not self.pre_conditions(color, dst_square.get_color(), to_print=False):
                    continue

                move = Move(piece.get_position(), (dst_row, dst_col), self.board)
                self.make_move(move)
                if self.check():
                    self.undo_move()
                    continue
                else:
                    self.undo_move()
                    return False  # not mate
        return True

    def castle(self, king, rook):
        """
        Makes the castling move if it's legal.
        :return: void
        """
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

        # If success - move rook also.
        if rook_x == 7:
            rook_target_x = 5
        else:  # If rook_x == 0
            move = Move(king_location, (king_y, 2), self.board)
            self.make_move(move)
            rook_target_x = 3

        move = Move(rook_location, (king_y, rook_target_x), self.board)
        self.make_move(move)

    @staticmethod
    def add_queen(color, row, col):
        """
        Creates a new queen in case there is a pawn promotion.
        :return: A new queen.
        """
        queen = chess_piece.Queen(color, row, col)
        if color == WHITE:
            WHITE_QUEENS.append(queen)
        else:
            BLACK_QUEENS.append(queen)
        return queen

    @staticmethod
    def right_color(is_white_turn, color):
        """
        :return: True if the color of the piece and who turn it is are corresponding.
        """
        if (is_white_turn and not color == WHITE) or (
                not is_white_turn and not color == BLACK):
            return False
        return True


class Move:
    def __init__(self, src_square, dst_square, board):
        self.source_row,  self.source_col = src_square
        self.dst_row, self.dst_col = dst_square
        self.board = board
        self.piece_moved = board[self.source_row][self.source_col]
        self.piece_captured = board[self.dst_row][self.dst_col]
