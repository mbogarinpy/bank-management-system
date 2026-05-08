"""
Base class representing a bank/repository.
"""

from exceptions import InsufficientFundsError
from account import SavingsAccount, CheckingAccount
import uuid
from bank_data_base import Database
from portfolio import Portfolio


class Bank:
    """
    Manages all bank accounts and portfolios, handles persistence through the database.
    """

    def __init__(self):
        self._accounts = {}
        self._portfolios = {}
        self._data_base = Database()
        row = self._data_base.load_accounts()

        for acc in row:
            if acc[3] == "SavingsAccount":
                self.create_account(
                    acc[3], acc[1], acc[2], acc[4], save=False, account_id=acc[0]
                )
            elif acc[3] == "CheckingAccount":
                self.create_account(
                    acc[3], acc[1], acc[2], acc[5], save=False, account_id=acc[0]
                )

        for portfolio_id, portfolio_obj in self._portfolios.items():
            row = self._data_base.load_positions(str(portfolio_id))
            for r in row:
                portfolio_obj.add_position(r[1], r[2], r[3], save=False)

    def create_account(
        self, account_type, owner, balance, extra_param, save=True, account_id=None
    ):
        """
        Creates a new SavingsAccount or CheckingAccount with a linked portfolio.
        Generates a unique UUID as the account ID.
        Raises ValueError if account type is invalid.
        """

        if account_id is None:
            new_user_id = uuid.uuid4()
        else:
            new_user_id = uuid.UUID(account_id)

        if account_type == "SavingsAccount":
            self._accounts[new_user_id] = SavingsAccount(owner, balance, extra_param)

        elif account_type == "CheckingAccount":
            self._accounts[new_user_id] = CheckingAccount(owner, balance, extra_param)

        else:
            raise ValueError('"savings" or "checking" only accepted')

        if save:
            self._data_base.save_account(new_user_id, self._accounts[new_user_id])

        self._portfolios[new_user_id] = Portfolio(owner, self._data_base, new_user_id)

        return new_user_id

    def get_account(self, account_id):
        """
        Gets the account using the unique account_id.
        Raises a ValueError if the account_id it's not valid.
        Raises a KeyError if the account has not been created yet.
        """

        try:
            account = self._accounts.get(uuid.UUID(account_id))
        except ValueError as exc:
            raise ValueError("""
                             Invalid account number — please copy and paste your account ID
                             """) from exc

        if account is None:
            raise KeyError("Account has not been found")

        return account

    def get_portfolio(self, account_id):
        """
        Gets the portfolio using the unique account_id.
        Raises a ValueError if the account_id it's not valid.
        Raises a KeyError if the account has not been created yet.
        """

        try:
            account = self._portfolios.get(uuid.UUID(account_id))
        except ValueError as exc:
            raise ValueError(
                "Invalid account number — please copy and paste your account ID"
            ) from exc

        if account is None:
            raise KeyError("Account has not been found")

        return account

    def transfer_account(self, from_id, to_id, amount):
        """
        Allows transfers between two accounts.
        Raises InsufficientFundsError if the source account has insufficient funds.
        """

        from_account = None
        try:
            from_account = self.get_account(from_id)
            from_account.withdraw(amount)
            to_account = self.get_account(to_id)
            to_account.deposit(amount)
        except (KeyError, InsufficientFundsError) as exc:
            if from_account is not None:
                from_account.deposit(amount)
            raise exc

    def list_accounts(self):
        """Prints a summary of all accounts in the bank."""
        for acc in self._accounts.values():
            print(acc)

    def bank_deposit(self, account_id, amount):
        """
        Keeps track of deposits amount into the account
        and updates the balance in the database.
        """

        account = self._accounts.get(uuid.UUID(account_id))
        account.deposit(amount)
        self._data_base.update(account_id, account.balance)

    def bank_withdraw(self, account_id, amount):
        """
        Keeps track of Withdraws amount from the account
        and updates the balance in the database.
        """

        account = self._accounts.get(uuid.UUID(account_id))
        account.withdraw(amount)
        self._data_base.update(account_id, account.balance)
