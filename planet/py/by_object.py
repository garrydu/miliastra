import numpy as np
from math import acos, sin
import time
from path_gen import gen_dirs
#  from statistics import mean

#  import sys
#
#  # Default is usually 1000
#  print(sys.getrecursionlimit())  # Check current limit
#
#  # Increase it (be careful!)
#  sys.setrecursionlimit(5000)

display_ps = []
es = []


class block:
    def __init__(self, y, theta, n):
        y = y - 0.0071174377224199285
        theta += 3.8832220774509327
        self.is_end = False
        self.n = n
        if y <= -0.99:
            self.is_end = True
            return
        radius = np.sqrt(1 - y**2)
        x = np.cos(theta) * radius
        z = np.sin(theta) * radius

        self.ctr = np.array([x, y, z])
        #  display_ps.append(self.ctr)
        self.stack_prev = self
        self.degree = 0
        self.edges = []
        self.vis = False
        self.neigb_vis = 0
        self.dirs = 0
        self.big_disp = False
        self.nxt = block(y, theta, n + 1)
        return

    def trigger(self, cmd):
        if self.is_end:
            return
        if cmd == 1:  # find edge
            self.find_edge()
        elif cmd == 2:  # path gen
            self.path_gen()
        elif cmd == 3:
            self.display()
        return

    def display(self):
        # print(self.degree, self.neigb_vis)
        if not self.vis:
            # unvis_nbs=len(self.edges)-self.neigb_vis
            # print(unvis_nbs)
            display_ps.append(self.ctr)
            # if unvis_nbs==0:
            # display_ps.append(np.array([self.ctr[0],self.ctr[1]+0.01,self.ctr[2]]))
            # else:
            # new_es=[]
            for neib in self.edges:
                if not neib.vis:
                    if neib.ctr[1] < self.ctr[1] or neib.big_disp:
                        es.append((self.ctr, neib.ctr))
            # if len(new_es)==1:
            #     es.append(new_es[0])
            # elif len(new_es)==0:
            #     display_ps.append(np.array([self.ctr[0],self.ctr[1]+0.01,self.ctr[2]]))
            # elif not self.big_disp:
            #     triangle=[self.ctr]
            #     self.big_disp=True
            #     for neib in self.edges:
            #         if not neib.vis:
            #             triangle.append(neib.ctr)
            #             neib.big_disp=True
            #             # if neib.ctr[1]<self.ctr[1]:
            #             #     es.append((self.ctr, neib.ctr))
            #     display_ps.append(np.array([
            #         mean([j[i] for j in triangle])
            #         for i in range(3)]))
        self.nxt.trigger(3)
        return

    def path_gen(self):
        #  print(self.ctr[1], self.dirs, self.degree)
        if self.degree == 0:
            self.degree = len(self.edges)
            self.dirs = gen_dirs(self.degree)
        if self.neigb_vis > 2:
            if self.stack_prev != self:
                self.stack_prev.trigger(2)
            return
        nofound = True
        for _ in range(7):
            if self.dirs == 0:
                break
            nxt = self.edges[self.dirs % 10 - 1]
            self.dirs = self.dirs // 10
            if nxt.vis:
                continue
            if nxt.neigb_vis > 2 and self.neigb_vis == 2:
                continue
            if nxt.neigb_vis > 1 and self.neigb_vis <= 1:
                continue
            nxt.vis = True
            for neigbor in nxt.edges:
                neigbor.neigb_vis += 1
            prev = self if self.dirs > 0 else self.stack_prev
            nxt.stack_prev = prev
            nxt.trigger(2)
            nofound = False
            break
        if nofound and self.stack_prev != self:
            self.stack_prev.trigger(2)
        return

    def find_edge(self):
        lmt = 0.954555620192181
        theta = acos(abs(self.ctr[1]))
        ylmt = -max(abs(sin(0.3 + theta)), sin(theta)) * 0.3 + self.ctr[1]
        j = self.nxt
        cross_head = False
        if self.n in [46, 200, 45, 60, 57, 201]:
            cross_head = True
        for i in range(50):
            if j.is_end:
                break
            if j.ctr[1] < ylmt:
                break
            if np.dot(self.ctr, j.ctr) > lmt:
                if cross_head:
                    if j.n in [80, 213, 79, 68, 65, 235]:
                        continue
                self.edges.append(j)
                j.edges.append(self)
                #  es.append((self.ctr, j.ctr))
            j = j.nxt
        self.nxt.trigger(1)
        return


def test():
    start = time.perf_counter()

    b = block(1, 0, 0)
    b.trigger(1)
    b.vis = True
    for neigbor in b.edges:
        neigbor.neigb_vis += 1
    b.trigger(2)
    b.trigger(3)

    end = time.perf_counter()
    elapsed_us = (end - start) * 1_000_000
    print(f"Execution time: {elapsed_us:.2f} µs")
    return display_ps, es


if __name__ == "__main__":
    p, e = test()
    print(len(p), len(e))
