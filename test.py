import unittest


class Expresssion:
    pass

class Sum(Expresssion):
    augend = None
    addend = None

    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

class Money(Expresssion):
    _amount = 0
    _currency = ''

    def __init__(self, amount, currency):
        self._amount = amount
        self._currency = currency

    def __eq__(self, money):
        return self._amount == money._amount and self._currency == money._currency
    
    def times(self, multiplier):
        return Money(self._amount * multiplier, self._currency)
    
    def plus(self, addend):
        return Sum(self, addend)

    def currency(self):
        return self._currency

    @classmethod
    def dollar(cls, amount):
        return Money(amount, "USD")
    
    @classmethod
    def franc(cls, amount):
        return Money(amount, "CHF")

class Bank:
    def reduce(self, source, to):
        return Money.dollar(10)

class TestMethods(unittest.TestCase):

    # 어떤 금액(주가)을 어떤 수(주식의 수)에 곱한 금액을 결과로 얻을 수 있어야 한다
    def test_multiplication(self):
        five = Money.dollar(5)
        
        self.assertEqual(Money.dollar(10), five.times(2))
        self.assertEqual(Money.dollar(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Money.dollar(5).__eq__(Money.dollar(5)))
        self.assertFalse(Money.dollar(5).__eq__(Money.dollar(6)))
        self.assertFalse(Money.franc(5).__eq__(Money.dollar(5)))

    def test_franc_multiplication(self):
        five = Money.franc(5)
        
        self.assertEqual(Money.franc(10), five.times(2))
        self.assertEqual(Money.franc(15), five.times(3))

    def test_currency(self):
        self.assertEqual("USD", Money.dollar(1).currency())
        self.assertEqual("CHF", Money.franc(1).currency())

    def test_simple_addition(self):
        five = Money.dollar(5)
        sum = five.plus(five)
        bank = Bank()
        reduced = bank.reduce(sum, "USD")
        self.assertEqual(Money.dollar(10), reduced)

    def test_plus_return_sum(self):
        five = Money.dollar(5)
        result = five.plus(five)
        sum = result
        self.assertEqual(five, sum.augend)
        self.assertEqual(five, sum.addend)

if __name__ == '__main__':
    unittest.main()
