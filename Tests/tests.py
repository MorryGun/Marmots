import unittest
from generator import Generator

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

if __name__ == '__main__':
    unittest.main()