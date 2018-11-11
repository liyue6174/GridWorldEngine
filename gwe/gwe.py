from . import init_window, get_path
from .screen import Screen
import pygame


class GridWorldEngine(object):
    def __init__(self, sim_obj):
        self.sim_obj = sim_obj
        self.window = None
        self.screen = None
        self.clock = None
        self.speed = 0
        self.frame = 0
        self.font = None
        self.mouse_button_down = False
        self.mouse_position = None
        self.pause = False
        self.events = {
            pygame.K_p: self.pause_or_resume,
            pygame.K_c: self.speed_plus,
            pygame.K_x: self.speed_reduce,
            pygame.K_z: self.speed_reset,
        }

    def register_key_events(self, events: dict):
        self.events.update(events)

    def remove_key_events(self, keys: list):
        for key in keys:
            if key in self.events:
                self.events.pop(key)

    def pause_or_resume(self):
        self.pause = not self.pause

    def speed_plus(self):
        self.speed = self.speed + 1 if self.speed < 100 else 100

    def speed_reduce(self):
        self.speed = self.speed - 1 if self.speed > 1 else 1

    def speed_reset(self):
        self.speed = 1

    def render(self, visible=True, speed=1):
        if visible and self.window is None:
            self.window = init_window()
            self.screen = Screen(self.sim_obj.width, self.sim_obj.height)
            self.font = pygame.font.Font(get_path('gwe') + '/font/fss.ttf', 20)
            self.clock = pygame.time.Clock()
            self.speed = speed
        if not visible and self.window is not None:
            pygame.quit()
            self.screen = None
            self.window = None
            self.clock = None
            self.speed = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.screen.update_scale(pygame.mouse.get_pos(), 1)
                elif event.button == 5:
                    self.screen.update_scale(pygame.mouse.get_pos(), -1)
                self.mouse_button_down = True
                self.mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_down = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:
                    self.screen.update_scale(pygame.mouse.get_pos(), 1)
                elif event.key == pygame.K_MINUS:
                    self.screen.update_scale(pygame.mouse.get_pos(), -1)
                if event.key in self.events:
                    self.events[event.key]()
        if self.mouse_button_down:
            self.screen.update_offset(self.mouse_position, pygame.mouse.get_pos())
            self.mouse_position = pygame.mouse.get_pos()

    def step(self):
        self.handle_events()
        if self.pause:
            return
        state, info = self.sim_obj.step()
        self.display(state, info)
        self.frame += 1
        return info

    def display(self, state, info):
        if self.window is None:
            return
        if self.speed >= 1 and self.frame % self.speed != 0:
            return
        self.clock.tick(100)
        self.window.fill((0, 0, 0))
        self.screen.set_data(state)
        self.window.blit(self.screen, (0, 0))

        # show grid world index about mouse
        index_x, index_y = self.screen.get_index_by_position(pygame.mouse.get_pos())
        index_surface = self.font.render(f'Grid World Index: ({index_x}, {index_y})', True, (255, 255, 255))
        self.window.blit(index_surface, (800, 0))

        # show information
        if (index_x, index_y) in info:
            info_title_surface = self.font.render(f'[information]', True, (255, 255, 255))
            self.window.blit(info_title_surface, (800, 20))
            for number, (key, value) in enumerate(info[(index_x, index_y)].items()):
                info_surface = self.font.render(f'{key}: {value}', True, (255, 255, 255))
                self.window.blit(info_surface, (800, number * 20 + 40))
        pygame.display.update()
