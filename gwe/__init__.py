__version__ = '0.0.2'

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


def init_window(title='GWE'):
    import pygame
    pygame.init()
    pygame.display.set_caption(title)
    pygame.key.set_repeat(1, 1)
    return pygame.display.set_mode(WINDOW_SIZE)


def close_window():
    pass
