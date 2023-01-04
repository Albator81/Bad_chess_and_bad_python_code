import pygame as pg
import numpy as np

RES = WIDTH, HEIGHT = 500, 500
FPS = 60
SCALED_COORD = WIDTH // 8

FIRST_TURN = 'w'


def floor_my(number, ndigits: int = 0):
    sub_result = number * 10 ** ndigits // 1 * 10 ** - ndigits
    if ndigits <= 0:
        return int(sub_result)
    else:
        return float(format(sub_result, f'.{len(str(number))}f'))


def lerp(x, a, b):
    return a + x * (b-a)

def get_color(x, y, a, b, c, d):
    r = lerp(y, lerp(x, a[0], b[0]), lerp(x, c[0], d[0]))
    g = lerp(y, lerp(x, a[1], b[1]), lerp(x, c[1], d[1]))
    b = lerp(y, lerp(x, a[2], b[2]), lerp(x, c[2], d[2]))
    return (int(r), int(g), int(b))

rgb_square_points = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0)]
