import numpy as np
from math import acos, sin

display_ps = []
es = []


class block:
    def __init__(self, y, theta):
        y = y - 0.0071174377224199285
        theta += 3.8832220774509327
        self.is_end = False
        if y <= -1:
            self.is_end = True
            return
        radius = np.sqrt(1 - y**2)
        x = np.cos(theta) * radius
        z = np.sin(theta) * radius

        self.ctr = np.array([x, y, z])
        display_ps.append(self.ctr)
        self.stack_prev = None
        self.degree = 0
        self.edges = []
        self.vis = False
        self.neigb_vis = 0
        self.dirs = 0
        self.nxt = block(y, theta)
        return

    def trigger(self, cmd):
        if self.is_end:
            return
        if cmd == 1:  # find edge
            self.find_edge()

        return

    def find_edge(self):
        lmt = 0.954555620192181
        theta = acos(1 - abs(self.ctr[1]))
        ylmt = -max(abs(sin(0.3 + theta)), sin(theta)) * 0.3 + self.ctr[1]
        j = self.nxt
        for i in range(50):
            if j.is_end:
                break
            if j.ctr[1] < ylmt:
                break
            if np.dot(self.ctr, j.ctr) > lmt:
                self.edges.append(j)
                j.edges.append(self)
                es.append((self.ctr, j.ctr))
            j = j.nxt
        self.nxt.trigger(1)
        return


def test():
    b = block(1, 0)
    b.trigger(1)
    return display_ps, es


if __name__ == "__main__":
    print(test())
