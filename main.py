import sys
from logging import getLogger
from logging.config import dictConfig

import pygame

from desktop.config import LOGGING
from desktop.consts import CHANGE_TO_GAME_STATE, CHANGE_TO_POST_GAME_STATE
from desktop.elements.game import Game

logger = getLogger(__name__)


def main() -> None:
    logger.debug(
        "Welcome to Tic-Tac-Toe Game! If you want to exit feel free to hit CTRL+C."
    )
    dictConfig(LOGGING)

    pygame.init()
    game = Game()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.debug("exit using quit")
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                logger.debug("exit using escape")
                pygame.quit()
                sys.exit(0)
            if event.type in [CHANGE_TO_GAME_STATE, CHANGE_TO_POST_GAME_STATE]:
                logger.debug(f"update game state: {event.dict['state']}")
                game.update_state(state=event.dict["state"])

        game.update()
        game.post_actions()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
