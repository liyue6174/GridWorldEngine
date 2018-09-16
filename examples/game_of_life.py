import numpy as np
from scipy import signal


class GameOfLife(object):
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        self.kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)

    def reset(self):
        self.world = np.zeros((self.width, self.height), dtype=int)
        self.world[60:741, 400] = self.world[400, 60:741] = 1

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
