class Board:

    def __init__(self, size: int = 3) -> None:
        self.size = size
        self.board = [[" " for x in range(self.size)] for y in range(self.size)]
        self.next_sign = "X"
        self.last_coords = tuple()

    def show_board(self) -> None:
        print()
        prefix = "    "
        for index, row in enumerate(self.board):
            row = " " + " | ".join(row) + " "
            divider = ("-" if x % 4 != 0 else "+" for x in range(1, len(row) + 1))
            print(f"{prefix}{row}")
            if index < len(self.board) - 1:
                print(f"{prefix}{''.join(divider)}")
        print()

    def place_sign(self, x: int, y: int) -> None:
        if self.board[x][y] == ' ':
            self.board[x][y] = self.next_sign
            self.last_coords = (x, y)
            self.next_sign = 'O' if self.next_sign == 'X' else 'X'
        else:
            raise ValueError("This place is already taken.")

    def check_winner(self) -> bool:
        x, y = self.last_coords
        sum_row = 0
        for x in range(x):
            cell = self.board[x][y]
            sum_row = self._check_cell(cell, sum_row)
        if abs(sum_row) == self.size:
            return True

        sum_col = 0
        for y in range(y):
            cell = self.board[x][y]
            sum_col = self._check_cell(cell, sum_row)
        if abs(sum_col) == self.size:
            return True

        sum_diagonal_one = 0
        sum_diagonal_two = 0
        for x in range(self.size):
            cell1 = self.board[x][x]
            cell2 = self.board[x][self.size - x - 1]
            sum_diagonal_one = self._check_cell(cell1, sum_diagonal_one)
            sum_diagonal_two = self._check_cell(cell2, sum_diagonal_two)
        if any(abs(val) == self.size for val in [sum_diagonal_one, sum_diagonal_two]):
            return True
        
        return False

    @staticmethod
    def _check_cell(cell: str, _sum: int) -> int:
        if cell == '0':
            _sum += 1
        elif cell == 'X':
            _sum -= 1
        return _sum