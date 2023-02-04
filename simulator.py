import numpy as np
from generator import Generator
from results import Results


class Simulator:
    def __init__(self, seed, rows, columns, tile_productivity, marmots_fertility, marmots_consumption):
        self.generator = Generator(seed)
        self.tiles = np.empty((rows, columns), dtype=object)
        self.tile_productivity = tile_productivity
        self.marmots_fertility = marmots_fertility
        self.marmots_consumption = marmots_consumption
        self.results = []
    
    def initiate(self) -> None:
        test = Results(self.tiles.shape)
        test2 = Results(self.tiles.shape)
        test3 = Results(self.tiles.shape)
        self.results.extend([test, test2, test3])


    def simulate(self, pasture: int, duration: int) -> None:
        for _ in range(duration):
            self.next_year(pasture)


    def next_year(self, pasture: int) -> None:
        pass


    


