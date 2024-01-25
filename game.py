import pygame

from utils import load_image, Direction, Boundary, Coord

from aliens import Aliens


pygame.init()

FPS = 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Ship(pygame.sprite.Sprite):
    def __init__(self, initial_coord=None, boundary=None):
        super().__init__()
        self.image = load_image("ship.png", 4)
        self.rect = self.image.get_rect()
        self.speed = 500
        self.__on_fire = None
        if initial_coord:
            self.rect.centerx = initial_coord.x
            self.rect.centery = initial_coord.y
        self.boundary = boundary

    def __in_boundary(self, next_rect):
        if not self.boundary:
            return True

        return (
            next_rect.left >= self.boundary.lower
            and next_rect.right <= self.boundary.upper
        )

    def move(self, direction, delta_time):
        x_offset = 0
        match direction:
            case Direction.RIGHT:
                x_offset = int(self.speed * delta_time)
            case Direction.LEFT:
                x_offset = int(-self.speed * delta_time)
        next_rect = self.rect.move(x_offset, 0)
        if self.__in_boundary(next_rect):
            self.rect = next_rect

    def on_fire(self, callback):
        self.__on_fire = callback

    def fire(self):
        if self.__on_fire:
            bullet = "bullet"
            self.__on_fire(bullet)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def __create_ship(self):
        initial_coord = Coord(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.75))
        boundary = Boundary(0, SCREEN_WIDTH)
        return Ship(initial_coord, boundary)

    def __space_released(self, event):
        return event.type == pygame.KEYUP and event.key == pygame.K_SPACE

    def run(self):
        running = True
        delta_time = 0
        ship = self.__create_ship()
        ship.on_fire(lambda bullet: print(bullet))
        aliens = Aliens()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.__space_released(event):
                    ship.fire()

            aliens.move(delta_time)

            self.screen.fill("black")
            self.screen.blit(ship.image, ship.rect)
            for alien in aliens:
                self.screen.blit(alien.image, alien.rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            if keys[pygame.K_RIGHT]:
                ship.move(Direction.RIGHT, delta_time)
            if keys[pygame.K_LEFT]:
                ship.move(Direction.LEFT, delta_time)

            pygame.display.flip()
            delta_time = self.clock.tick(FPS) / 1000

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
