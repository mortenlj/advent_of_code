import argparse
import enum
import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from importlib import resources as il_resources
from typing import Optional

import pygame

_MARGIN = 200


visualization_enabled = False
pause_enabled = False
fps = 0


class ImageMixIn:
    image: pygame.Surface

    def load(self, scale_factor):
        binary = il_resources.open_binary("ibidem.advent_of_code.visualizer.resources", self.value)
        image = pygame.image.load(binary).convert_alpha()
        self.image = pygame.transform.scale(image, (scale_factor, scale_factor))


class Tiles(ImageMixIn, enum.Enum):
    Grass = "bg_grass.png"
    Dirt = "bg_dirt.png"
    Stone = "bg_stone.png"
    Wall = "bg_wall.png"
    Water = "bg_water.png"
    Obstacle = "obstacle.png"


class Sprites(ImageMixIn, enum.Enum):
    Tree = "tree.png"
    Tank = "tank_base.png"
    RedTankTurret = "red_turret.png"
    Tombstone = "tombstone.png"


class Colors(enum.Enum):
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)

    def load(self, scale_factor):
        image = pygame.Surface((16, 16))
        image.fill(self.value)
        self.image = pygame.transform.scale(image, (scale_factor, scale_factor))



@dataclass
class Config:
    size_x: Optional[int] = None
    size_y: Optional[int] = None


def _get_scale_factor(size_x, size_y):
    if not visualization_enabled:
        return 1
    desktop_sizes = pygame.display.get_desktop_sizes()
    assert desktop_sizes, "No desktop sizes found"
    ds = desktop_sizes.pop()
    scale_factor_x = (ds[0] - _MARGIN) // size_x
    scale_factor_y = (ds[1] - _MARGIN) // size_y
    return min(scale_factor_x, scale_factor_y)


def load_images(scale_factor):
    if not visualization_enabled:
        return
    for tile in Tiles:
        tile.load(scale_factor)
    for sprite in Sprites:
        sprite.load(scale_factor)
    for color in Colors:
        color.load(scale_factor)


class Visualizer(metaclass=ABCMeta):
    def __init__(self, config: Config):
        if not visualization_enabled:
            return
        self._config = config
        self._scale_factor = _get_scale_factor(config.size_x, config.size_y)
        screen_x, screen_y = config.size_x * self._scale_factor, config.size_y * self._scale_factor
        load_images(self._scale_factor)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Advent of Code - Visualizer")
        self.screen = pygame.display.set_mode([screen_x, screen_y])
        self.screen.fill((20, 20, 20))
        self.draw_background()
        self._background = self.screen.copy()
        self._clock = pygame.time.Clock()
        pygame.display.flip()

    @abstractmethod
    def draw_background(self):
        pass

    def pause(self):
        if not visualization_enabled:
            return
        self.draw_message("Press any key to continue", 40)
        try:
            while pause_enabled:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN:
                        return
        finally:
            self.draw_background()

    def draw(self, x, y, sprite: ImageMixIn):
        if visualization_enabled:
            self.screen.blit(sprite.image, (x * self._scale_factor, y * self._scale_factor))

    def flip(self):
        if visualization_enabled:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
            self._clock.tick(fps)

    def close(self):
        global visualization_enabled
        if visualization_enabled:
            visualization_enabled = False
            pygame.quit()

    def draw_message(self, msg, size):
        if not visualization_enabled:
            return
        rect = self.screen.get_rect()
        font = pygame.font.Font(None, size)
        text = font.render(msg, True, (255, 255, 255))
        textRect = text.get_rect()
        x = rect.centerx - (textRect.width // 2)
        y = rect.centery - (textRect.height // 2)
        textRect.topleft = (x, y)
        self.screen.blit(text, textRect)
        pygame.display.flip()


def parse_cmdline():
    parser = argparse.ArgumentParser(description="Advent of Code")
    parser.add_argument("--visualize", action="store_true", default=True, help="Visualize the solution")
    parser.add_argument("--pause", action="store_true", default=True, help="Pause before start and after end")
    parser.add_argument("--fps", type=int, default=0, help="Frames per second")
    options, _ = parser.parse_known_args()
    global visualization_enabled, pause_enabled, fps
    visualization_enabled = options.visualize
    pause_enabled = options.pause
    fps = options.fps


def initialize_and_display_splash():
    parse_cmdline()
    if not visualization_enabled:
        return
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
