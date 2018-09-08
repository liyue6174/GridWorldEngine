from . import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SIZE
import pygame
import numpy


class Screen(pygame.Surface):
    def __init__(self):
        super().__init__(SCREEN_SIZE)
        self.__scale = 1
        self.__min_scale = 1
        self.__max_scale = 100
        self.__size_x = 0
        self.__size_y = 0
        self.__offset_x = 0
        self.__offset_y = 0
        self.__epsilon_x = 0
        self.__epsilon_y = 0

    def set_data(self, data):
        self.__size_x, self.__size_y = data.shape
        assert self.__size_x >= 8 and self.__size_y >= 8, 'the array.shape is invalid'

        if self.__size_x * self.__scale < SCREEN_WIDTH or self.__size_y * self.__scale < SCREEN_HEIGHT:
            self.__min_scale = max((SCREEN_WIDTH - 1) // self.__size_x, (SCREEN_HEIGHT - 1) // self.__size_y) + 1
            self.__scale = self.__min_scale
        assert self.__scale <= 100, 'scale is too large'

        index_x, index_y = self.__offset_x // self.__scale, self.__offset_y // self.__scale
        delta_x, delta_y = self.__offset_x % self.__scale, self.__offset_y % self.__scale
        count_x = (SCREEN_WIDTH + delta_x - 1) // self.__scale + 1
        count_y = (SCREEN_HEIGHT + delta_y - 1) // self.__scale + 1

        valid_data = data[index_x:index_x + count_x, index_y:index_y + count_y]
        scale_data = numpy.kron(valid_data, numpy.ones((self.__scale, self.__scale), dtype=int))
        render_data = scale_data[delta_x:delta_x + SCREEN_WIDTH, delta_y:delta_y + SCREEN_HEIGHT]

        pygame.pixelcopy.array_to_surface(self, render_data)

    def update_offset(self, prev_position, cur_position):
        prev_pos_x, prev_pos_y = prev_position
        cur_pos_x, cur_pos_y = cur_position
        self.__offset_x += prev_pos_x - cur_pos_x
        self.__offset_y += prev_pos_y - cur_pos_y
        self.__offset_x = min(max(0, self.__offset_x), self.__size_x * self.__scale - SCREEN_WIDTH)
        self.__offset_y = min(max(0, self.__offset_y), self.__size_y * self.__scale - SCREEN_HEIGHT)

    def update_scale(self, mouse_position, delta_scale):
        mouse_x, mouse_y = mouse_position
        mouse_x = min(max(0, mouse_x), SCREEN_WIDTH - 1)
        mouse_y = min(max(0, mouse_y), SCREEN_HEIGHT - 1)
        prev_pos_x, prev_pos_y = mouse_x + self.__offset_x, mouse_y + self.__offset_y
        index_x, index_y = prev_pos_x / self.__scale, prev_pos_y / self.__scale
        self.__scale += delta_scale
        self.__scale = min(max(self.__min_scale, self.__scale), self.__max_scale)
        next_pos_x = index_x * self.__scale + self.__epsilon_x - mouse_x
        next_pos_y = index_y * self.__scale + self.__epsilon_y - mouse_y
        self.__offset_x, self.__epsilon_x = int(next_pos_x), next_pos_x - int(next_pos_x)
        self.__offset_y, self.__epsilon_y = int(next_pos_y), next_pos_y - int(next_pos_y)
        self.__offset_x = min(max(0, self.__offset_x), self.__size_x * self.__scale - SCREEN_WIDTH)
        self.__offset_y = min(max(0, self.__offset_y), self.__size_y * self.__scale - SCREEN_HEIGHT)
