"""
Contains Position and Portfolio classes for tracking stock investments.
"""

from decimal import Decimal
import yfinance as yf


class Position:
    """
    Represents a single stock position with symbol, shares, and average cost.
    """

    def __init__(self, symbol, shares, avg_cost):
        self._symbol = symbol
        self._shares = shares
        self._avr_cost = Decimal(str(avg_cost))

    @property
    def symbol(self):
        """Returns the symbol name"""
        return self._symbol

    @property
    def shares(self):
        """Returns the quantity of shares"""
        return self._shares

    @property
    def avg_cost(self):
        """Returns average cost per share"""
        return self._avr_cost

    def share_cost(self):
        """Calculates the cost of the position."""
        return self._shares * self._avr_cost

    def gain_loss(self, current_price):
        """Calculates the unrealized gain or loss for this position given the current price."""
        return (current_price - self._avr_cost) * self._shares

    def __str__(self):
        return f"Ticker: {self._symbol} Shares: {self._shares}  Cost: {self._avr_cost}"


class Portfolio:
    """
    Manages a collection of stock positions for an owner.
    Allows adding positions and calculating total value and gain/loss using live prices.
    """

    def __init__(self, owner, data_base, account_id):
        self._owner = owner
        self._data_base = data_base
        self._account_id = account_id
        self._positions = {}

    @property
    def owner(self):
        """Returns the account owner's name."""
        return self._owner

    def add_position(self, symbol, shares, avg_cost, save=True):
        """Allows to add a new position."""

        if symbol in self._positions:
                new_avg_cost = (self._positions[symbol].shares * self._positions[symbol].avg_cost + shares * avg_cost) / (self._positions[symbol].shares + shares)
                total_shares = self._positions[symbol].shares + shares
                self._positions[symbol] = Position(symbol, total_shares, new_avg_cost)
                if save:
                    self._data_base.update_positions(self._account_id, symbol, total_shares, new_avg_cost)
        else:
            new_stock = Position(symbol, shares, avg_cost)
            self._positions[symbol] = new_stock
            if save:
                self._data_base.save_position(self._account_id, symbol, shares, avg_cost)

    def get_position(self):
        """Prints all current positions in the portfolio."""

        for position in self._positions.values():
            print(position)

    def total_value(self, prices):
        """Calculates the total current market value of all positions."""

        total = 0
        for position in self._positions.values():
            current_price = prices[position.symbol]
            total += current_price * position.shares

        return total

    def total_gain_loss(self, prices):
        """Calculates the total unrealized gain or loss across all positions."""

        total = 0
        for position in self._positions.values():
            current_price = prices[position.symbol]
            total += position.gain_loss(current_price)

        return total

    def get_prices(self):
        """
        Fetches current market prices for all positions using the yfinance API.
        Returns a dictionary of symbol to current price.
        """

        try:
            price = {}
            for position in self._positions:
                ticker = yf.Ticker(position)
                price[position] = Decimal(str(ticker.info["currentPrice"]))

            return price
        except KeyError as exc:
            raise KeyError(f"Invalid ticker symbol: {position}") from exc
