import unittest
from accounts import Account, TransactionType, get_share_price

class TestAccount(unittest.TestCase):
    def test_init(self):
        account = Account(1000)
        self.assertEqual(account.cash_balance, 1000)
        self.assertEqual(account.initial_deposit, 1000)

    def test_deposit(self):
        account = Account()
        account.deposit_funds(500)
        self.assertEqual(account.cash_balance, 500)

    def test_withdraw(self):
        account = Account(1000)
        account.withdraw_funds(500)
        self.assertEqual(account.cash_balance, 500)

    def test_buy_shares(self):
        account = Account(1000)
        account.buy_shares('AAPL', 2)
        self.assertEqual(account.cash_balance, 1000 - 300)
        self.assertEqual(account.get_holdings()['AAPL'], 2)

    def test_sell_shares(self):
        account = Account(1000)
        account.buy_shares('AAPL', 2)
        account.sell_shares('AAPL', 1)
        self.assertEqual(account.cash_balance, 1000 - 300 + 150)
        self.assertEqual(account.get_holdings()['AAPL'], 1)

    def test_get_holdings(self):
        account = Account()
        account.buy_shares('AAPL', 2)
        self.assertEqual(account.get_holdings(), {'AAPL': 2})

    def test_get_transactions(self):
        account = Account()
        account.deposit_funds(100)
        account.buy_shares('AAPL', 1)
        self.assertEqual(len(account.get_transactions()), 2)

    def test_calculate_portfolio_value(self):
        account = Account(1000)
        account.buy_shares('AAPL', 2)
        self.assertGreater(account.calculate_portfolio_value(), 1000)

    def test_calculate_profit_loss(self):
        account = Account(1000)
        account.buy_shares('AAPL', 2)
        self.assertGreater(account.calculate_profit_loss(), 0)

    def test_report_profit_loss(self):
        account = Account(1000)
        account.buy_shares('AAPL', 2)
        self.assertGreater(account.report_profit_loss(), 0)

    def test_get_share_price(self):
        self.assertEqual(get_share_price('AAPL'), 150.0)

    def test_invalid_symbol(self):
        with self.assertRaises(ValueError):
            get_share_price('UNKNOWN')

if __name__ == '__main__':
    unittest.main()