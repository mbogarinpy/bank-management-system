"""
Database module for the bank management system.
Manages SQLite persistence for accounts and transactions.
"""

import sqlite3


class Database:
    """
    Handles all SQLite database operations for the bank management system,
    including saving, loading, and updating accounts.
    """

    def __init__(self):
        """
        Connects to the SQLite database and creates the accounts
        and transactions tables if they do not exist.
        """

        self._connection = sqlite3.connect("bank.db")

        self._connection.execute("""CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            owner TEXT,
            balance TEXT,
            account_type TEXT,
            interest_rate TEXT,
            overdraft_limit TEXT
)""")

        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
            id TEXT PRIMARY KEY,
            account_id TEXT,
            description TEXT     
)""")

        self._connection.execute("""CREATE TABLE IF NOT EXISTS positions (
            account_id TEXT,
            symbol TEXT,
            shares TEXT,
            avg_cost TEXT,
            PRIMARY KEY (account_id, symbol)
)""")

        self._connection.commit()

    def save_account(self, account_id, account):
        """
        Inserts a new account record into the accounts table.
        """

        self._connection.execute(
            """
            INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?)

""",
            (
                str(account_id),
                account.owner,
                str(account.balance),
                type(account).__name__,
                str(getattr(account, "_interest_rate", None)),
                str(getattr(account, "_overdraft_limit", None)),
            ),
        )

        self._connection.commit()

    def load_accounts(self):
        """
        Retrieves all account records from the database
        and returns them as a list of tuples.
        """

        result = self._connection.execute("""
            SELECT * FROM accounts
""")
        accounts = result.fetchall()
        return accounts

    def update(self, account_id, new_balance):
        """
        Updates the balance of an existing
        account in the database.
        """

        self._connection.execute(
            """
                                UPDATE accounts SET balance = ? WHERE id = ?
                                """,
            (str(new_balance), str(account_id)),
        )
        self._connection.commit()

    def save_position(self, account_id, symbol, shares, avg_cost):
        """
        Keeps track of the portfolio positions
        """
        self._connection.execute(
            """
            INSERT INTO positions VALUES(?, ?, ?, ?)

""",
            (str(account_id), symbol, shares, avg_cost),
        )

        self._connection.commit()

    def load_positions(self, account_id):
        """
        Retrieves all positions records from the database
        and returns them.
        """

        result = self._connection.execute(
            """
            SELECT * FROM positions
            WHERE account_id = ?                         
""",
            (str(account_id),),
        )

        positions = result.fetchall()
        return positions

    def update_positions(self, account_id, symbol, shares, avg_cost):
        """
        Updates the positions of an existing
        account in the database.
        """

        self._connection.execute(
            """
                                UPDATE positions SET shares = ?,  avg_cost = ? 
                                WHERE account_id = ? AND symbol = ?
                                """,
            (str(shares), str(avg_cost), str(account_id), str(symbol)),
        )
        self._connection.commit()