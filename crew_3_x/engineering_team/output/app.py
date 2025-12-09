import gradio as gr
from accounts import Account, get_share_price
from datetime import datetime

# Initialize a single account for the demo
account = None

def create_account(initial_deposit):
    """Create a new account with initial deposit."""
    global account
    try:
        if initial_deposit <= 0:
            return "Error: Initial deposit must be positive", "", ""
        account = Account("USER001", float(initial_deposit))
        return (
            f"✅ Account created successfully with initial deposit of ${initial_deposit:.2f}",
            get_account_summary(),
            get_holdings_display()
        )
    except Exception as e:
        return f"❌ Error: {str(e)}", "", ""

def deposit_funds(amount):
    """Deposit funds to the account."""
    global account
    if account is None:
        return "❌ Please create an account first", "", ""
    try:
        account.deposit_funds(float(amount))
        return (
            f"✅ Successfully deposited ${amount:.2f}",
            get_account_summary(),
            get_holdings_display()
        )
    except Exception as e:
        return f"❌ Error: {str(e)}", get_account_summary(), get_holdings_display()

def withdraw_funds(amount):
    """Withdraw funds from the account."""
    global account
    if account is None:
        return "❌ Please create an account first", "", ""
    try:
        account.withdraw_funds(float(amount))
        return (
            f"✅ Successfully withdrew ${amount:.2f}",
            get_account_summary(),
            get_holdings_display()
        )
    except Exception as e:
        return f"❌ Error: {str(e)}", get_account_summary(), get_holdings_display()

def buy_shares(symbol, quantity):
    """Buy shares of a stock."""
    global account
    if account is None:
        return "❌ Please create an account first", "", ""
    try:
        account.buy_shares(symbol.upper(), int(quantity))
        return (
            f"✅ Successfully bought {quantity} shares of {symbol.upper()}",
            get_account_summary(),
            get_holdings_display()
        )
    except Exception as e:
        return f"❌ Error: {str(e)}", get_account_summary(), get_holdings_display()

def sell_shares(symbol, quantity):
    """Sell shares of a stock."""
    global account
    if account is None:
        return "❌ Please create an account first", "", ""
    try:
        account.sell_shares(symbol.upper(), int(quantity))
        return (
            f"✅ Successfully sold {quantity} shares of {symbol.upper()}",
            get_account_summary(),
            get_holdings_display()
        )
    except Exception as e:
        return f"❌ Error: {str(e)}", get_account_summary(), get_holdings_display()

def get_account_summary():
    """Get account summary information."""
    if account is None:
        return "No account created yet"
    
    report = account.report_profit_or_loss()
    summary = f"""
**Account Summary**
- Cash Balance: ${report['cash_balance']:.2f}
- Portfolio Value: ${report['portfolio_value']:.2f}
- Total Value: ${report['total_value']:.2f}
- Initial Deposit: ${report['initial_deposit']:.2f}
- Profit/Loss: ${report['profit_or_loss']:.2f} ({report['return_percentage']:.2f}%)
"""
    return summary

def get_holdings_display():
    """Get current holdings display."""
    if account is None:
        return "No account created yet"
    
    holdings = account.report_holdings()
    if not holdings:
        return "**Current Holdings**\nNo stocks owned"
    
    holdings_text = "**Current Holdings**\n"
    for symbol, details in holdings.items():
        holdings_text += f"- {symbol}: {details['quantity']} shares @ ${details['current_price']:.2f} = ${details['total_value']:.2f}\n"
    
    return holdings_text

def get_transactions_history():
    """Get transaction history."""
    if account is None:
        return "No account created yet"
    
    transactions = account.list_transactions()
    if not transactions:
        return "No transactions yet"
    
    history = "**Transaction History**\n\n"
    for i, trans in enumerate(transactions, 1):
        timestamp = trans['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        history += f"{i}. [{timestamp}] {trans['description']}\n"
    
    return history

def get_stock_prices():
    """Display available stock prices."""
    return """
**Available Stocks and Prices**
- AAPL: $150.00
- TSLA: $700.00
- GOOGL: $2,800.00
"""

# Create Gradio interface
with gr.Blocks(title="Trading Account Simulator") as app:
    gr.Markdown("# Trading Account Simulator")
    gr.Markdown("A simple trading simulation platform to manage your portfolio")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Account Setup")
            initial_deposit = gr.Number(label="Initial Deposit ($)", value=10000)
            create_btn = gr.Button("Create Account", variant="primary")
            
            gr.Markdown("## Fund Management")
            deposit_amount = gr.Number(label="Deposit Amount ($)", value=1000)
            deposit_btn = gr.Button("Deposit Funds")
            
            withdraw_amount = gr.Number(label="Withdraw Amount ($)", value=500)
            withdraw_btn = gr.Button("Withdraw Funds")
            
        with gr.Column():
            gr.Markdown("## Trading")
            stock_prices_display = gr.Markdown(get_stock_prices())
            
            with gr.Row():
                buy_symbol = gr.Dropdown(
                    choices=["AAPL", "TSLA", "GOOGL"],
                    label="Buy Stock Symbol",
                    value="AAPL"
                )
                buy_quantity = gr.Number(label="Quantity", value=10, precision=0)
            buy_btn = gr.Button("Buy Shares", variant="primary")
            
            with gr.Row():
                sell_symbol = gr.Dropdown(
                    choices=["AAPL", "TSLA", "GOOGL"],
                    label="Sell Stock Symbol",
                    value="AAPL"
                )
                sell_quantity = gr.Number(label="Quantity", value=5, precision=0)
            sell_btn = gr.Button("Sell Shares", variant="stop")
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            account_summary = gr.Markdown("**Account Summary**\nNo account created yet")
            holdings_display = gr.Markdown("**Current Holdings**\nNo account created yet")
        
        with gr.Column():
            status_message = gr.Textbox(label="Status", lines=2, interactive=False)
            refresh_btn = gr.Button("Refresh Transaction History")
            transactions_display = gr.Markdown("**Transaction History**\nNo account created yet")
    
    # Connect buttons to functions
    create_btn.click(
        fn=create_account,
        inputs=[initial_deposit],
        outputs=[status_message, account_summary, holdings_display]
    )
    
    deposit_btn.click(
        fn=deposit_funds,
        inputs=[deposit_amount],
        outputs=[status_message, account_summary, holdings_display]
    )
    
    withdraw_btn.click(
        fn=withdraw_funds,
        inputs=[withdraw_amount],
        outputs=[status_message, account_summary, holdings_display]
    )
    
    buy_btn.click(
        fn=buy_shares,
        inputs=[buy_symbol, buy_quantity],
        outputs=[status_message, account_summary, holdings_display]
    )
    
    sell_btn.click(
        fn=sell_shares,
        inputs=[sell_symbol, sell_quantity],
        outputs=[status_message, account_summary, holdings_display]
    )
    
    refresh_btn.click(
        fn=get_transactions_history,
        inputs=[],
        outputs=[transactions_display]
    )

if __name__ == "__main__":
    app.launch()