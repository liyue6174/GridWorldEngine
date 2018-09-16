__version__ = '0.0.3'

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


def init_window(title='GWE'):
    import pygame
    pygame.init()
    pygame.display.set_caption(title)
    pygame.key.set_repeat(10, 10)
    return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def close_window():
    pass


def clip(value, min_value, max_value):
    return min(max(min_value, value), max_value)
