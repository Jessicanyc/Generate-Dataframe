import unittest
from data_generator import generate_string, generate_integer, generate_float, generate_array_float, generate_array_string

class TestDataGenerator(unittest.TestCase):

    def test_generate_string(self):
        # Testing string generation with specific length
        result = generate_string({'fixed_length': 5}, 'random')
        self.assertEqual(len(result), 5)

        # Testing string generation with default length
        result = generate_string(None, 'random')
        self.assertEqual(len(result), 10)

    def test_generate_integer(self):
        # Testing integer generation within a range
        result = generate_integer([10, 20], None)
        self.assertTrue(10 <= result <= 20)

        # Testing integer generation with default range
        result = generate_integer(None, None)
        self.assertTrue(0 <= result <= 100)

    def test_generate_float(self):
        # Testing float generation with specific precision
        result = generate_float(2, None)
        self.assertTrue(isinstance(result, float))
        self.assertTrue(0 <= result <= 100)
