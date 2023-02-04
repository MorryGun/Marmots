import numpy as np


class Results:
    def __init__(self, shape):
        # self.marmots = np.empty([rows, columns])
        # self.vegetation = np.empty([rows, columns])
        # self.pasture = np.empty([rows, columns])
        self.marmots = np.random.randint(0, 3, shape)
        self.vegetation = np.random.randint(0, 3, shape)
        self.pasture = np.random.randint(0, 3, shape)