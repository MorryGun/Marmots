from random import Random


class Generator:
    def __init__(self, seed):
        self.randomGenerator = Random(seed)


    def random(self):
        return self.randomGenerator.random()


    def uniform(self, min, max):
        return self.randomGenerator.uniform(min, max)

    
    def gauss(self, mean, sigma):
        return self.randomGenerator.gauss(mean, sigma)

