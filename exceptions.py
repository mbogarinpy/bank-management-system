"""Custom exceptions for the bank management system."""

class InsufficientFundsError(Exception):
    """
    Raised when a withdrawal amount exceeds the available balance.
    """
    def __init__(self, amount):
        self._amount = amount
        super().__init__(f"Insufficient funds. Attempted: ${amount}")
