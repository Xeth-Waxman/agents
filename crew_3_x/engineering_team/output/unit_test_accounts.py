import unittest
from accounts import Account

class TestAccount(unittest.TestCase):
    def test_init(self):
        account = Account('user1', 10000)
        self.assertEqual(account.user_id, 'user1')
        self.assertEqual(account.initial_deposit, 10000)
        self.assertEqual(account.balance, 10000)
        self.assertEqual(account.portfolio, {})
        self.assertEqual(account.transaction_history, [])

    def test_deposit_funds(self):
        account = Account('user1', 10000)
        account.deposit_funds(5000)
        self.assertEqual(account.balance, 15000)
        self.assertEqual(len(account.transaction_history), 1)
        self.assertEqual(account.transaction_history[0]['type'], 'deposit')
        self.assertEqual(account.transaction_history[0]['amount'], 5000)

    def test_withdraw_funds(self):
        account = Account('user1', 10000)
        account.withdraw_funds(2000)
        self.assertEqual(account.balance, 8000)
        self.assertEqual(len(account.transaction_history), 1)
        self.assertEqual(account.transaction_history[0]['type'], 'withdrawal')
        self.assertEqual(account.transaction_history[0]['amount'], 2000)

    def test_buy_shares(self):
        account = Account('user1', 10000)
        account.buy_shares('AAPL', 10)
        self.assertEqual(account.balance, 8500)
        self.assertEqual(len(account.transaction_history), 1)
        self.assertEqual(account.transaction_history[0]['type'], 'buy')
        self.assertEqual(account.transaction_history[0]['symbol'], 'AAPL')
        self.assertEqual(account.transaction_history[0]['quantity'], 10)
        self.assertEqual(account.transaction_history[0]['price'], 150)
        self.assertEqual(account.portfolio['AAPL'], 10)

    def test_sell_shares(self):
        account = Account('user1', 10000)
        account.buy_shares('AAPL', 10)
        account.sell_shares('AAPL', 5)
        self.assertEqual(account.balance, 9250)
        self.assertEqual(len(account.transaction_history), 2)
        self.assertEqual(account.transaction_history[1]['type'], 'sell')
        self.assertEqual(account.transaction_history[1]['symbol'], 'AAPL')
        self.assertEqual(account.transaction_history[1]['quantity'], 5)
        self.assertEqual(account.transaction_history[1]['price'], 150)
        self.assertEqual(account.portfolio['AAPL'], 5)

    def test_calculate_portfolio_value(self):
        account = Account('user1', 10000)
        account.buy_shares('AAPL', 10)
        self.assertEqual(account.calculate_portfolio_value(), 1500)

    def test_calculate_profit_loss(self):
        account = Account('user1', 10000)
        account.buy_shares('AAPL', 10)
        self.assertEqual(account.calculate_profit_loss(), 500)

    def test_get_holdings(self):
        account = Account('user1', 10000)
        account.buy_shares('AAPL', 10)
        self.assertEqual(account.get_holdings(), {'AAPL': 10})

    def test_get_transaction_history(self):
        account = Account('user1', 10000)
        account.deposit_funds(5000)
        account.withdraw_funds(2000)
        account.buy_shares('AAPL', 10)
        self.assertEqual(len(account.get_transaction_history()), 3)

    def test_get_account_balance(self):
        account = Account('user1', 10000)
        self.assertEqual(account.get_account_balance(), 10000)

    def test_get_share_price(self):
        account = Account('user1', 10000)
        self.assertEqual(account.get_share_price('AAPL'), 150)

if __name__ == '__main__':
    unittest.main()