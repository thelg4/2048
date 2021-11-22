class Grid:
    # todo: generate random start state
    def __init__(self, n):
        # initialize empty nxn grid
        self.size = n
        self.val = []
        for i in range(n):
            self.val.append([])
            for _ in range(n):
                self.val[i].append('0')

    def get(self, x, y):
        return self.val[y][x]

    def set(self, x, y, elem):
        self.val[y][x] = elem

    def contains(self, elem):
        for row in self.val:
            for col in row:
                if col == elem:
                    return True
        return False

    def get_legal_actions(self):
        pass

    # determine whether given column is movable (has legal move)
    def col_immovable(self, x):
        for y in range(self.size):
            if self.val[y][x] == '0':
                # empty square found, column is movable
                return False
            if self.val[y][x] == self.get_above_square_val(x, y) or self.val[y][x] == self.get_below_square_val(x, y):
                # equal adjacent squares found, column is movable
                return False
        # no empty squares or equal adjacent square, column is immovable
        return True

    # determine whether given row is movable (has legal move)
    def row_immovable(self, y):
        for x in range(self.size):
            if self.val[y][x] == '0':
                # empty square found, row is movable
                return False
            if self.val[y][x] == self.get_left_square_val(x, y) or self.val[y][x] == self.get_right_square_val(x, y):
                # equal adjacent squares found, row is movable
                return False
        # no empty squares or equal adjacent square, row is immovable
        return True

    # get value of first non-empty square above given position
    def get_above_square_val(self, x, y):
        above = 0
        offset = 0
        while above == 0:
            above = self.val[y - offset][x] if y - offset >= 0 else -1
            offset += 1
        return above

    # get value of first non-empty square below given position
    def get_below_square_val(self, x, y):
        below = 0
        offset = 0
        while below == 0:
            below = self.val[y + offset][x] if y + offset < self.size else -1
            offset += 1
        return below

    # get value of first non-empty square to the left of given position
    def get_left_square_val(self, x, y):
        left = 0
        offset = 0
        while left == 0:
            left = self.val[y][x - offset] if x - offset >= 0 else -1
            offset += 1
        return left

    # get value of first non-empty square to the left of given position
    def get_right_square_val(self, x, y):
        right = 0
        offset = 0
        while right == 0:
            right = self.val[y][x + offset] if x + offset < self.size else -1
            offset += 1
        return right
