from math import *

R = 7.5
bWidth = 2


def row_len():
    theta = pi/2
    step = atan(bWidth/2/R)*2
    i = 0
    while (theta > 0):
        print(theta, i, R*sin(theta)*2*pi/bWidth)
        theta -= step
        i += 1


if __name__ == "__main__":
    row_len()
