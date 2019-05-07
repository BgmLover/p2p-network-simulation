import matplotlib.pyplot as plt
import numpy as np
import config
import time

max_distance = float('inf')


class Point:
    x = 0
    y = 0

    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def get_distance_of_point(self, point):
        return np.sqrt(np.square(self.x - point.x) + np.square(self.y - point.y))


def random_generate_point(xbegin, xend, ybegin, yend, size):
    x_array = np.random.randint(xbegin, xend, size)
    y_array = np.random.randint(ybegin, yend, size)
    points = list()
    for i in range(size):
        points.append(Point(x_array[i], y_array[i]))
    return points
