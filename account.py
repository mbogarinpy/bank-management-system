"""
Account module containing Account, SavingsAccount, and CheckingAccount classes.
"""

from decimal import Decimal
from exceptions import InsufficientFundsError


class Account:
    """
    Base class representing a bank account
    with deposit, withdrawal, and transaction history.
    """

    def __init__(self, owner, balance):
        self._owner = owner
        self._balance = Decimal(balance)
        self._transaction_history = []

    @property
    def owner(self):
        """Returns the account owner's name."""
        return self._owner

    @property
    def balance(self):
        """Returns the current account balance."""
        return self._balance

    def deposit(self, amount):
        """
        Deposits amount into the account balance
        Raises ValueError if amount is zero or negative.
        """
        amount = Decimal(str(amount))
        if amount > 0:
            self._balance += amount
            self._transaction_history.append(f"Deposit: ${amount}")
        else:
            raise ValueError("Amount must be greater than 0")

    def withdraw(self, amount):
        """
        Withdraws amount from the account balance.
        Raises InsufficientFundsError if amount exceeds balance.
        """
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        elif amount > self._balance:
            raise InsufficientFundsError(amount)
        else:
            self._balance -= amount
            self._transaction_history.append(f"Withdrawal: ${amount}")

    def show_history(self):
        """Prints the full transaction history of the account."""

        for transaction in self._transaction_history:
            print(transaction)

    def __str__(self):
        return f"{self._owner}'s account: ${self._balance:.2f}"


class SavingsAccount(Account):
    """A savings account that earns interest on the balance."""

    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self._interest_rate = Decimal(str(interest_rate))

    def apply_interest(self):
        """Applies interest rate to current balance and logs the transaction."""

        interest_amount = self._balance * self._interest_rate
        self._balance += interest_amount
        self._transaction_history.append(f"Interest applied: ${interest_amount:.2f}")

    def __str__(self):
        return f"{super().__str__()}    |   Interest rate: {self._interest_rate:.1%}"


class CheckingAccount(Account):
    """A checking account with overdraft protection up to a set limit."""

    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self._overdraft_limit = Decimal(str(overdraft_limit))

    def withdraw(self, amount):
        """Withdraws amount allowing balance to go negative up to the overdraft limit."""

        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        elif amount > (self._balance + self._overdraft_limit):
            raise InsufficientFundsError(amount)
        else:
            self._balance -= amount
            self._transaction_history.append(f"Withdrawal: ${amount}")

            if self._balance < 0:
                print(f"Warning: account is overdrawn. Balance: ${self._balance:.2f}")

    def __str__(self):
        return (
            f"{super().__str__()}    |   Overdraft limit: ${self._overdraft_limit:.2f}"
        )
