import numpy as np
from scipy import signal


class GameOfLife(object):
    def __init__(self, width=1024, height=1024):
        self.width = width
        self.height = height
        self.kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)

    def reset(self):
        self.world = np.zeros((self.width, self.height), dtype=int)
        s, t = self.width // 15, self.height // 15
        self.world[s:self.width - s + 1, self.width // 2] = 1
        self.world[self.height // 2, t: self.height - t + 1] = 1

    def step(self):
        world = signal.convolve2d(self.world, self.kernel, mode='same', boundary='fill')
        self.world[np.logical_and(world == 3, self.world == 0)] = 1
        self.world[np.logical_or(world < 2, world > 3)] = 0
        return self.world * 0xffffff, {}


if __name__ == '__main__':
    from gwe.gwe import GridWorldEngine

    life_game = GameOfLife()
    life_game.reset()
    gwe = GridWorldEngine(sim_obj=life_game)
    gwe.render(visible=True, speed=1)
    while True:
        gwe.step()
