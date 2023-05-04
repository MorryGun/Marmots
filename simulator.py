import numpy as np
from generator import Generator
from results import Results
from tile import Tile


class Simulator:
    def __init__(self, seed, columns, rows, tile_productivity, marmots_fertility, marmots_consumption):
        self.generator = Generator(seed)
        self.tiles = np.empty((rows, columns), dtype=Tile)
        self.tile_productivity = tile_productivity
        self.marmots_fertility = marmots_fertility
        self.marmots_consumption = marmots_consumption
        self.results = []
    
    
    def initiate(self) -> None:
        initial_results = Results([self.tiles.shape[0], self.tiles.shape[1]])

        #initiate tiles
        for x in range(self.tiles.shape[0]):
            for y in range(self.tiles.shape[1]):
                tile = Tile([y+1, x+1], self.tile_productivity, self.marmots_fertility, self.generator)
                self.tiles[x, y] = tile

                initial_results.marmots[y, x] = tile.population
                initial_results.vegetation[y, x] = tile.vegetation
                initial_results.pasture[y, x] = 0

        #as soon as all tile ids set, we can identify tiles' neighbors
        for x in range(self.tiles.shape[0]):
            for y in range(self.tiles.shape[1]):
                self.tiles[x, y].set_neighbors(self.tiles)

        self.results.append(initial_results)

    def simulate(self, pasture: int, duration: int) -> None:
        for _ in range(duration):
            self.next_year(pasture)


    def next_year(self, pasture: int) -> None:
        pass


    


