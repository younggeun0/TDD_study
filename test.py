import unittest

class Money:
    _amount = 0

    def __init__(self, amount):
        self._amount = amount

    def __eq__(self, money):
        return self._amount == money._amount

class Dollar(Money):
    def times(self, multiplier):
        return Dollar(self._amount * multiplier)


class Franc(Money):
    def times(self, multiplier):
        return Franc(self._amount * multiplier)



class TestMethods(unittest.TestCase):

    # 어떤 금액(주가)을 어떤 수(주식의 수)에 곱한 금액을 결과로 얻을 수 있어야 한다
    def test_multiplication(self):
        five = Dollar(5)
        
        self.assertEqual(Dollar(10), five.times(2))
        self.assertEqual(Dollar(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Dollar(5).__eq__(Dollar(5)))
        self.assertFalse(Dollar(5).__eq__(Dollar(6)))
        self.assertTrue(Franc(5).__eq__(Franc(5)))
        self.assertFalse(Franc(5).__eq__(Franc(6)))

    def test_franc_multiplication(self):
        five = Franc(5)
        
        self.assertEqual(Franc(10), five.times(2))
        self.assertEqual(Franc(15), five.times(3))


if __name__ == '__main__':
    unittest.main()
