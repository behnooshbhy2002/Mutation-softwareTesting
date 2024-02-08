import unittest
class TestBMI(unittest.TestCase):
    def test_underweight(self):
        result = BMI(50, 1.7)
        self.assertEqual(result, "Underweight")

if __name__ == '__main__':
    unittest.main()