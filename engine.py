"""
Restoring all the data of a game and determining the valid moves.
"""

from numpy import array
import chess_piece

WHITE = 0
BLACK = 1

EMPTY = chess_piece.Empty()

BLACK_ROOK_1 = chess_piece.Rook(BLACK, 0, 0)
BLACK_KNIGHT_1 = chess_piece.Knight(BLACK, 0, 1)
BLACK_BISHOP_1 = chess_piece.Bishop(BLACK, 0, 2)
BLACK_QUEEN = chess_piece.Queen(BLACK, 0, 3)
BLACK_KING = chess_piece.King(BLACK, 0, 4)
BLACK_BISHOP_2 = chess_piece.Bishop(BLACK, 0, 5)
BLACK_KNIGHT_2 = chess_piece.Knight(BLACK, 0, 6)
BLACK_ROOK_2 = chess_piece.Rook(BLACK, 0, 7)
BLACK_PAWNS = [chess_piece.Pawn(BLACK, 1, i) for i in range(8)]

WHITE_ROOK_1 = chess_piece.Rook(WHITE, 7, 0)
WHITE_KNIGHT_1 = chess_piece.Knight(WHITE, 7, 1)
WHITE_BISHOP_1 = chess_piece.Bishop(WHITE, 7, 2)
WHITE_QUEEN = chess_piece.Queen(WHITE, 7, 3)
WHITE_KING = chess_piece.King(WHITE, 7, 4)
WHITE_BISHOP_2 = chess_piece.Bishop(WHITE, 7, 5)
WHITE_KNIGHT_2 = chess_piece.Knight(WHITE, 7, 6)
WHITE_ROOK_2 = chess_piece.Rook(WHITE, 7, 7)
WHITE_PAWNS = [chess_piece.Pawn(WHITE, 7, i) for i in range(8)]
EMPTY_ROW = [EMPTY] * 8

BLACK_ROW_1 = [BLACK_ROOK_1, BLACK_KNIGHT_1, BLACK_BISHOP_1, BLACK_QUEEN, BLACK_KING,
               BLACK_BISHOP_2, BLACK_KNIGHT_2, BLACK_ROOK_2]
BLACK_ROW_2 = [BLACK_PAWNS[0], BLACK_PAWNS[1], BLACK_PAWNS[2], BLACK_PAWNS[3],
               BLACK_PAWNS[4], BLACK_PAWNS[5], BLACK_PAWNS[6], BLACK_PAWNS[7]]
WHITE_ROW_1 = [WHITE_PAWNS[0], WHITE_PAWNS[1], WHITE_PAWNS[2], WHITE_PAWNS[3],
               WHITE_PAWNS[4], WHITE_PAWNS[5], WHITE_PAWNS[6], WHITE_PAWNS[7]]
WHITE_ROW_2 = [WHITE_ROOK_1, WHITE_KNIGHT_1, WHITE_BISHOP_1, WHITE_QUEEN, WHITE_KING,
               WHITE_BISHOP_2, WHITE_KNIGHT_2, WHITE_ROOK_2]


class GameState:
    def __init__(self):
        self.is_white_turn = True
        self.move_log = []
        self.black_king_location = (0, 4)
        self.white_king_location = (7, 4)

        self.black_pieces = BLACK_ROW_1 + BLACK_ROW_2
        self.white_pieces = WHITE_ROW_1 + WHITE_ROW_2
        self.board = array(
            [BLACK_ROW_1, BLACK_ROW_2, EMPTY_ROW, EMPTY_ROW,
             EMPTY_ROW, EMPTY_ROW, WHITE_ROW_1, WHITE_ROW_2])

    """
    Not working for castling, pawn promotion and en-passant.
    """

    def make_move(self, move):
        piece = move.piece_moved
        piece.set_position(move.dst_row, move.dst_col)
        self.board[move.source_row][move.source_col] = chess_piece.Empty()  # Cleans source square
        self.board[move.dst_row][move.dst_col] = piece  # Moves piece to destination square
        self.move_log.append(move)
        # self.is_white_turn = not self.is_white_turn  # Switch turns (can be done with XOR 1)

        if isinstance(piece, chess_piece.King):  # Update king location if needed
            if piece.get_color() == WHITE:
                self.white_king_location = (move.dst_row, move.dst_col)
            else:
                self.black_king_location = (move.dst_row, move.dst_col)

    def undo_move(self):
        if len(self.move_log) > 0:
            move = self.move_log.pop()
            piece = move.piece_moved
            piece.set_position(move.source_row, move.source_col)
            self.board[move.source_row][move.source_col] = piece  # Returns piece
            self.board[move.dst_row][move.dst_col] = move.piece_captured
            self.is_white_turn = not self.is_white_turn  # Switch turns (can be done with XOR 1)

            if isinstance(piece, chess_piece.King):  # Update king location if needed
                if piece.get_color() == WHITE:
                    self.white_king_location = (move.source_row, move.source_col)
                else:
                    self.black_king_location = (move.source_row, move.source_col)

    # All moves
    # def get_valid_moves(self):
    #     return self.get_all_possible_moves()

    # Without check
    # def get_all_possible_moves(self):
    #     moves = []
    #     for row in range(len(self.board)):
    #         for col in range(len(self.board[0])):
    #             piece = self.board[row][col]
    #             if isinstance(piece, chess_piece.ChessPiece):
    #                 if (piece.get_color() == WHITE and self.is_white_turn) or (
    #                         piece.get_color() == BLACK and not self.is_white_turn):
    #                     if piece.__class__ == "Pawn":
    #                         self.get_pawn_moves(row, col, moves)
    #     return moves

    def check(self):
        if self.is_white_turn:
            for piece in self.black_pieces:
                if piece.is_check(self.white_king_location, self.board, piece.get_position()):
                    print("Not moving because of:")
                    print(piece.__class__.__name__)
                    print("white" if piece.get_color() == 0 else "black")
                    print(self.white_king_location)
                    return True
            return False
        else:  # Black's turn
            for piece in self.white_pieces:
                if piece.is_check(self.black_king_location, self.board, piece.get_position()):
                    print("Not moving because of:")
                    print(piece.__class__.__name__)
                    print(piece.get_color())
                    print("white" if piece.get_color() == 0 else "black")
                    print(self.black_king_location)
                    return True
            return False


class Move:
    # Todo: remove if possible
    # ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    # rows_to_ranks = {val: key for key, val in ranks_to_rows.items()}
    # files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    # cols_to_files = {val: key for key, val in files_to_cols.items()}

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

    # Todo: remove if possible
    # def get_chess_notation(self):
    #     return self.get_rank_file(self.source_row, self.source_col) + self.get_rank_file(self.dst_row, self.dst_col)

    # Todo: remove if possible
    # def get_rank_file(self, row, col):
    #     return self.cols_to_files[col] + self.rows_to_ranks[row]
