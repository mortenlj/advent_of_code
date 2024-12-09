import enum
import threading
from dataclasses import field, dataclass
from importlib import resources

import pygame

from . import Board


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
    scale_factor: int
    sprite_mapping: dict = field(repr=False, compare=False)
    exit_signal: threading.Event = field(default=threading.Event(), init=False, repr=False, compare=False)


class Visualizer:
    def __init__(self, board: Board, config: Config):
        self.board = board
        self.config = config
        screen_x, screen_y = board.size_x * config.scale_factor, board.size_y * config.scale_factor
        self.screen = pygame.display.set_mode([screen_x, screen_y])
        sprite_size = Images.Grass.image.get_width()
        self.screen.fill((20, 20, 20))
        for x in range(0, screen_x, sprite_size):
            for y in range(0, screen_y, sprite_size):
                self.screen.blit(Images.Grass.image, (x, y))
        pygame.display.flip()

    def run(self):
        while not self.config.exit_signal.is_set():
            self.draw_board()
        pygame.quit()

    def draw_board(self, board=None):
        if board is None:
            board = self.board
        grid = board.grid.copy()
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value is not None:
                    self.draw(x, y, value)
        pygame.display.flip()

    def draw(self, x, y, value):
        sprite = self.config.sprite_mapping.get(value)
        if sprite is None:
            return
        self.screen.blit(sprite.image, (x * self.config.scale_factor, y * self.config.scale_factor))

    def close(self):
        self.config.exit_signal.set()
        pygame.quit()


def visualize(board: Board, config: Config):
    """Step by step visaualization of the board."""
    initialize_and_display_splash()
    for image in Images:
        image.load(config.scale_factor)
    return Visualizer(board, config)


def _visualize(board: Board, config: Config):
    initialize_and_display_splash()
    for image in Images:
        image.load(config.scale_factor)
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
