class Position:
    def __init__(self, col, row):
        self.row = row
        self.col = col

    def __sub__(self, other):
        row = self.row - other.row
        col = self.col - other.col
        return col, row