import pygame


def load_image(filename, scale=1):
    image = pygame.image.load(filename).convert()
    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    return pygame.transform.scale(image, size)
