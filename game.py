import collections
from enum import Enum, auto

import pygame

from utils import load_image

pygame.init()

FPS = 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

Coord = collections.namedtuple("Coord", "x y")


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class Ship(pygame.sprite.Sprite):
    def __init__(self, initial_coord=None):
        self.image = load_image("ship.png", 4)
        self.rect = self.image.get_rect()
        self.speed = 500
        if initial_coord:
            self.rect.centerx = initial_coord.x
            self.rect.centery = initial_coord.y

    def move(self, direction, delta_time):
        x_offset = 0
        match direction:
            case Direction.RIGHT:
                x_offset = int(self.speed * delta_time)
            case Direction.LEFT:
                x_offset = int(-self.speed * delta_time)
        self.rect = self.rect.move(x_offset, 0)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def __create_ship(self):
        initial_coord = Coord(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.75))
        return Ship(initial_coord)

    def run(self):
        running = True
        delta_time = 0
        ship = self.__create_ship()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill("black")
            self.screen.blit(ship.image, ship.rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            if keys[pygame.K_RIGHT]:
                ship.move(Direction.RIGHT, delta_time)
            if keys[pygame.K_LEFT]:
                ship.move(Direction.LEFT, delta_time)

            pygame.display.flip()
            delta_time = self.clock.tick(FPS) / 1000


if __name__ == "__main__":
    game = Game()
    game.run()
