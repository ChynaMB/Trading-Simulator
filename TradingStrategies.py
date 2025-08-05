
from Stock import Stock
from Balance import Balance

class TradingStrategies:
    """
    A dedicated class for all trading strategies to keep the main simulation clean.
    Usage:
    1. Initialise with strategies dictionary
    2. Call apply() during simulation
    """
    def __init__(self, balance: Balance):
        self.balance = balance
        self.stock_take_profit = {}  # {ticker: {'threshold': float, 'active': bool}}
        self.stock_stop_loss = {}    # {ticker: {'threshold': float, 'active': bool}}
        self.stock_dollar_cost_avg = {}  # {ticker: {'cash': float, 'day_interval': int, 'active': bool}}

    def initialise_strategies(self, Stock):
        """Set strategies so that they are all neutral and innactive"""
        ticker = Stock.ticker
        self.stock_take_profit[ticker] = {'threshold': None, 'active': False}
        self.stock_stop_loss[ticker] = {'threshold': None, 'active': False}
        self.stock_dollar_cost_avg[ticker] = {'cash': None, 'day_interval': None, 'active': False}
        print(f"Strategies initialised for {ticker}: {self.stock_take_profit[ticker]}, {self.stock_stop_loss[ticker]}, {self.stock_dollar_cost_avg[ticker]}")


    def activate(self, stock, strategy_name: str):
        """Activate a strategy for a specific stock."""
        ticker = stock.get_ticker()
        if strategy_name == "take_profit":
            self.stock_take_profit[ticker]['active'] = True
        elif strategy_name == "stop_loss":
            self.stock_stop_loss[ticker]['active'] = True
        elif strategy_name == "dollar_cost_avg":
            self.stock_dollar_cost_avg[ticker]['active'] = True
        

    def deactivate(self, stock, strategy_name: str):
        """Deactivate a strategy for a specific stock."""
        ticker = stock.get_ticker()
        if strategy_name == "take_profit":
            self.stock_take_profit[ticker]['active'] = False
        elif strategy_name == "stop_loss":
            self.stock_stop_loss[ticker]['active'] = False
        elif strategy_name == "dollar_cost_avg":
            self.stock_dollar_cost_avg[ticker]['active'] = False
        

    def set_all_strategies(self, stock, configs:dict):
        """
        Access the configuration dictionary:
        "take_profit": threshold,
        "stop_loss": threshold,
        "dollar_cost_avg": [cash, day_interval]
        and use it to set all strategies (without activating or deactivating them)
        """
        ticker = stock.get_ticker()
        if "take_profit" in configs:
            self.stock_take_profit[ticker]['threshold'] = configs["take_profit"]
        if "stop_loss" in configs:
            self.stock_stop_loss[ticker]['threshold'] = configs["stop_loss"]
        if "dollar_cost_avg" in configs:
            self.stock_dollar_cost_avg[ticker]['cash'] = configs["dollar_cost_avg"]["cash"]
            self.stock_dollar_cost_avg[ticker]['day_interval'] = configs["dollar_cost_avg"]["day_interval"]

    def get_all_strategies(self, stock):
        """Get all strategies for a specific stock."""
        ticker = stock.get_ticker()
        return {
            "take_profit": self.stock_take_profit[ticker],
            "stop_loss": self.stock_stop_loss[ticker],
            "dollar_cost_avg": self.stock_dollar_cost_avg[ticker]
        }

    def get_active_strategies(self, stock):
        """Get all active strategies for a specific stock."""
        ticker = stock.get_ticker()
        return {
            "take_profit": self.stock_take_profit[ticker]['active'],
            "stop_loss": self.stock_stop_loss[ticker]['active'],
            "dollar_cost_avg": self.stock_dollar_cost_avg[ticker]['active']
        }

    def apply_strategies(self, stock, day_index: int):
        """Apply all active strategies to a stocks."""
        ticker = stock.get_ticker()
        if self.stock_take_profit[ticker]["active"]:
            profit_threshold:float = self.stock_take_profit[ticker]['threshold']
            if profit_threshold is None:
                raise ValueError("Profit threshold must be set before applying take profit strategy.")
            self.take_profit(stock, profit_threshold)
            print(f"Applied take profit strategy for {ticker} with threshold {profit_threshold}")

        if self.stock_stop_loss[ticker]["active"]:
            loss_threshold:float = self.stock_stop_loss[ticker]['threshold']
            if loss_threshold is None:
                raise ValueError("Loss threshold must be set before applying stop loss strategy.")
            self.stop_loss(stock, loss_threshold)
            print(f"Applied stop loss strategy for {ticker} with threshold {loss_threshold}")

        if self.stock_dollar_cost_avg[ticker]["active"]:
            cash:float = self.stock_dollar_cost_avg[ticker]["cash"]
            if cash is None:
                raise ValueError("Cash amount must be set before applying dollar cost averaging strategy.")
            day_interval:int = self.stock_dollar_cost_avg[ticker]["day_interval"]
            if day_interval is None:
                raise ValueError("Day interval must be set before applying dollar cost averaging strategy.")
            self.dollar_cost_avg(stock, cash, day_interval, day_index)
            print(f"Applied all strategies for {ticker} on day {day_index}")

        print(f"Applied all strategies for {ticker} on day {day_index}")
        
    def take_profit(self, stock, threshold:float) -> bool:
        """Take profit strategy: sell if profit exceeds threshold."""
        invested_cash = stock.get_cash_invested() - stock.get_cash_withdrawn()
        investment_value = stock.get_investment_value()
        profit = (investment_value - invested_cash)/invested_cash
        print(f"Profit for {stock.get_ticker()}: {profit}, Threshold: {threshold}")
        if threshold <= profit:
            print(f"Taking profit for {stock.get_ticker()}")
            return self.balance.sell(stock, stock.get_number_stocks())
        print(f"Profit for {stock.get_ticker()} does not exceed threshold. No action taken.")
        return False
            

    def stop_loss(self, stock, threshold:float)-> bool:
        """Stop loss strategy: sell if investment loss drops below threshold."""
        invested_cash = stock.get_cash_invested() - stock.get_cash_withdrawn()
        investment_value = stock.get_investment_value()
        loss = (investment_value - invested_cash)/invested_cash
        print(f"Loss for {stock.get_ticker()}: {loss}, Threshold: {threshold}")
        if loss <= -threshold:
            print(f"Stopping loss for {stock.get_ticker()}")
            return self.balance.sell(stock, stock.get_number_stocks())
        print(f"Loss for {stock.get_ticker()} does not exceed threshold. No action taken.")
        return False
        

    def dollar_cost_avg(self, stock, cash, day_interval, day_index: int)-> bool:
        """Invest a specified amount of money (cash) into stocks every set amount of days(day_interval)"""
        stock_price = stock.get_current_stock_value()
        shares = cash // stock_price
        if isinstance(day_index, int) and day_index % day_interval == 0:
            return self.balance.purchase(stock, shares)
        return False