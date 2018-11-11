__version__ = '0.0.6'

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


def init_window(title='GWE'):
    import pygame
    pygame.init()
    pygame.display.set_caption(title)
    pygame.key.set_repeat(500, 100)
    return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def close_window():
    pass


def clip(value, min_value, max_value):
    return min(max(min_value, value), max_value)

def get_path(name):
    import os
    directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_relative_path(name):
    import os
    directory = os.path.abspath(name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory
