

import gradio as gr
from accounts import Account, get_share_price
from datetime import datetime

# Initialize a single account instance
account = Account()

def create_account_with_deposit(initial_deposit):
    """Creates a new account with initial deposit."""
    global account
    try:
        initial_deposit = float(initial_deposit)
        account = Account(initial_deposit)
        return f"✅ Account created with initial deposit: ${initial_deposit:.2f}", update_displays()
    except ValueError as e:
        return f"❌ Error: {str(e)}", update_displays()
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}", update_displays()

def deposit_funds(amount):
    """Deposits funds into the account."""
    try:
        amount = float(amount)
        account.deposit_funds(amount)
        return f"✅ Deposited ${amount:.2f} successfully", update_displays()
    except ValueError as e:
        return f"❌ Error: {str(e)}", update_displays()
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}", update_displays()

def withdraw_funds(amount):
    """Withdraws funds from the account."""
    try:
        amount = float(amount)
        account.withdraw_funds(amount)
        return f"✅ Withdrew ${amount:.2f} successfully", update_displays()
    except ValueError as e:
        return f"❌ Error: {str(e)}", update_displays()
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}", update_displays()

def buy_shares(symbol, quantity):
    """Buys shares of a given stock."""
    try:
        quantity = int(quantity)
        symbol = symbol.upper().strip()
        account.buy_shares(symbol, quantity)
        price = get_share_price(symbol)
        total_cost = price * quantity
        return f"✅ Bought {quantity} shares of {symbol} at ${price:.2f}/share (Total: ${total_cost:.2f})", update_displays()
    except ValueError as e:
        return f"❌ Error: {str(e)}", update_displays()
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}", update_displays()

def sell_shares(symbol, quantity):
    """Sells shares of a given stock."""
    try:
        quantity = int(quantity)
        symbol = symbol.upper().strip()
        account.sell_shares(symbol, quantity)
        price = get_share_price(symbol)
        total_revenue = price * quantity
        return f"✅ Sold {quantity} shares of {symbol} at ${price:.2f}/share (Total: ${total_revenue:.2f})", update_displays()
    except ValueError as e:
        return f"❌ Error: {str(e)}", update_displays()
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}", update_displays()

def update_displays():
    """Updates all display components."""
    return (
        get_account_summary(),
        get_holdings_display(),
        get_transactions_display()
    )

def get_account_summary():
    """Gets the account summary information."""
    try:
        cash_balance = account.cash_balance
        portfolio_value = account.calculate_portfolio_value()
        profit_loss = account.calculate_profit_loss()
        
        summary = f"""
### Account Summary
- **Cash Balance:** ${cash_balance:,.2f}
- **Portfolio Value:** ${portfolio_value:,.2f}
- **Profit/Loss:** ${profit_loss:+,.2f} {'📈' if profit_loss >= 0 else '📉'}
- **Return:** {(profit_loss / account.initial_deposit * 100) if account.initial_deposit > 0 else 0:.2f}%
"""
        return summary
    except Exception:
        return "### Account Summary\n*No account created yet*"

def get_holdings_display():
    """Gets the current holdings display."""
    try:
        holdings = account.get_holdings()
        if not holdings:
            return "### Current Holdings\n*No holdings*"
        
        holdings_text = "### Current Holdings\n"
        holdings_text += "| Symbol | Shares | Current Price | Total Value |\n"
        holdings_text += "|--------|--------|---------------|-------------|\n"
        
        total_value = 0
        for symbol, quantity in holdings.items():
            price = get_share_price(symbol)
            value = price * quantity
            total_value += value
            holdings_text += f"| {symbol} | {quantity} | ${price:.2f} | ${value:,.2f} |\n"
        
        holdings_text += f"\n**Total Holdings Value:** ${total_value:,.2f}"
        return holdings_text
    except Exception:
        return "### Current Holdings\n*No account created yet*"

def get_transactions_display():
    """Gets the transaction history display."""
    try:
        transactions = account.get_transactions()
        if not transactions:
            return "### Transaction History\n*No transactions*"
        
        trans_text = "### Transaction History (Most Recent First)\n"
        trans_text += "| Time | Type | Symbol | Quantity | Price | Amount |\n"
        trans_text += "|------|------|--------|----------|-------|--------|\n"
        
        # Show most recent transactions first
        for trans in reversed(transactions[-10:]):  # Show last 10 transactions
            time_str = trans['timestamp'].strftime("%H:%M:%S")
            type_str = trans['type'].capitalize()
            symbol = trans['symbol'] if trans['symbol'] else "-"
            quantity = str(trans['quantity']) if trans['quantity'] else "-"
            price = f"${trans['price']:.2f}" if trans['price'] else "-"
            amount = f"${trans['amount']:.2f}" if trans['amount'] else "-"
            
            trans_text += f"| {time_str} | {type_str} | {symbol} | {quantity} | {price} | {amount} |\n"
        
        if len(transactions) > 10:
            trans_text += f"\n*Showing last 10 of {len(transactions)} transactions*"
        
        return trans_text
    except Exception:
        return "### Transaction History\n*No account created yet*"

def get_stock_prices():
    """Gets current stock prices for display."""
    return """
### Available Stocks & Prices
- **AAPL** (Apple): $150.00
- **TSLA** (Tesla): $250.00
- **GOOGL** (Google): $2,800.00
"""

# Create the Gradio interface
with gr.Blocks(title="Trading Simulation Platform", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 📈 Trading Simulation Platform")
    gr.Markdown("Manage your virtual trading account, buy/sell stocks, and track your portfolio performance.")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Account Operations")
            
            with gr.Group():
                gr.Markdown("### Create/Reset Account")
                initial_deposit_input = gr.Number(label="Initial Deposit ($)", value=10000, minimum=0)
                create_account_btn = gr.Button("Create New Account", variant="primary")
            
            with gr.Group():
                gr.Markdown("### Deposit/Withdraw Funds")
                amount_input = gr.Number(label="Amount ($)", value=1000, minimum=0)
                with gr.Row():
                    deposit_btn = gr.Button("Deposit", variant="secondary")
                    withdraw_btn = gr.Button("Withdraw", variant="secondary")
            
            with gr.Group():
                gr.Markdown("### Trade Stocks")
                stock_prices_display = gr.Markdown(get_stock_prices())
                symbol_input = gr.Textbox(label="Stock Symbol", placeholder="e.g., AAPL", value="AAPL")
                quantity_input = gr.Number(label="Quantity", value=10, minimum=1, step=1)
                with gr.Row():
                    buy_btn = gr.Button("Buy Shares", variant="primary")
                    sell_btn = gr.Button("Sell Shares", variant="stop")
            
            status_output = gr.Markdown("*Ready to start trading*")
        
        with gr.Column(scale=2):
            gr.Markdown("## Portfolio Dashboard")
            
            with gr.Tab("Summary"):
                account_summary = gr.Markdown(get_account_summary())
            
            with gr.Tab("Holdings"):
                holdings_display = gr.Markdown(get_holdings_display())
            
            with gr.Tab("Transactions"):
                transactions_display = gr.Markdown(get_transactions_display())
            
            refresh_btn = gr.Button("🔄 Refresh Dashboard", variant="secondary")
    
    # Connect the buttons to their functions
    create_account_btn.click(
        create_account_with_deposit,
        inputs=[initial_deposit_input],
        outputs=[status_output, account_summary, holdings_display, transactions_display]
    )
    
    deposit_btn.click(
        deposit_funds,
        inputs=[amount_input],
        outputs=[status_output, account_summary, holdings_display, transactions_display]
    )
    
    withdraw_btn.click(
        withdraw_funds,
        inputs=[amount_input],
        outputs=[status_output, account_summary, holdings_display, transactions_display]
    )
    
    buy_btn.click(
        buy_shares,
        inputs=[symbol_input, quantity_input],
        outputs=[status_output, account_summary, holdings_display, transactions_display]
    )
    
    sell_btn.click(
        sell_shares,
        inputs=[symbol_input, quantity_input],
        outputs=[status_output, account_summary, holdings_display, transactions_display]
    )
    
    refresh_btn.click(
        lambda: ("Dashboard refreshed", *update_displays()),
        outputs=[status_output, account_summary, holdings_display, transactions_display]
    )
    
    # Initial load
    app.load(
        lambda: ("Welcome to Trading Simulation Platform!", *update_displays()),
        outputs=[status_output, account_summary, holdings_display, transactions_display]
    )

if __name__ == "__main__":
    app.launch(share=False, server_name="127.0.0.1", server_port=7860)