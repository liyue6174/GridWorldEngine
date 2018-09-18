import numpy as np


class LangtonAnt(object):
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height

    def reset(self):
        self.world = np.zeros((self.width, self.height), dtype=int)
        self.pos_x = self.width // 2
        self.pos_y = self.height // 2
        self.direction = (0, 1)
        self.rotate_left = {(0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0), (1, 0): (0, 1)}
        self.rotate_right = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1)}

    def step(self):
        if 0 <= self.pos_x < self.width and 0 <= self.pos_y < self.height:
            value = self.world[self.pos_x, self.pos_y]
            rotate_dict = self.rotate_left if value == 0 else self.rotate_right
            self.direction = rotate_dict[self.direction]
            self.world[self.pos_x, self.pos_y] = 1 - value
            self.pos_x += self.direction[0]
            self.pos_y += self.direction[1]
        return self.world * 0xffffff, {}


if __name__ == '__main__':
    from gwe.gwe import GridWorldEngine

    game = LangtonAnt()
    game.reset()
    gwe = GridWorldEngine(sim_obj=game)
    gwe.render(visible=True, speed=1)
    while True:
        gwe.step()
