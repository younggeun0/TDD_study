import unittest

class Dollar:
    amount = 10

    def __init__(self, amount):
        pass

    def times(self, multiplier):
        pass


class TestMethods(unittest.TestCase):

    def test_multiplication(self):
        five = Dollar(5)
        five.times(2)
        self.assertEqual(10, five.amount)


if __name__ == '__main__':
    unittest.main()
