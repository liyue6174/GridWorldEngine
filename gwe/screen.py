from . import SCREEN_WIDTH, SCREEN_HEIGHT, clip
import pygame
import numpy


class Screen(pygame.Surface):
    def __init__(self, game_width=SCREEN_WIDTH, game_height=SCREEN_HEIGHT):
        super().__init__((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__offset_x = (game_width - SCREEN_WIDTH) // 2
        self.__offset_y = (game_height - SCREEN_HEIGHT) // 2
        self.__scale = 1
        self.__size_x = 0
        self.__size_y = 0
        self.__epsilon_x = 0
        self.__epsilon_y = 0

    def set_data(self, data, frame_color=(255, 0, 0)):
        self.fill((0, 0, 0))
        self.__size_x, self.__size_y = data.shape
        scale, ssx, ssy = self.__scale, SCREEN_WIDTH, SCREEN_HEIGHT  # ss:screen_size
        lx, ly = self.__size_x * scale, self.__size_y * scale  # l:length
        tx, ty = self.__offset_x, self.__offset_y  # t:offset
        ix, iy = max(0, tx), max(0, ty)  # i:initialize
        nx, ny = ix // scale, iy // scale  # n:number
        dx, dy = ix % scale, iy % scale  # d:delta
        px, py = lx - ssx, ly - ssy  # p:position
        len_x = {True: ssx, tx < 0: tx + ssx, tx > px: lx - ix}[True]
        len_y = {True: ssy, ty < 0: ty + ssy, ty > py: ly - iy}[True]
        cx, cy = (len_x + dx - 1) // scale + 1, (len_y + dy - 1) // scale + 1  # c:count
        if cx > 0 and cy > 0:
            valid_data = data[nx:nx + cx, ny:ny + cy]
            scale_data = numpy.kron(valid_data, numpy.ones((scale, scale), dtype=int))
            render_data = scale_data[dx:dx + len_x, dy:dy + len_y]
            screen = pygame.Surface((len_x, len_y))
            pygame.pixelcopy.array_to_surface(screen, render_data)
            self.blit(screen, (max(0, -tx), max(0, -ty)))

        pos_l, pos_r = -tx - 1, lx - tx + 1  # l:left, r:right
        pos_u, pos_d = -ty - 1, ly - ty + 1  # u:up, d:down
        if tx < 0:
            pygame.draw.line(self, frame_color, (pos_l, pos_u), (pos_l, pos_d))
        if tx > px:
            pygame.draw.line(self, frame_color, (pos_r, pos_u), (pos_r, pos_d))
        if ty < 0:
            pygame.draw.line(self, frame_color, (pos_l, pos_u), (pos_r, pos_u))
        if ty > py:
            pygame.draw.line(self, frame_color, (pos_l, pos_d), (pos_r, pos_d))

    def update_offset(self, prev_position, cur_position):
        prev_pos_x, prev_pos_y = prev_position
        cur_pos_x, cur_pos_y = cur_position
        self.__offset_x += prev_pos_x - cur_pos_x
        self.__offset_y += prev_pos_y - cur_pos_y
        self.__offset_x = clip(self.__offset_x, -SCREEN_WIDTH, self.__size_x * self.__scale)
        self.__offset_y = clip(self.__offset_y, -SCREEN_HEIGHT, self.__size_y * self.__scale)

    def update_scale(self, mouse_position, delta_scale):
        mouse_x, mouse_y = mouse_position
        mouse_x = clip(mouse_x, 0, SCREEN_WIDTH - 1)
        mouse_y = clip(mouse_y, 0, SCREEN_HEIGHT - 1)
        prev_pos_x, prev_pos_y = mouse_x + self.__offset_x, mouse_y + self.__offset_y
        index_x, index_y = prev_pos_x / self.__scale, prev_pos_y / self.__scale
        self.__scale += delta_scale
        self.__scale = clip(self.__scale, 1, 100)
        next_pos_x = index_x * self.__scale + self.__epsilon_x - mouse_x
        next_pos_y = index_y * self.__scale + self.__epsilon_y - mouse_y
        self.__offset_x, self.__epsilon_x = int(next_pos_x), next_pos_x - int(next_pos_x)
        self.__offset_y, self.__epsilon_y = int(next_pos_y), next_pos_y - int(next_pos_y)
        self.__offset_x = clip(self.__offset_x, -SCREEN_WIDTH, self.__size_x * self.__scale)
        self.__offset_y = clip(self.__offset_y, -SCREEN_HEIGHT, self.__size_y * self.__scale)

    def get_index_by_position(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        index_x = (mouse_x + self.__offset_x) // self.__scale
        index_y = (mouse_y + self.__offset_y) // self.__scale
        if mouse_x >= SCREEN_WIDTH: return -1, -1
        if index_x < 0 or index_x >= self.__size_x: return -1, -1
        if index_y < 0 or index_y >= self.__size_y: return -1, -1
        return index_x, index_y
