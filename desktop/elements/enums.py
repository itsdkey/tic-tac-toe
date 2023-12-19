import enum


class Symbol(enum.Enum):
    PLAYER_ONE = "X"
    PLAYER_TWO = "O"

    def __str__(self) -> str:
        return self.value
