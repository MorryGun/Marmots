import numpy as np
import uuid

from generator import Generator


class Tile:
    def __init__(self, coordinates, tile_productivity, marmots_fertility, generator : Generator): 
        self.id = uuid.uuid4()
        self.coordinates = coordinates
        self.productivity = round(generator.uniform(tile_productivity[0], tile_productivity[1]))
        self.fertility = round(generator.uniform(marmots_fertility[0], marmots_fertility[1]))
        self.vegetation = self.productivity
        self.population = self.fertility
        self.neighbors = []
        self.pasture = 0

    
    def set_neighbors(self, tiles):
        indices = self.get_neighbor_indices(tiles, self.coordinates[0], self.coordinates[1])
        ids = [tiles[vector[1]-1, vector[0]-1].id for vector in indices]

        self.neighbors = ids


    def get_neighbor_indices(self, tiles : np.ndarray, column_number : int, row_number : int):
        indices = []

        for x in range(column_number-1, column_number+2):
            for y in range(row_number-1, row_number+2):
                if x > 0 and y > 0 and (x != self.coordinates[0] or y != self.coordinates[1]) and x <= tiles.shape[1] and y <= tiles.shape[0]:
                    indices.append([x, y])

        return indices