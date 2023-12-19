from logging import getLogger

import pygame
from pygame.event import Event, post
from pygame.rect import Rect

from desktop.config import STATICS_DIR
from desktop.consts import CHANGE_TO_GAME_STATE, CHANGE_TO_POST_GAME_STATE, GameState
from desktop.elements.board import Board
from desktop.elements.enums import Symbol
from desktop.elements.sprites import Marker

logger = getLogger(__name__)


class Game:
    def __init__(self) -> None:
        self.sign_size = 158
        grid_size = self.sign_size * 3
        self.width, self.height = size = (grid_size, grid_size + 100)
        pygame.display.set_caption("Tic-tac-toe")
        self.screen = pygame.display.set_mode(size)
        self.state = GameState.PRE_GAME
        self.font = pygame.font.Font(f"{STATICS_DIR}/fonts/Pixeltype.ttf", 50)
        self.score = {Symbol.PLAYER_ONE: 0, Symbol.PLAYER_TWO: 0}
        self.player_who_won = None
        self.cooldown = 0
        self.board = Board()
        self.x_signs = pygame.sprite.Group()
        self.o_signs = pygame.sprite.Group()

    def update_state(self, state: GameState) -> None:
        self.state = state
        self.cooldown = 60

    def post_actions(self) -> None:
        """A hook to run actions after each game state."""
        if self.cooldown:
            self.cooldown -= 1

    def _cleanup(self) -> None:
        self.board.clear()
        self.x_signs.empty()
        self.o_signs.empty()

    def _render_text_blocks(self, blocks: dict) -> list[Rect]:
        results = []
        for title, kwargs in blocks.items():
            text = self.font.render(title, False, "White")
            rect = text.get_rect(**kwargs)
            results.append(self.screen.blit(text, rect))
        return results

    def update(self) -> None:
        """Update screen based on game state."""
        if method := getattr(self, f"_handle_{self.state.name.lower()}"):
            return method()

    def _handle_pre_game(self) -> None:
        """Handle welcome screen state."""
        blocks = {
            "Tic-Tac-Toe": {"midtop": (self.width / 2, 50)},
            "Press space to start": {"midbottom": (self.width / 2, self.height - 150)},
        }
        self.screen.fill((123, 123, 123))
        self._render_text_blocks(blocks)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.cooldown:
            logger.debug("pre game -> game")
            post(Event(CHANGE_TO_GAME_STATE, {"state": GameState.GAME}))

    def _handle_game(self) -> None:
        """Handle actual game of tic-tac-toe."""
        score_one = self.score[Symbol.PLAYER_ONE]
        score_two = self.score[Symbol.PLAYER_TWO]
        blocks = {
            f"Pad1   {score_one}: {score_two}   Pad2": {"midtop": (self.width / 2, 50)},
        }

        self.screen.fill((0, 0, 0))
        self._render_text_blocks(blocks)
        self._draw_board_lines()
        rects = self._draw_board()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.cooldown:
            logger.debug("game -> post game")
            post(Event(CHANGE_TO_POST_GAME_STATE, {"state": GameState.POST_GAME}))

        keys = pygame.mouse.get_pressed()
        if keys[0] and not self.cooldown:
            pos = pygame.mouse.get_pos()
            for index, rect in enumerate(rects):
                if rect.collidepoint(pos) and not self.cooldown:
                    self._place_next_symbol(index, rect)

        if self.board.check_winner():
            logger.debug("We have a winner!")
            player_who_won = Symbol.PLAYER_ONE
            if self.board.next_player == Symbol.PLAYER_ONE:
                player_who_won = Symbol.PLAYER_TWO

            self.player_who_won = player_who_won
            self.score[self.player_who_won] += 1
            post(Event(CHANGE_TO_POST_GAME_STATE, {"state": GameState.POST_GAME}))

    def _handle_post_game(self) -> None:
        """Handle post game state after someone wins."""
        score_one = self.score[Symbol.PLAYER_ONE]
        score_two = self.score[Symbol.PLAYER_TWO]
        blocks = {
            f"Pad1   {score_one}: {score_two}   Pad2": {"midtop": (self.width / 2, 50)},
            "Press space to play again": {
                "midbottom": (self.width / 2, self.height - 150)
            },
        }

        self.screen.fill("black")
        self._draw_board_lines()
        self._draw_board(win_state=True)
        self._render_text_blocks(blocks)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.cooldown:
            logger.debug("post game -> game")
            self._cleanup()
            post(Event(CHANGE_TO_GAME_STATE, {"state": GameState.GAME}))

    def _place_next_symbol(self, index: int, rect: Rect) -> None:
        logger.debug(f"collision with: {index}")
        self.cooldown = 60
        x, y = (index // self.board.size, index % self.board.size)
        next_player = self.board.next_player
        try:
            self.board.place_sign(x, y)
        except ValueError:
            return

        logger.debug(f"Add {next_player} sign")
        group = self.x_signs
        if next_player == Symbol.PLAYER_TWO:
            group = self.o_signs
        Marker(next_player, rect.center, group)

    def _draw_board(self, win_state: bool = False) -> list[Rect]:
        """Draw tic-tac-toe board."""
        color = "black"
        width = 1
        square_dimensions = (self.sign_size, self.sign_size)
        y_axis = 100
        rects = []
        for row in self.board.board:
            x_axis = 0
            for index, cell in enumerate(row):
                rect = Rect((x_axis, y_axis), square_dimensions)
                match cell:
                    case None:
                        rects.append(pygame.draw.rect(self.screen, color, rect, width))
                    case "X":
                        rects.append(pygame.draw.rect(self.screen, color, rect, width))
                    case "O":
                        rects.append(pygame.draw.rect(self.screen, color, rect, width))
                x_axis += self.sign_size
            y_axis += self.sign_size

        self.x_signs.draw(self.screen)
        self.o_signs.draw(self.screen)
        self.x_signs.update(who_won=self.player_who_won, win_state=win_state)
        self.o_signs.update(who_won=self.player_who_won, win_state=win_state)
        return rects

    def _draw_board_lines(self) -> None:
        color = "white"
        y_axis = 100
        width = 2
        coords = [
            [(self.sign_size, y_axis), (self.sign_size, self.sign_size * 3 + y_axis)],
            [
                (self.sign_size * 2, y_axis),
                (self.sign_size * 2, self.sign_size * 3 + y_axis),
            ],
            [(0, self.sign_size + 100), (self.sign_size * 3, self.sign_size + 100)],
            [
                (0, self.sign_size * 2 + 100),
                (self.sign_size * 3, self.sign_size * 2 + 100),
            ],
        ]
        for coord in coords:
            pygame.draw.line(self.screen, color, *coord, width=width)
