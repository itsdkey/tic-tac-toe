import enum

from pygame import USEREVENT


class GameState(enum.Enum):
    PRE_GAME = 1
    GAME = 2
    POST_GAME = 3


CHANGE_TO_GAME_STATE = USEREVENT + 1
CHANGE_TO_POST_GAME_STATE = USEREVENT + 2
