import unittest

class TestIsPrime(unittest.TestCase):

    def test_func(self):
        result1 = is_prime(3)
        result2 = is_prime(6)
        self.assertTrue(result1)
        self.assertFalse(result2)

if __name__ == '__main__':
    unittest.main()