import enum
import os
import threading
from dataclasses import field, dataclass
from importlib import resources
from typing import Optional

import pygame

from . import Board

_MARGIN = 20


class Images(enum.Enum):
    Grass = (enum.auto(), "bg_grass.png")
    Dirt = (enum.auto(), "bg_dirt.png")
    Stone = (enum.auto(), "bg_stone.png")
    Wall = (enum.auto(), "bg_wall.png")
    Water = (enum.auto(), "bg_water.png")
    Tree = (enum.auto(), "tree.png")
    Obstacle = (enum.auto(), "obstacle.png")
    Guard = (enum.auto(), "guard.png")

    def __init__(self, value, filename):
        self._value_ = value
        self._filename = filename
        self.image = None

    def load(self, scale_factor):
        binary = resources.open_binary("ibidem.advent_of_code.board.resources", self._filename)
        image = pygame.image.load(binary).convert_alpha()
        self.image = pygame.transform.scale(image, (scale_factor, scale_factor))


@dataclass
class Config:
    sprite_mapping: dict = field(repr=False, compare=False)
    scale_factor: Optional[int] = field(default=None)
    exit_signal: threading.Event = field(default=threading.Event(), init=False, repr=False, compare=False)


def _get_scale_factor(board, config):
    desktop_sizes = pygame.display.get_desktop_sizes()
    if config.scale_factor is None:
        for ds in desktop_sizes:
            scale_factor_x = (ds[0] - _MARGIN) // board.size_x
            scale_factor_y = (ds[1] - _MARGIN) // board.size_y
        scale_factor = min(scale_factor_x, scale_factor_y)
    else:
        scale_factor = config.scale_factor
    return scale_factor


class Visualizer:
    def __init__(self, board: Board, config: Config):
        self._board = board
        self._config = config
        self._scale_factor = _get_scale_factor(board, config)
        screen_x, screen_y = board.size_x * self._scale_factor, board.size_y * self._scale_factor
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Advent of Code - Board Visualizer")
        self.screen = pygame.display.set_mode([screen_x, screen_y])
        sprite_size = Images.Grass.image.get_width()
        self.screen.fill((20, 20, 20))
        for x in range(0, screen_x, sprite_size):
            for y in range(0, screen_y, sprite_size):
                self.screen.blit(Images.Grass.image, (x, y))
        pygame.display.flip()

    def pause(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    return

    def run(self):
        while not self._config.exit_signal.is_set():
            self.draw_board()
        pygame.quit()

    def draw_board(self, board=None):
        if board is None:
            board = self._board
        grid = board.grid.copy()
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value is not None:
                    self.draw(x, y, value)
        pygame.display.flip()

    def draw(self, x, y, value):
        sprite = self._config.sprite_mapping.get(value)
        if sprite is None:
            return
        self.screen.blit(sprite.image, (x * self._scale_factor, y * self._scale_factor))

    def close(self):
        self._config.exit_signal.set()
        pygame.quit()


def visualize(board: Board, config: Config) -> Visualizer:
    """Step by step visaualization of the board."""
    initialize_and_display_splash()
    scale_factor = _get_scale_factor(board, config)
    for image in Images:
        image.load(scale_factor)
    return Visualizer(board, config)


def _visualize(board: Board, config: Config):
    initialize_and_display_splash()
    scale_factor = _get_scale_factor(board, config)
    for image in Images:
        image.load(scale_factor)
    visualizer = Visualizer(board, config)
    visualizer.run()


def visualize_background(board, config):
    """Launches a thread in the background which is responsible for visualizing the board."""
    threading.Thread(target=_visualize, args=(board, config)).start()


def initialize_and_display_splash():
    pygame.init()
    screen = pygame.display.set_mode((320, 200))
    rect = screen.get_rect()
    font = pygame.font.Font(None, 20)
    text = font.render("Initializing, please wait...", True, (255, 255, 255))
    textRect = text.get_rect()
    x = rect.centerx - (textRect.width / 2)
    y = rect.centery - (textRect.height / 2)
    textRect.topleft = (x, y)
    screen.blit(text, textRect)
    pygame.display.flip()
    print("Display initialized")
