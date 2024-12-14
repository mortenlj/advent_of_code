import pygame

from ibidem.advent_of_code.board import Board
from ibidem.advent_of_code.visualizer import Config, Visualizer


class BoardVisualizer(Visualizer):
    def __init__(self, board: Board, sprite_mapping):
        self._board = board
        self._sprite_mapping = sprite_mapping
        config = Config(board.size_x, board.size_y)
        super().__init__(config)

    def draw_background(self):
        self._background = self.screen.copy()
        self.draw_board()

    def draw_board(self, board=None):
        self.screen.blit(self._background, (0, 0))
        if board is None:
            board = self._board
        grid = board.grid.copy()
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value is not None:
                    sprite = self._sprite_mapping.get(value)
                    if sprite is None:
                        continue
                    self.draw(x, y, sprite)
        pygame.display.flip()


