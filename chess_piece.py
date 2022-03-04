WHITE = 0
BLACK = 1


class ChessPiece:
    def __init__(self, color, row, col):
        self.color = color
        self.position = (row, col)

    def get_color(self):
        return self.color

    def get_position(self):
        return self.position

    def is_valid_move(self, board, from_square, to_square):
        pass

    @staticmethod
    def is_piece_in_the_way_straight(diff, board, x_src, x_dst, y_src, y_dst):
        x_diff = diff[1]
        y_diff = diff[0]
        if abs(x_diff == 0):  # Checking if there is a piece in the way.
            if x_src < x_dst:
                x_src, x_dst = x_src+1, x_dst
            else:
                x_src, x_dst = x_dst+1, x_src
            # from_ind, to_ind = self.order(x_src, x_dst)
            for col in range(x_src, x_dst-1):
                print(col)
                if not isinstance(board[col][y_src], Empty):
                    return True, board[col][y_src]
            print("###")
        elif abs(y_diff == 0):  # Checking if there is a piece in the way.
            # row_from, row_to = self.order(y_src, y_dst)
            if y_src < y_dst:
                y_src, y_dst = y_src+1, y_dst
            else:
                x_src, x_dst = x_dst+1, x_src
            for row in range(y_src, y_dst):
                if not isinstance(board[x_src][row], Empty):
                    return True, board[x_src][row]
        return False, Empty

    def is_check(self, king_position, board, from_square):
        if not self.is_valid_move(board, from_square, king_position):
            return False

        src = Position(from_square[0], from_square[1])
        dst = Position(king_position[0], king_position[1])
        x_src, y_src = src.get_x(), src.get_y()
        x_dst, y_dst = dst.get_x(), dst.get_y()
        diff = src - dst
        piece = self.is_piece_in_the_way_straight(diff, board, x_src, x_dst, y_src, y_dst)[1]
        if isinstance(piece, King):
            return True
        return False

    @staticmethod
    def order(src, dst):
        if src > dst:
            return dst, src
        return src, dst

    @staticmethod
    def is_piece_in_the_way_diag(row_from, row_to, col_from, col_to, board):
        for row, col in zip(range(row_from + 1, row_to),
                            range(col_from + 1, col_to)):  # Can't skip pieces
            if not isinstance(board[row][col], Empty):
                return True, board[row][col]
        return False, Empty


class Empty(ChessPiece):
    def __init__(self):
        super().__init__(-1, -1, -1)

    def is_valid_move(self, board, from_square, to_square):
        return True


class Rook(ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def is_valid_move(self, board, from_square, to_square):
        src = Position(from_square[0], from_square[1])
        dst = Position(to_square[0], to_square[1])
        x_src, y_src = src.get_x(), src.get_y()
        x_dst, y_dst = dst.get_x(), dst.get_y()
        diff = src - dst
        if self.is_piece_in_the_way_straight(diff, board, x_src, x_dst, y_src, y_dst)[0]:
            return False

        return (abs(diff[0]) > 0 and abs(diff[1]) == 0) or (
                abs(diff[0]) == 0 and abs(diff[1]) > 0)


class Knight(ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def is_valid_move(self, board, from_square, to_square):
        src = Position(from_square[0], from_square[1])
        dst = Position(to_square[0], to_square[1])
        diff = src - dst
        return (abs(diff[0]) == 2 and abs(diff[1]) == 1) or (
                abs(diff[0]) == 1 and abs(diff[1]) == 2)

    def is_check(self, king_position, board, from_square):
        return self.is_valid_move(board, from_square, king_position)


class Bishop(ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def is_valid_move(self, board, from_square, to_square):
        src = Position(from_square[0], from_square[1])
        dst = Position(to_square[0], to_square[1])
        x_src, y_src = src.get_x(), src.get_y()
        x_dst, y_dst = dst.get_x(), dst.get_y()
        diff = src - dst
        row_from, row_to = self.order(x_src, x_dst)
        col_from, col_to = self.order(y_src, y_dst)

        if self.is_piece_in_the_way_diag(row_from, row_to, col_from, col_to, board)[0]:
            return False

        return abs(diff[0]) == abs(diff[1])


class Queen(ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def is_valid_move(self, board, from_square, to_square):
        src = Position(from_square[0], from_square[1])
        dst = Position(to_square[0], to_square[1])
        x_src, y_src = src.get_x(), src.get_y()
        x_dst, y_dst = dst.get_x(), dst.get_y()
        col_from, row_from = from_square
        col_to, row_to = to_square
        diff = src - dst
        if self.is_piece_in_the_way_straight(diff, board, x_src, x_dst, y_src, y_dst)[0]:
            return False

        if self.is_piece_in_the_way_diag(row_from, row_to, col_from, col_to, board)[0]:
            return False
        return True


class King(ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.has_moved = False

    def is_valid_move(self, board, from_square, to_square):
        src = Position(from_square[0], from_square[1])
        dst = Position(to_square[0], to_square[1])
        options = ((1, 0), (0, 1), (0, -1), (-1, 0),
                   (-1, -1), (-1, 1), (1, -1), (1, 1))

        if src - dst in options:
            self.has_moved = True
            return True
        return False


class Pawn(ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.has_moved = False

    def is_valid_move(self, board, from_square, to_square):
        src = Position(from_square[0], from_square[1])
        dst = Position(to_square[0], to_square[1])
        eat_white = ((1, 1), (1, -1))
        eat_black = ((-1, 1), (-1, -1))
        to_piece = board[to_square[0]][to_square[1]]

        if (src - dst == (1, 0) and self.get_color() == WHITE) or (
                dst - src == (1, 0) and self.get_color() == BLACK):  # One step up
            if isinstance(to_piece, Empty):  # No piece in dst square
                self.has_moved = True
                return True

        elif (src - dst == (2, 0) and self.get_color() == WHITE) or (
                dst - src == (2, 0) and self.get_color() == BLACK
        ):
            if not self.has_moved:  # If pawn hasn't moved, can be moved two squares up.
                if isinstance(to_piece, Empty):
                    if self.get_color() == WHITE:
                        in_path = board[to_square[0] + 1][to_square[1]]
                    else:
                        in_path = board[to_square[0] - 1][to_square[1]]
                    if isinstance(in_path, Empty):
                        self.has_moved = True
                        return True

        elif (src - dst in eat_white and self.get_color() == WHITE) or (
                src - dst in eat_black and self.get_color() == BLACK):  # Eat diagonal
            if not isinstance(to_piece, Empty):  # There is a piece to eat
                self.has_moved = True
                return True
        return False


class Position:
    def __init__(self, col, row):
        self.row = row
        self.col = col

    def __sub__(self, other):
        row = self.row - other.row
        col = self.col - other.col
        return col, row

    def get_x(self):
        return self.col

    def get_y(self):
        return self.row
