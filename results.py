import numpy as np


class Results:
    def __init__(self, shape):
        self.marmots = np.empty(shape, dtype=int)
        self.vegetation = np.empty(shape, dtype=int)
        self.pasture = np.empty(shape, dtype=int)