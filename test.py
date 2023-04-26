import unittest


class Pair():
    _from = None
    _to = None

    def __init__(self, _from, to):
        self._from = _from
        self._to = to

    def __eq__(self, pair):
        return self._from == pair._from and self._to == pair._to
    
    def __hash__(self):
        return 0

class Expresssion:
    def plus(self, addend):
        return Sum(self, addend)

    def reduce(self, source, to):
        return source.reduce(to)
    
    def times(self, multiplier):
        pass

class Sum(Expresssion):
    augend = None
    addend = None

    def plus(self, addend):
        return Sum(self, addend)

    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend
    
    def reduce(self, bank, to):
        amount = self.augend.reduce(bank, to)._amount + self.addend.reduce(bank, to)._amount
        return Money(amount, to)
    
    def times(self, multiplier):
        return Sum(self.augend.times(multiplier), self.addend.times(multiplier))

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
    
    def reduce(self, bank, to):
        rate = bank.rate(self._currency, to)
        return Money(self._amount / rate, to)

    @classmethod
    def dollar(cls, amount):
        return Money(amount, "USD")
    
    @classmethod
    def franc(cls, amount):
        return Money(amount, "CHF")

class Bank:
    rates = {}

    def rate(self, _from, to):
        if (_from == to):
            return 1

        rate = self.rates.get(Pair(_from, to))
        return rate

    def reduce(self, source, to):
        return source.reduce(self, to)
    
    def addRate(self, source, to, rate):
        self.rates[Pair(source, to)] = rate

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

    def test_reduce_sum(self):
        sum = Sum(Money.dollar(3), Money.dollar(4))
        bank = Bank()
        result = bank.reduce(sum, "USD")
        self.assertEqual(Money.dollar(7), result)

    def test_reduce_money(self):
        bank = Bank()
        result = bank.reduce(Money.dollar(1), "USD")
        self.assertEqual(Money.dollar(1), result)

    def test_reduce_money_difference_currency(self):
        bank = Bank()
        bank.addRate("CHF", "USD", 2)
        result = bank.reduce(Money.franc(2), "USD")
        self.assertEqual(Money.dollar(1), result)

    def test_identity_rate(self):
        self.assertEqual(1, Bank().rate("USD", "USD"))

    def test_mixed_addition(self):
        fiveBucks = Money.dollar(5)
        tenFrancs = Money.franc(10)
        bank = Bank()
        bank.addRate("CHF", "USD", 2)

        result = bank.reduce(fiveBucks.plus(tenFrancs), "USD")
        self.assertEqual(Money.dollar(10), result)

    def test_sum_plus_money(self):
        fiveBucks = Money.dollar(5)
        tenFrans = Money.franc(10)
        bank = Bank()
        bank.addRate("CHF", "USD", 2)
        sum = Sum(fiveBucks, tenFrans).plus(fiveBucks)
        result = bank.reduce(sum, "USD")
        self.assertEqual(Money.dollar(15), result)

    def test_sum_times(self):
        fiveBucks = Money.dollar(5)
        tenFrans = Money.franc(10)
        bank = Bank()
        bank.addRate("CHF", "USD", 2)
        sum = Sum(fiveBucks, tenFrans).times(2)
        result = bank.reduce(sum, "USD")
        self.assertEqual(Money.dollar(20), result)

if __name__ == '__main__':
    unittest.main()
