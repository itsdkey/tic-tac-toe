from board import Board
from validators import validate_coords, validate_size


def get_board_size() -> int:
    while True:
        size = input("What will be the board size? ")
        try:
            size = validate_size(size)
        except ValueError as ex:
            print(str(ex))
        else:
            break
    return size


def get_coordinates(size: int) -> tuple:
    while True:
        coords = input("Provide X and Y where you want to place your sign: ").split()
        try:
            coords = validate_coords(coords, size)
        except ValueError as ex:
            print(str(ex))
        else:
            break
    return coords


def main() -> None:
    print("Welcome to Tic-Tac-Toe Game! If you want to exit feel free to hit CTRL+C.")
    size = get_board_size()
    board = Board(size)
    while True:
        board.show_board()
        coords = get_coordinates(board.size)
        try:
            board.place_sign(*coords)
        except ValueError as ex:
            print(str(ex))
        else:
            if board.check_winner():
                board.show_board()
                print("You won!")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
