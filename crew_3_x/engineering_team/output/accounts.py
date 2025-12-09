from datetime import datetime
from typing import Dict, List, Tuple, Optional

def get_share_price(symbol: str) -> float:
    """Retrieves the current price of a stock given its symbol.
    Test implementation returns fixed prices for AAPL, TSLA, and GOOGL.
    
    Args:
        symbol: Stock symbol to get price for
        
    Returns:
        Current price of the stock
        
    Raises:
        ValueError: If symbol is not recognized
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0
    }
    if symbol not in prices:
        raise ValueError(f"Unknown stock symbol: {symbol}")
    return prices[symbol]


class Account:
    """Represents a user's account, managing funds, transactions, and portfolio holdings."""
    
    def __init__(self, account_id: str, initial_deposit: float):
        """Initializes a new account with a unique account_id, sets initial deposit 
        and balance, and initializes holdings and transaction history.
        
        Args:
            account_id: Unique identifier for the account
            initial_deposit: Initial funds to deposit into the account
            
        Raises:
            ValueError: If initial_deposit is negative
        """
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
            
        self.account_id = account_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings: Dict[str, int] = {}
        self.transaction_history: List[Dict] = []
        
        # Record initial deposit as first transaction
        if initial_deposit > 0:
            self.transaction_history.append({
                'type': 'deposit',
                'amount': initial_deposit,
                'timestamp': datetime.now(),
                'description': 'Initial deposit'
            })
    
    def deposit_funds(self, amount: float):
        """Increases the account balance by the specified amount.
        Validates that the deposit amount is positive.
        
        Args:
            amount: Amount to deposit
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
            
        self.balance += amount
        self.initial_deposit += amount
        
        self.transaction_history.append({
            'type': 'deposit',
            'amount': amount,
            'timestamp': datetime.now(),
            'description': f'Deposit of ${amount:.2f}'
        })
    
    def withdraw_funds(self, amount: float):
        """Decreases the account balance by the specified amount, if sufficient funds exist.
        Prevents withdrawal resulting in negative balance.
        
        Args:
            amount: Amount to withdraw
            
        Raises:
            ValueError: If amount is not positive or would result in negative balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
            
        if self.balance - amount < 0:
            raise ValueError(f"Insufficient funds. Available balance: ${self.balance:.2f}")
            
        self.balance -= amount
        
        self.transaction_history.append({
            'type': 'withdrawal',
            'amount': amount,
            'timestamp': datetime.now(),
            'description': f'Withdrawal of ${amount:.2f}'
        })
    
    def buy_shares(self, symbol: str, quantity: int):
        """Records the purchase of a specified quantity of shares for a given stock symbol.
        Updates holdings and decrements balance by the shares' total cost.
        Validates sufficient balance for the transaction.
        
        Args:
            symbol: Stock symbol to buy
            quantity: Number of shares to buy
            
        Raises:
            ValueError: If quantity is not positive or insufficient funds
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        
        if self.balance < total_cost:
            raise ValueError(f"Insufficient funds to buy {quantity} shares of {symbol}. " +
                           f"Cost: ${total_cost:.2f}, Available: ${self.balance:.2f}")
        
        self.balance -= total_cost
        
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
            
        self.transaction_history.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price_per_share': share_price,
            'total_cost': total_cost,
            'timestamp': datetime.now(),
            'description': f'Bought {quantity} shares of {symbol} at ${share_price:.2f}/share'
        })
    
    def sell_shares(self, symbol: str, quantity: int):
        """Records the sale of a specified quantity of shares for a given stock symbol.
        Updates holdings and increments balance by the shares' total sale value.
        Validates sufficient shares are owned for the transaction.
        
        Args:
            symbol: Stock symbol to sell
            quantity: Number of shares to sell
            
        Raises:
            ValueError: If quantity is not positive or insufficient shares owned
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            owned = self.holdings.get(symbol, 0)
            raise ValueError(f"Insufficient shares to sell. You own {owned} shares of {symbol}")
        
        share_price = get_share_price(symbol)
        total_sale_value = share_price * quantity
        
        self.balance += total_sale_value
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
            
        self.transaction_history.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price_per_share': share_price,
            'total_sale_value': total_sale_value,
            'timestamp': datetime.now(),
            'description': f'Sold {quantity} shares of {symbol} at ${share_price:.2f}/share'
        })
    
    def calculate_portfolio_value(self) -> float:
        """Calculates the total value of current holdings using get_share_price(symbol) 
        for each stock.
        
        Returns:
            Total value of all stock holdings
        """
        total_value = 0.0
        for symbol, quantity in self.holdings.items():
            share_price = get_share_price(symbol)
            total_value += share_price * quantity
        return total_value
    
    def calculate_profit_or_loss(self) -> float:
        """Calculates profit or loss as the difference between the current account value 
        (balance + portfolio value) and the initial deposit.
        
        Returns:
            Profit (positive) or loss (negative) amount
        """
        current_total_value = self.balance + self.calculate_portfolio_value()
        return current_total_value - self.initial_deposit
    
    def report_holdings(self) -> Dict[str, Dict]:
        """Returns a detailed report of all stock holdings and their respective quantities.
        
        Returns:
            Dictionary with stock symbols as keys and details as values
        """
        report = {}
        for symbol, quantity in self.holdings.items():
            share_price = get_share_price(symbol)
            report[symbol] = {
                'quantity': quantity,
                'current_price': share_price,
                'total_value': share_price * quantity
            }
        return report
    
    def report_profit_or_loss(self) -> Dict[str, float]:
        """Returns the current profit or loss calculated via calculate_profit_or_loss().
        
        Returns:
            Dictionary with detailed profit/loss information
        """
        portfolio_value = self.calculate_portfolio_value()
        total_value = self.balance + portfolio_value
        profit_or_loss = self.calculate_profit_or_loss()
        
        return {
            'cash_balance': self.balance,
            'portfolio_value': portfolio_value,
            'total_value': total_value,
            'initial_deposit': self.initial_deposit,
            'profit_or_loss': profit_or_loss,
            'return_percentage': (profit_or_loss / self.initial_deposit * 100) if self.initial_deposit > 0 else 0
        }
    
    def list_transactions(self) -> List[Dict]:
        """Provides a complete list of all transactions made by the account, 
        including deposits, withdrawals, and trades.
        
        Returns:
            List of transaction dictionaries in chronological order
        """
        return self.transaction_history.copy()