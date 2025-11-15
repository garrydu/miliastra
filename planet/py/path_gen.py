from optimize1 import get_pNe
#  import numpy as np
from random import randint
#  from math import sin


def gen_dirs(n):
    l = list(range(1, n + 1))
    for i in range(n - 1, 1, -1):
        j = randint(0, i - 1)
        l[i], l[j] = l[j], l[i]
    return int(''.join([str(i) for i in l]))


def gen():
    ps, es = get_pNe()
    N = len(ps)
    vis = [0] * N
    neigb_vis = [0] * N
    e = []
    for i in range(N):
        e.append([])
    for i, j in es:
        e[i].append(j)
        e[j].append(i)
    d = [len(i) for i in e]
    vis[0] = 1
    for neigbor in e[0]:
        neigb_vis[neigbor] += 1
    stack = [0]
    stackd = [gen_dirs(d[0])]
    while len(stack) > 0:
        point = stack.pop()
        dirs = stackd.pop()
        # print(point, dirs)
        if neigb_vis[point] > 2:
            continue
        while dirs > 0:
            nxt = e[point][dirs % 10 - 1]
            dirs = dirs // 10
            # print(nxt)
            if vis[nxt]:
                continue
            if neigb_vis[nxt] > 2 and neigb_vis[point] == 2:
                continue
            if neigb_vis[nxt] > 1 and neigb_vis[point] <= 1:
                continue
            # print(nxt)
            vis[nxt] = 1
            for nxt_neib in e[nxt]:
                neigb_vis[nxt_neib] += 1
            if dirs > 0:
                stack.append(point)
                stackd.append(dirs)
            stack.append(nxt)
            stackd.append(gen_dirs(d[nxt]))
            break
    return vis


if __name__ == "__main__":
    # print(gen())
    # print(sum(gen()))
    # print(gen_dirs(7))
    #  print(blk_points())
    pass
