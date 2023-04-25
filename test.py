import unittest

class Dollar:
    amount = 0

    def __init__(self, amount):
        self.amount = amount

    def times(self, multiplier):
        self.amount *= multiplier


class TestMethods(unittest.TestCase):

    # 어떤 금액(주가)을 어떤 수(주식의 수)에 곱한 금액을 결과로 얻을 수 있어야 한다
    def test_multiplication(self):
        five = Dollar(5)
        five.times(2)
        self.assertEqual(10, five.amount)


if __name__ == '__main__':
    unittest.main()
