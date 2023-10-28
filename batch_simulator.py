import numpy as np
from generator import Generator
from simulator import Simulator
from tile import Tile


class BatchSimulator(Simulator):
    def __init__(self, batch_size, tile_productivity, marmots_fertility, marmots_consumption, shrubbing_limit, initial_population):
        self.generator = Generator(0)
        self.tiles = np.empty((1,1), dtype=Tile)
        self.tile_productivity = tile_productivity
        self.marmots_fertility = marmots_fertility
        self.marmots_consumption = marmots_consumption
        self.results = []
        self.shrubbing_limit = shrubbing_limit * 1000
        self.initial_population = initial_population
        self.batch_results = []
        self.batch_size = batch_size

    
    def batch_simulate(self, years) -> None:
        #loop by pasture level
        for pasture in range(101):
            print("Looping for pasture level: ", pasture)
            #loop by seed
            pasture_results = []

            for seed in range(self.batch_size):
                self.generator = Generator(seed)
                self.initiate()
                self.simulate(pasture, years)
                pasture_results.append(self.results[-1].marmots.sum())
                self.results = []
            
            positive_results = [result for result in pasture_results if result > 0]
            viability = len(positive_results)/len(pasture_results)
            mean_population = sum(positive_results)/max(len(positive_results), 1)
            self.batch_results.append([pasture, viability, mean_population])