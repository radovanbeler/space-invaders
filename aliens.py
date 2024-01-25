import pygame
from utils import Direction, load_image, Coord, Boundary

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class AlienStateMachine:
    def __init__(self):
        right = self.State(Direction.RIGHT)
        down = self.State(Direction.DOWN)
        left = self.State(Direction.LEFT)
        right.add_transition(down, down)
        down.add_transition(right, left)
        down.add_transition(left, right)
        left.add_transition(down, down)

        self.right = right
        self.down = down
        self.left = left
        self.prev = down
        self.current = right

    def next(self):
        prev = self.prev
        self.prev = self.current
        self.current = self.current.next(prev)

    def direction(self):
        return self.current.direction

    class State:
        def __init__(self, direction):
            self.direction = direction
            self.transitions = {}

        def add_transition(self, on, next):
            self.transitions[on] = next

        def next(self, on):
            return self.transitions[on]


class Alien(pygame.sprite.Sprite):
    def __init__(self, boundary, initial_coord=None, on_collision=None):
        super().__init__()
        self.image = load_image("alien.png", 4)
        self.rect = self.image.get_rect()
        if initial_coord:
            self.rect.centerx = initial_coord.x
            self.rect.centery = initial_coord.y
        self.speed = 300
        self.boundary = boundary
        self.on_collision = on_collision
        self.state = AlienStateMachine()
        self.down_count = 0
        self.down_count_limit = 10

    def __within_boundary(self, next_rect):
        return (
            next_rect.left >= self.boundary.lower
            and next_rect.right <= self.boundary.upper
        )

    def __next_rect(self, direction, delta_time):
        x_offset = 0
        y_offset = 0
        match direction:
            case Direction.RIGHT:
                x_offset = int(self.speed * delta_time)
            case Direction.DOWN:
                y_offset = int(self.speed * delta_time)
            case Direction.LEFT:
                x_offset = int(-self.speed * delta_time)
        return self.rect.move(x_offset, y_offset)

    def move(self, delta_time):
        direction = self.state.direction()

        if direction == Direction.DOWN:
            if self.down_count >= self.down_count_limit:
                self.state.next()
                self.down_count = 0
            else:
                self.down_count += 1

        next_rect = self.__next_rect(direction, delta_time)
        if self.__within_boundary(next_rect):
            self.rect = next_rect
        elif self.on_collision:
            self.on_collision()

    def change_direction(self):
        self.state.next()


class Aliens:
    def __init__(self):
        self.aliens = self.__create_aliens()

    def __on_collision(self):
        for alien in self.aliens:
            alien.change_direction()

    def __create_alien(self):
        initial_coord = Coord(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.5))
        boundary = Boundary(0, SCREEN_WIDTH)
        return Alien(boundary, initial_coord, self.__on_collision)

    def __create_aliens(self):
        alien = self.__create_alien()
        return [alien]

    def move(self, delta_time):
        for alien in self.aliens:
            alien.move(delta_time)

    def __iter__(self):
        return iter(self.aliens)
