import numpy as np
from generator import Generator
from results import Results
from tile import Tile


class Simulator:
    def __init__(self, seed, columns, rows, tile_productivity, marmots_fertility, marmots_consumption):
        self.generator = Generator(seed)
        self.tiles = np.empty((rows, columns), dtype=object)
        self.tile_productivity = tile_productivity
        self.marmots_fertility = marmots_fertility
        self.marmots_consumption = marmots_consumption
        self.results = []
    
    
    def initiate(self) -> None:
        print(f'columns = {self.tiles.shape[1]}, rows = {self.tiles.shape[0]}')
        for x in range(self.tiles.shape[0]):
            for y in range(self.tiles.shape[1]):
                tile = Tile([y+1, x+1], self.tile_productivity, self.marmots_fertility, self.generator)
                self.tiles[x, y] = tile

        for x in range(self.tiles.shape[0]):
            for y in range(self.tiles.shape[1]):
                self.tiles[x, y].set_neighbors(self.tiles)

        test = Results(self.tiles.shape)
        test2 = Results(self.tiles.shape)
        test3 = Results(self.tiles.shape)
        self.results.extend([test, test2, test3])


    def simulate(self, pasture: int, duration: int) -> None:
        for _ in range(duration):
            self.next_year(pasture)


    def next_year(self, pasture: int) -> None:
        pass


    


