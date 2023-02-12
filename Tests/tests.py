import unittest
from generator import Generator
from simulator import Simulator

class Tests(unittest.TestCase):

    def test_random_generator_with_same_seed(self):
        generator1 = Generator(1)
        list1 = [generator1.random(), generator1.gauss(3, 2), generator1.uniform(2, 5), generator1.random()]

        generator2 = Generator(1)
        list2 = [generator2.random(), generator2.gauss(3, 2), generator2.uniform(2, 5), generator2.random()]

        self.assertEqual(list1, list2)


    def test_random_generator_with_different_seeds(self):
        generator1 = Generator(1)
        list1 = [generator1.random(), generator1.gauss(3, 2), generator1.uniform(2, 5), generator1.random()]

        generator2 = Generator(2)
        list2 = [generator2.random(), generator2.gauss(3, 2), generator2.uniform(2, 5), generator2.random()]

        self.assertNotEqual(list1, list2)

    
    def test_tiles_with_same_seed_are_equal(self):
        simulator1 = Simulator(1, 2, 2, [1, 100], [1,100], [1, 100])
        simulator1.initiate()
        tiles1 = simulator1.tiles
        
        productivity1 = [x[0].productivity for x in tiles1]
        fertility1 = [x[0].fertility for x in tiles1]

        simulator2 = Simulator(1, 2, 2, [1, 100], [1,100], [1, 100])
        simulator2.initiate()
        tiles2 = simulator2.tiles

        productivity2 = [x[0].productivity for x in tiles2]
        fertility2 = [x[0].fertility for x in tiles2]

        self.assertEqual(productivity1, productivity2)
        self.assertEqual(fertility1, fertility2)


    def test_tiles_with_different_seed_are_not_equal(self):
        simulator1 = Simulator(1, 2, 2, [1, 100], [1,100], [1, 100])
        simulator1.initiate()
        tiles1 = simulator1.tiles

        productivity1 = [x[0].productivity for x in tiles1]
        fertility1 = [x[0].fertility for x in tiles1]

        simulator2 = Simulator(2, 2, 2, [1, 100], [1,100], [1, 100])
        simulator2.initiate()
        tiles2 = simulator2.tiles

        productivity2 = [x[0].productivity for x in tiles2]
        fertility2 = [x[0].fertility for x in tiles2]

        self.assertNotEqual(productivity1, productivity2)
        self.assertNotEqual(fertility1, fertility2)


if __name__ == '__main__':
    unittest.main()