class InsufficientFundsError(Exception):
    """Raised when a withdrawal amount exceeds the available balance."""
    
    def __init__(self, amount):
        """
        Args:
            amount: The amount that was attempted to be withdrawn.
        """
        self._amount = amount
        super().__init__(f'Insufficient funds. Attempted: ${amount}')