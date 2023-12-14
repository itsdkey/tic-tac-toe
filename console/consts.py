import enum


class Sign(enum.Enum):
    EMPTY = " "
    PLAYER_ONE = "X"
    PLAYER_TWO = "O"

    def __str__(self) -> str:
        return self.value
