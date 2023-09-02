import numpy as np
from generator import Generator
from results import Results
from tile import Tile


class Simulator:
    def __init__(self, seed, columns, rows, tile_productivity, marmots_fertility, marmots_consumption, shrubbing_limit):
        self.generator = Generator(seed)
        self.tiles = np.empty((rows, columns), dtype=Tile)
        self.tile_productivity = tile_productivity
        self.marmots_fertility = marmots_fertility
        self.marmots_consumption = marmots_consumption
        self.results = []
        self.shrubbing_limit = shrubbing_limit * 1000
    
    
    def initiate(self) -> None:
        initial_results = Results([self.tiles.shape[0], self.tiles.shape[1]])

        #initiate tiles
        for x in range(self.tiles.shape[0]):
            for y in range(self.tiles.shape[1]):
                tile = Tile([y+1, x+1], self.tile_productivity, self.marmots_fertility, self.generator)
                self.tiles[x, y] = tile

                initial_results.marmots[x, y] = tile.population
                initial_results.vegetation[x, y] = tile.vegetation
                initial_results.pasture[x, y] = 0

        #as soon as all tile ids set, we can identify tiles' neighbors
        for x in range(self.tiles.shape[0]):
            for y in range(self.tiles.shape[1]):
                self.tiles[x, y].set_neighbors(self.tiles)

        self.results.append(initial_results)

    def simulate(self, pasture: int, duration: int) -> None:
        for _ in range(duration):
            self.next_year(pasture)


    def next_year(self, pasture: int) -> None:
        yearly_results = Results([self.tiles.shape[0], self.tiles.shape[1]])

        #pasture
        if (pasture == 0):
            yearly_results.pasture = np.zeros([self.tiles.shape[0], self.tiles.shape[1]])
        else:
            for x in range(self.tiles.shape[0]):
                for y in range(self.tiles.shape[1]):
                    current_tile = self.tiles[x, y]

                    if (current_tile.not_is_shrub):
                        pasture_volumes = current_tile.vegetation * (pasture / 100)
                        
                        current_tile.vegetation = current_tile.vegetation - pasture_volumes
                        yearly_results.pasture[x, y] = pasture_volumes / 1000

        #consumption + reproduction
        for x in range(self.tiles.shape[0]):
            for y in range(self.tiles.shape[1]):
                current_tile = self.tiles[x, y]
                
                if (current_tile.not_is_shrub):
                    
                    #consumption
                    for _ in range(current_tile.population):
                        individual_consumption = round(self.generator.uniform(self.marmots_consumption[0], self.marmots_consumption[1]))

                        if (current_tile.vegetation - individual_consumption >= 0):
                            current_tile.vegetation = current_tile.vegetation - individual_consumption
                        else:
                            current_tile.population = current_tile.population - 1

                    if (current_tile.population >= 2):
                        current_fertility = round(self.generator.gamma(self.marmots_fertility))
                        for _ in range(current_fertility):
                            individual_consumption = round(self.generator.uniform(self.marmots_consumption[0], self.marmots_consumption[1]))

                            if (current_tile.vegetation - individual_consumption >= 0):
                                current_tile.vegetation = current_tile.vegetation - individual_consumption
                                current_tile.population = current_tile.population + 1

                yearly_results.marmots[x, y] = current_tile.population

        #vegetation
        for x in range(self.tiles.shape[0]):
            for y in range(self.tiles.shape[1]):
                current_tile = self.tiles[x, y]

                if (current_tile.not_is_shrub):
                    current_tile.vegetation = current_tile.vegetation + current_tile.productivity

                yearly_results.vegetation[x, y] = current_tile.vegetation /1000

                if (self.shrubbing_limit != 0 and current_tile.vegetation > self.shrubbing_limit):
                    current_tile.not_is_shrub = False
                    current_tile.population = 0

        self.results.append(yearly_results)
