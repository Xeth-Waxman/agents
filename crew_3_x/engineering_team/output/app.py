import gradio as gr
import accounts  # Assuming the Account class is in accounts.py

# Create a global account instance
account = accounts.Account('user1', 10000)

def create_deposit_fn(amount):
    """Handle deposit functionality"""
    try:
        amount = float(amount)
        account.deposit_funds(amount)
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.get_account_balance():.2f}"
    except ValueError:
        return "Please enter a valid number"

def create_withdrawal_fn(amount):
    """Handle withdrawal functionality"""
    try:
        amount = float(amount)
        if account.withdraw_funds(amount):
            return f"Successfully withdrew ${amount:.2f}. New balance: ${account.get_account_balance():.2f}"
        else:
            return "Insufficient funds for withdrawal"
    except ValueError:
        return "Please enter a valid number"

def create_buy_shares_fn(symbol, quantity):
    """Handle buying shares"""
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        price = account.get_share_price(symbol)
        
        if account.buy_shares(symbol, quantity):
            total_cost = price * quantity
            return f"Bought {quantity} shares of {symbol} at ${price:.2f} per share. Total cost: ${total_cost:.2f}"
        else:
            return "Unable to buy shares. Check balance or symbol."
    except ValueError:
        return "Please enter a valid quantity"

def create_sell_shares_fn(symbol, quantity):
    """Handle selling shares"""
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        price = account.get_share_price(symbol)
        
        if account.sell_shares(symbol, quantity):
            total_revenue = price * quantity
            return f"Sold {quantity} shares of {symbol} at ${price:.2f} per share. Total revenue: ${total_revenue:.2f}"
        else:
            return "Unable to sell shares. Check holdings or symbol."
    except ValueError:
        return "Please enter a valid quantity"

def get_account_summary():
    """Generate comprehensive account summary"""
    balance = account.get_account_balance()
    portfolio_value = account.calculate_portfolio_value()
    profit_loss = account.calculate_profit_loss()
    holdings = account.get_holdings()
    
    summary = f"Account Balance: ${balance:.2f}\n"
    summary += f"Portfolio Value: ${portfolio_value:.2f}\n"
    summary += f"Total Profit/Loss: ${profit_loss:.2f}\n\n"
    summary += "Current Holdings:\n"
    
    for symbol, qty in holdings.items():
        price = account.get_share_price(symbol)
        summary += f"{symbol}: {qty} shares at ${price:.2f} each\n"
    
    return summary

def get_transaction_history_fn():
    """Retrieve and format transaction history"""
    history = account.get_transaction_history()
    formatted_history = []
    for transaction in history:
        if transaction['type'] == 'deposit':
            formatted_history.append(f"Deposit: ${transaction['amount']:.2f}")
        elif transaction['type'] == 'withdrawal':
            formatted_history.append(f"Withdrawal: ${transaction['amount']:.2f}")
        elif transaction['type'] == 'buy':
            formatted_history.append(f"Buy: {transaction['quantity']} {transaction['symbol']} @ ${transaction['price']:.2f}")
        elif transaction['type'] == 'sell':
            formatted_history.append(f"Sell: {transaction['quantity']} {transaction['symbol']} @ ${transaction['price']:.2f}")
    
    return "\n".join(formatted_history)

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        with gr.Row():
            deposit_input = gr.Textbox(label="Deposit Amount")
            deposit_btn = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Deposit Result")
        
        with gr.Row():
            withdraw_input = gr.Textbox(label="Withdrawal Amount")
            withdraw_btn = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Withdrawal Result")
    
    with gr.Tab("Trading"):
        with gr.Row():
            buy_symbol = gr.Textbox(label="Buy Symbol (AAPL, TSLA, GOOGL)")
            buy_quantity = gr.Textbox(label="Quantity")
            buy_btn = gr.Button("Buy Shares")
            buy_output = gr.Textbox(label="Buy Result")
        
        with gr.Row():
            sell_symbol = gr.Textbox(label="Sell Symbol")
            sell_quantity = gr.Textbox(label="Quantity")
            sell_btn = gr.Button("Sell Shares")
            sell_output = gr.Textbox(label="Sell Result")
    
    with gr.Tab("Reports"):
        summary_btn = gr.Button("Get Account Summary")
        summary_output = gr.Textbox(label="Account Summary")
        
        history_btn = gr.Button("Transaction History")
        history_output = gr.Textbox(label="Transaction History")
    
    # Button Actions
    deposit_btn.click(create_deposit_fn, inputs=deposit_input, outputs=deposit_output)
    withdraw_btn.click(create_withdrawal_fn, inputs=withdraw_input, outputs=withdraw_output)
    buy_btn.click(create_buy_shares_fn, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
    sell_btn.click(create_sell_shares_fn, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    summary_btn.click(get_account_summary, outputs=summary_output)
    history_btn.click(get_transaction_history_fn, outputs=history_output)

# Launch the demo
if __name__ == "__main__":
    demo.launch()

