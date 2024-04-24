import constants


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

    def get_all_moves(self, board):
        pass

    def get_all_valid_moves(self, board, src_row, src_col, moves):
        """
        :param moves: All possible moves the piece can do.
        :return: All valid moves the piece can do from square (src_row, src_col).
        """
        valid_moves = []
        for move in moves:
            row, col = src_row + move[0], src_col + move[1]
            if not (0 <= row < 8 and 0 <= col < 8):
                continue
            if self.is_valid_move(board, (src_row, src_col), (row, col)):
                valid_moves.append((row, col))
        return valid_moves

    def is_check(self, king_position, board, from_square):
        """
        :param from_square: pieces location.
        :return: True if piece is threatening the king, else False.
        """
        if not self.is_valid_move(board, from_square, king_position):
            return False

        x_src, y_src = from_square
        x_dst, y_dst = king_position
        piece = self.is_piece_in_the_way_straight(board, x_src, x_dst, y_src, y_dst)[1]
        if isinstance(piece, King):
            return True
        return False

    def is_piece_in_the_way_straight(self, board, x_src, x_dst, y_src, y_dst):
        """
        :return: True if there is a piece in the straight way
        between (x_src, y_src) and (x_dst, y_dst).
        """
        if y_src == y_dst:
            x_src, x_dst = self.order(x_src, x_dst)
            for col in range(x_src, x_dst):
                if not isinstance(board[col][y_src], Empty):
                    return True, board[col][y_src]
        elif x_src == x_dst:
            y_src, y_dst = self.order(y_src, y_dst)
            for row in range(y_src, y_dst):
                if not isinstance(board[x_src][row], Empty):
                    return True, board[x_src][row]
        return False, Empty

    @staticmethod
    def all_moves_straight():
        """
        :return: All possible moves for a piece that is going straight.
        """
        moves = []
        for adding in range(1, 8):
            moves.append((adding, 0))
            moves.append((-adding, 0))
            moves.append((0, adding))
            moves.append((0, -adding))

        return moves

    @staticmethod
    def all_moves_diagonal():
        """
        :return: All possible moves for a piece that is going diagonal.
        """
        moves = []
        for i in range(1, 8):
            moves.append((i, i))
            moves.append((i, i))
            moves.append((-i, i))
            moves.append((-i, -i))

        return moves

    @staticmethod
    def order(first, second):
        """
        Puts in first the smallest value between the two variables and ands one.
        And puts the bigger value in second.
        """
        if first < second:
            return first + 1, second
        return second + 1, first

    @staticmethod
    def is_piece_in_the_way_diagonal(x_src, x_dst, y_src, y_dst, board):
        """
        Checks diagonally if there is a chess piece between the source and
        destination board positions and returns True and the piece if there is.
        """
        x_direction = 1 if x_src < x_dst else -1
        y_direction = 1 if y_src < y_dst else -1

        x_src += x_direction
        y_src += y_direction

        while ((0 <= x_src < 8) and (0 <= y_src < 8) and
               (x_src != x_dst) and (y_src != y_dst)):
            square = board[x_src][y_src]
            if not isinstance(square, Empty):
                return True, square
            x_src += x_direction
            y_src += y_direction
        return False, Empty


class Empty(ChessPiece):
    def __init__(self, row, col):
        super().__init__(-1, row, col)

    def is_valid_move(self, board, from_square, to_square):
        return True
