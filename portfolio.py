"""
    Represents a single stock position with symbol, shares, and average cost.
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

    def __init__(self, owner):
        self._owner = owner
        self._positions = {}

    def add_position(self, symbol, shares, avg_cost):
        """Alows to add a new position."""

        new_stock = Position(symbol, shares, avg_cost)
        self._positions[symbol] = new_stock

    def get_position(self):
        """ "Prints all current positions in the portfolio."""

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

        price = {}
        for position in self._positions:
            ticker = yf.Ticker(position)
            price[position] = Decimal(str(ticker.info["currentPrice"]))

        return price
