from logging import getLogger

from desktop.elements.enums import Symbol

logger = getLogger(__name__)


class Board:
    def __init__(self, size: int = 3) -> None:
        self.size = size
        self.board = [[None for x in range(self.size)] for y in range(self.size)]
        self.next_player = Symbol.PLAYER_ONE
        self.last_coords = tuple()

    def clear(self) -> None:
        self.board = [[None for x in range(self.size)] for y in range(self.size)]

    def show_board(self) -> None:
        logger.debug("show board:")
        prefix = "    "
        for index, row in enumerate(self.board):
            row = " " + " | ".join(sign or " " for sign in row) + " "
            divider = ("-" if x % 4 != 0 else "+" for x in range(1, len(row) + 1))
            logger.debug(f"{prefix}{row}")
            if index < len(self.board) - 1:
                logger.debug(f"{prefix}{''.join(divider)}")

    def place_sign(self, x: int, y: int) -> None:
        if self.board[x][y] is None:
            self.board[x][y] = str(self.next_player)
            self.last_coords = (x, y)
            self.next_player = (
                Symbol.PLAYER_ONE
                if self.next_player == Symbol.PLAYER_TWO
                else Symbol.PLAYER_TWO
            )
            self.show_board()
        else:
            raise ValueError("This place is already taken.")

    def check_winner(self) -> bool:
        if not self.last_coords:
            return False

        x, y = self.last_coords
        sum_row = sum_col = 0
        for num in range(self.size):
            cell_row = self.board[x][num]
            cell_col = self.board[num][y]
            sum_row = self._check_cell(cell_row, sum_row)
            sum_col = self._check_cell(cell_col, sum_col)
        if any(abs(val) == self.size for val in [sum_row, sum_col]):
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
        if cell == str(Symbol.PLAYER_ONE):
            _sum -= 1
        elif cell == str(Symbol.PLAYER_TWO):
            _sum += 1
        return _sum
