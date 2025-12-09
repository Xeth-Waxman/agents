import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def test_get_share_price(self):
        self.assertEqual(get_share_price('AAPL'), 150.0)
        self.assertEqual(get_share_price('TSLA'), 700.0)
        self.assertEqual(get_share_price('GOOGL'), 2800.0)
        with self.assertRaises(ValueError):
            get_share_price('Unknown')

    def test_account_initialization(self):
        account = Account('ID123', 1000.0)
        self.assertEqual(account.account_id, 'ID123')
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.initial_deposit, 1000.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(len(account.transaction_history), 1)
        with self.assertRaises(ValueError):
            Account('ID123', -100.0)

    def test_deposit_funds(self):
        account = Account('ID123', 1000.0)
        account.deposit_funds(500.0)
        self.assertEqual(account.balance, 1500.0)
        self.assertEqual(account.initial_deposit, 1500.0)
        self.assertEqual(len(account.transaction_history), 2)
        with self.assertRaises(ValueError):
            account.deposit_funds(-100.0)

    def test_withdraw_funds(self):
        account = Account('ID123', 1000.0)
        account.withdraw_funds(500.0)
        self.assertEqual(account.balance, 500.0)
        self.assertEqual(len(account.transaction_history), 2)
        with self.assertRaises(ValueError):
            account.withdraw_funds(-100.0)
        with self.assertRaises(ValueError):
            account.withdraw_funds(1000.0)

    def test_buy_shares(self):
        account = Account('ID123', 1000.0)
        account.buy_shares('AAPL', 5)
        self.assertEqual(account.balance, 1000.0 - 5 * 150.0)
        self.assertEqual(account.holdings['AAPL'], 5)
        self.assertEqual(len(account.transaction_history), 2)
        with self.assertRaises(ValueError):
            account.buy_shares('Unknown', 5)
        with self.assertRaises(ValueError):
            account.buy_shares('AAPL', -5)
        with self.assertRaises(ValueError):
            account.buy_shares('AAPL', 100)

    def test_sell_shares(self):
        account = Account('ID123', 1000.0)
        account.buy_shares('AAPL', 5)
        account.sell_shares('AAPL', 5)
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(len(account.transaction_history), 3)
        with self.assertRaises(ValueError):
            account.sell_shares('Unknown', 5)
        with self.assertRaises(ValueError):
            account.sell_shares('AAPL', -5)
        with self.assertRaises(ValueError):
            account.sell_shares('AAPL', 10)

    def test_calculate_portfolio_value(self):
        account = Account('ID123', 1000.0)
        account.buy_shares('AAPL', 5)
        self.assertEqual(account.calculate_portfolio_value(), 5 * 150.0)

    def test_calculate_profit_or_loss(self):
        account = Account('ID123', 1000.0)
        account.buy_shares('AAPL', 5)
        self.assertEqual(account.calculate_profit_or_loss(), 5 * 150.0)

    def test_report_holdings(self):
        account = Account('ID123', 1000.0)
        account.buy_shares('AAPL', 5)
        self.assertEqual(account.report_holdings(), {'AAPL': {'quantity': 5, 'current_price': 150.0, 'total_value': 750.0}})

    def test_report_profit_or_loss(self):
        account = Account('ID123', 1000.0)
        account.buy_shares('AAPL', 5)
        self.assertEqual(account.report_profit_or_loss(), {'cash_balance': 1000.0 - 5 * 150.0, 'portfolio_value': 750.0, 'total_value': 1000.0 - 5 * 150.0 + 750.0, 'initial_deposit': 1000.0, 'profit_or_loss': 0.0, 'return_percentage': 0.0})

    def test_list_transactions(self):
        account = Account('ID123', 1000.0)
        account.deposit_funds(500.0)
        account.withdraw_funds(200.0)
        account.buy_shares('AAPL', 5)
        account.sell_shares('AAPL', 5)
        self.assertEqual(len(account.list_transactions()), 5)

if __name__ == '__main__':
    unittest.main()