import pygame
from enum import auto, Enum
import collections

Coord = collections.namedtuple("Coord", "x y")
Boundary = collections.namedtuple("Boundary", "lower upper")


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


def load_image(filename, scale=1):
    image = pygame.image.load(filename).convert()
    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    return pygame.transform.scale(image, size)
