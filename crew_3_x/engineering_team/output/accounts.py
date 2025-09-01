import json

class Account:
    def __init__(self, user_id: str, initial_deposit: float):
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.portfolio = {}
        self.transaction_history = []
        self.test_share_prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}

    def deposit_funds(self, amount: float) -> None:
        self.balance += amount
        self.transaction_history.append({'type': 'deposit', 'amount': amount})

    def withdraw_funds(self, amount: float) -> bool:
        if amount > self.balance:
            return False
        self.balance -= amount
        self.transaction_history.append({'type': 'withdrawal', 'amount': amount})
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        share_price = self.test_share_prices.get(symbol)
        if share_price is None:
            return False
        cost = share_price * quantity
        if cost > self.balance:
            return False
        self.balance -= cost
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity
        self.transaction_history.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': share_price})
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            return False
        share_price = self.test_share_prices.get(symbol)
        if share_price is None:
            return False
        revenue = share_price * quantity
        self.balance += revenue
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        self.transaction_history.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'price': share_price})
        return True

    def calculate_portfolio_value(self) -> float:
        value = 0
        for symbol, quantity in self.portfolio.items():
            share_price = self.test_share_prices.get(symbol)
            if share_price is not None:
                value += share_price * quantity
        return value

    def calculate_profit_loss(self) -> float:
        return self.calculate_portfolio_value() + self.balance - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.portfolio

    def get_transaction_history(self) -> list:
        return self.transaction_history

    def get_account_balance(self) -> float:
        return self.balance

    def get_share_price(self, symbol: str) -> float:
        return self.test_share_prices.get(symbol, 0)

# Test the class
account = Account('user1', 10000)
print(account.get_account_balance())
account.deposit_funds(5000)
print(account.get_account_balance())
account.withdraw_funds(2000)
print(account.get_account_balance())
account.buy_shares('AAPL', 10)
print(account.get_holdings())
account.sell_shares('AAPL', 5)
print(account.get_holdings())
print(account.get_transaction_history())
print(account.calculate_portfolio_value())
print(account.calculate_profit_loss())