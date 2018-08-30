class GridWorldEngine(object):
    def __init__(self, sim_obj):
        self.sim_obj = sim_obj
        self.screen = None
        self.clock = None
        self.speed = 0
        self.frame = 0

    def render(self, visible=True, speed=1):
        if visible and self.screen is None:
            import pygame
            pygame.init()
            pygame.display.set_caption('GWE')
            self.screen = pygame.display.set_mode((1280, 720))
            self.clock = pygame.time.Clock()
            self.speed = speed
        if not visible and self.screen is not None:
            import pygame
            pygame.quit()
            self.screen = None
            self.clock = None
            self.speed = 0

    def step(self):
        state, info = self.sim_obj.step()
        self.display(state, info)
        self.frame += 1

    def display(self, state, info):
        if self.screen is None:
            return
        if self.speed >= 1 and self.frame % self.speed != 0:
            return
        self.clock.tick(60)
        import pygame
        pygame.pixelcopy.array_to_surface(self.screen, state)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()
