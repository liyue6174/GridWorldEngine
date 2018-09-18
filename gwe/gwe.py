from . import init_window, get_path
from .screen import Screen


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

    def render(self, visible=True, speed=1):
        if visible and self.window is None:
            self.window = init_window()
            self.screen = Screen(self.sim_obj.width, self.sim_obj.height)
            import pygame
            self.font = pygame.font.Font(get_path('gwe') + '/font/fss.ttf', 20)
            self.clock = pygame.time.Clock()
            self.speed = speed
        if not visible and self.window is not None:
            import pygame
            pygame.quit()
            self.screen = None
            self.window = None
            self.clock = None
            self.speed = 0

    def step(self):
        state, info = self.sim_obj.step()
        self.display(state, info)
        self.frame += 1

    def display(self, state, info):
        if self.window is None:
            return
        if self.speed >= 1 and self.frame % self.speed != 0:
            return
        self.clock.tick(100)
        self.window.fill((0, 0, 0))
        self.screen.set_data(state)
        self.window.blit(self.screen, (0, 0))

        import pygame
        mouse_pos = self.font.render(str(pygame.mouse.get_pos()), True, (255, 255, 255))
        self.window.blit(mouse_pos, (800, 0))
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
        if self.mouse_button_down:
            self.screen.update_offset(self.mouse_position, pygame.mouse.get_pos())
            self.mouse_position = pygame.mouse.get_pos()

        pygame.display.update()
