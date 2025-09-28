# accounts.py - Trading Simulation Account Management System

from datetime import datetime
from typing import Optional, Dict, List, Tuple
from enum import Enum


class TransactionType(Enum):
    """Enumeration for different types of transactions."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BUY = "buy"
    SELL = "sell"


def get_share_price(symbol: str) -> float:
    """Returns the current price of a share for a given stock symbol.
    
    This is a test implementation that returns fixed prices for specific symbols.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
        
    Returns:
        The current price of the share
        
    Raises:
        ValueError: If the symbol is not recognized
    """
    prices = {
        'AAPL': 150.00,
        'TSLA': 250.00,
        'GOOGL': 2800.00
    }
    
    if symbol not in prices:
        raise ValueError(f"Unknown stock symbol: {symbol}")
    
    return prices[symbol]


class Account:
    """Manages user accounts for the trading simulation platform.
    
    This class handles all account operations including deposits, withdrawals,
    share trading, and portfolio tracking.
    """
    
    def __init__(self, initial_deposit: float = 0.0):
        """Initializes a new account with an optional initial deposit.
        
        Args:
            initial_deposit: The initial amount to deposit (default: 0.0)
            
        Raises:
            ValueError: If initial deposit is negative
        """
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        
        self._cash_balance = initial_deposit
        self._initial_deposit = initial_deposit
        self._holdings = {}  # {symbol: quantity}
        self._transactions = []  # List of transaction records
        
        if initial_deposit > 0:
            self._record_transaction(
                TransactionType.DEPOSIT,
                amount=initial_deposit
            )
    
    def _record_transaction(self, transaction_type: TransactionType, 
                          amount: float = None, symbol: str = None, 
                          quantity: int = None, price: float = None):
        """Records a transaction in the transaction history.
        
        Args:
            transaction_type: Type of transaction
            amount: Amount of money (for deposits/withdrawals)
            symbol: Stock symbol (for buy/sell)
            quantity: Number of shares (for buy/sell)
            price: Price per share (for buy/sell)
        """
        transaction = {
            'timestamp': datetime.now(),
            'type': transaction_type.value,
            'amount': amount,
            'symbol': symbol,
            'quantity': quantity,
            'price': price
        }
        self._transactions.append(transaction)
    
    def deposit_funds(self, amount: float):
        """Adds funds to the user's account.
        
        Args:
            amount: The amount to deposit
            
        Raises:
            ValueError: If the amount is not positive
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._cash_balance += amount
        self._record_transaction(TransactionType.DEPOSIT, amount=amount)
    
    def withdraw_funds(self, amount: float):
        """Withdraws funds from the user's account.
        
        Args:
            amount: The amount to withdraw
            
        Raises:
            ValueError: If the amount is not positive or would result in negative balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self._cash_balance:
            raise ValueError(f"Insufficient funds. Available balance: ${self._cash_balance:.2f}")
        
        self._cash_balance -= amount
        self._record_transaction(TransactionType.WITHDRAWAL, amount=amount)
    
    def buy_shares(self, symbol: str, quantity: int):
        """Records the purchase of shares for a given stock symbol.
        
        Args:
            symbol: Stock symbol to buy
            quantity: Number of shares to buy
            
        Raises:
            ValueError: If quantity is not positive or insufficient funds
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Get current share price
        try:
            price = get_share_price(symbol)
        except ValueError as e:
            raise ValueError(str(e))
        
        total_cost = price * quantity
        
        # Check if user has sufficient funds
        if total_cost > self._cash_balance:
            raise ValueError(f"Insufficient funds to buy {quantity} shares of {symbol}. " 
                           f"Required: ${total_cost:.2f}, Available: ${self._cash_balance:.2f}")
        
        # Execute the purchase
        self._cash_balance -= total_cost
        
        # Update holdings
        if symbol not in self._holdings:
            self._holdings[symbol] = 0
        self._holdings[symbol] += quantity
        
        # Record transaction
        self._record_transaction(
            TransactionType.BUY,
            amount=total_cost,
            symbol=symbol,
            quantity=quantity,
            price=price
        )
    
    def sell_shares(self, symbol: str, quantity: int):
        """Records the sale of shares for a given stock symbol.
        
        Args:
            symbol: Stock symbol to sell
            quantity: Number of shares to sell
            
        Raises:
            ValueError: If quantity is not positive or insufficient shares
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Check if user has the shares to sell
        if symbol not in self._holdings or self._holdings[symbol] < quantity:
            current_holdings = self._holdings.get(symbol, 0)
            raise ValueError(f"Insufficient shares to sell. You have {current_holdings} shares of {symbol}")
        
        # Get current share price
        try:
            price = get_share_price(symbol)
        except ValueError as e:
            raise ValueError(str(e))
        
        total_revenue = price * quantity
        
        # Execute the sale
        self._cash_balance += total_revenue
        self._holdings[symbol] -= quantity
        
        # Remove symbol from holdings if quantity becomes 0
        if self._holdings[symbol] == 0:
            del self._holdings[symbol]
        
        # Record transaction
        self._record_transaction(
            TransactionType.SELL,
            amount=total_revenue,
            symbol=symbol,
            quantity=quantity,
            price=price
        )
    
    def calculate_portfolio_value(self) -> float:
        """Calculates the total value of the user's portfolio.
        
        Returns:
            The total value including cash and all stock holdings
        """
        total_value = self._cash_balance
        
        for symbol, quantity in self._holdings.items():
            try:
                price = get_share_price(symbol)
                total_value += price * quantity
            except ValueError:
                # Skip unknown symbols in portfolio calculation
                pass
        
        return total_value
    
    def calculate_profit_loss(self) -> float:
        """Calculates the profit or loss compared to the initial deposit.
        
        Returns:
            The profit (positive) or loss (negative) amount
        """
        current_value = self.calculate_portfolio_value()
        
        # Calculate total deposits (initial + any additional deposits - withdrawals)
        total_deposits = 0
        for transaction in self._transactions:
            if transaction['type'] == TransactionType.DEPOSIT.value:
                total_deposits += transaction['amount']
            elif transaction['type'] == TransactionType.WITHDRAWAL.value:
                total_deposits -= transaction['amount']
        
        return current_value - total_deposits
    
    def get_holdings(self) -> Dict[str, int]:
        """Returns the user's current stock holdings.
        
        Returns:
            Dictionary with stock symbols as keys and share quantities as values
        """
        return self._holdings.copy()
    
    def get_transactions(self) -> List[Dict]:
        """Returns a list of all transactions made by the user.
        
        Returns:
            List of transaction dictionaries
        """
        return self._transactions.copy()
    
    def report_profit_loss(self, timestamp: Optional[datetime] = None) -> float:
        """Reports the profit or loss of the user at the specified time.
        
        Args:
            timestamp: The point in time to calculate profit/loss (default: current time)
            
        Returns:
            The profit or loss at the specified time
        """
        if timestamp is None:
            # Use current profit/loss
            return self.calculate_profit_loss()
        
        # Calculate profit/loss at a specific point in time
        # Reconstruct the state at that timestamp
        cash = 0
        holdings = {}
        total_deposits = 0
        
        for transaction in self._transactions:
            if transaction['timestamp'] > timestamp:
                break
            
            if transaction['type'] == TransactionType.DEPOSIT.value:
                cash += transaction['amount']
                total_deposits += transaction['amount']
            elif transaction['type'] == TransactionType.WITHDRAWAL.value:
                cash -= transaction['amount']
                total_deposits -= transaction['amount']
            elif transaction['type'] == TransactionType.BUY.value:
                cash -= transaction['amount']
                symbol = transaction['symbol']
                if symbol not in holdings:
                    holdings[symbol] = 0
                holdings[symbol] += transaction['quantity']
            elif transaction['type'] == TransactionType.SELL.value:
                cash += transaction['amount']
                symbol = transaction['symbol']
                holdings[symbol] -= transaction['quantity']
                if holdings[symbol] == 0:
                    del holdings[symbol]
        
        # Calculate portfolio value at that time
        portfolio_value = cash
        for symbol, quantity in holdings.items():
            try:
                price = get_share_price(symbol)
                portfolio_value += price * quantity
            except ValueError:
                pass
        
        return portfolio_value - total_deposits
    
    @property
    def cash_balance(self) -> float:
        """Returns the current cash balance."""
        return self._cash_balance
    
    @property
    def initial_deposit(self) -> float:
        """Returns the initial deposit amount."""
        return self._initial_deposit