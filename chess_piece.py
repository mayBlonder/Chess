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

    def set_position(self, row, col):
        self.position = (row, col)

    def is_valid_move(self, board, from_square, to_square):
        pass

    def is_check(self, king_position, board, from_square):
        if not self.is_valid_move(board, from_square, king_position):
            return False

        x_src, y_src = from_square
        x_dst, y_dst = king_position
        piece = self.is_piece_in_the_way_straight(board, x_src, x_dst, y_src, y_dst)[1]
        if isinstance(piece, King):
            return True
        return False

    def is_piece_in_the_way_straight(self, board, x_src, x_dst, y_src, y_dst):
        if y_src == y_dst:  # Checking if there is a piece in the way.
            x_src, x_dst = self.order(x_src, x_dst)
            for col in range(x_src, x_dst):
                if not isinstance(board[col][y_src], Empty):
                    return True, board[col][y_src]
        elif x_src == x_dst:  # Checking if there is a piece in the way.
            y_src, y_dst = self.order(y_src, y_dst)
            for row in range(y_src, y_dst):
                if not isinstance(board[x_src][row], Empty):
                    return True, board[x_src][row]
        return False, Empty

    @staticmethod
    def order(first, second):
        if first < second:
            return first + 1, second
        return second + 1, first

    @staticmethod
    def is_piece_in_the_way_diagonal(x_src, x_dst, y_src, y_dst, board):
        x_direction = 1 if x_src < x_dst else -1
        y_direction = 1 if y_src < y_dst else -1

        x_src += x_direction
        y_src += y_direction
        while (x_src * x_direction <= x_dst * x_direction) and (
                y_src * y_direction <= y_dst * y_direction):
            square = board[x_src][y_src]
            if not isinstance(square, Empty):
                return True, square
            x_src += x_direction
            y_src += y_direction
        return False, Empty


class Empty(ChessPiece):
    def __init__(self):
        super().__init__(-1, -1, -1)

    def is_valid_move(self, board, from_square, to_square):
        return True


class Rook(ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.has_moved = False

    def set_has_moved(self, has_moved):
        self.has_moved = has_moved

    def is_valid_move(self, board, from_square, to_square):
        x_src, y_src = from_square
        x_dst, y_dst = to_square

        if not (x_src == x_dst or y_src == y_dst):
            return False

        if self.is_piece_in_the_way_straight(board, x_src, x_dst, y_src, y_dst)[0]:
            return False

        self.has_moved = True
        return True


class Knight(ChessPiece):
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


class Bishop(ChessPiece):
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


class Queen(ChessPiece):
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


class King(ChessPiece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.has_moved = False
        self.in_check = False

    def set_has_moved(self, has_moved):
        self.has_moved = has_moved

    def set_in_check(self, in_check):
        self.in_check = in_check

    def is_valid_move(self, board, from_square, to_square):
        x_src, y_src = from_square
        x_dst, y_dst = to_square

        if abs(x_dst - x_src) <= 1 and abs(y_dst - y_src) <= 1:
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

