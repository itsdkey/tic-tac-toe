class Board:

    def __init__(self, size: int = 3) -> None:
        self.size = size
        self.board = [[" " for x in range(self.size)] for y in range(self.size)]
        self.next_sign = "X"

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
            self.next_sign = 'O' if self.next_sign == 'X' else 'X'
        else:
            raise ValueError("This place is already taken.")

    def check_winner(self) -> bool:
        for x in range(self.size):
            sums = [
                sum(self.board[x][y] == 'O' for y in range(self.size)),
                sum(self.board[x][y] == 'X' for y in range(self.size)),
                sum(self.board[y][x] == 'O' for y in range(self.size)),
                sum(self.board[y][x] == 'X' for y in range(self.size)),
                sum(self.board[x][x] == 'O' for x in range(self.size)),
                sum(self.board[x][x] == 'X' for x in range(self.size)),
                sum(self.board[x][self.size - x - 1] == 'O' for x in range(self.size)),
                sum(self.board[x][self.size - x - 1] == 'X' for x in range(self.size)),
            ]
            if any(_sum == self.size for _sum in sums):
                return True
        return False
