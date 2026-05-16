"""
Main module for the bank management system. Contains the main CLI loop and user interaction logic.
Handles account creation, deposits, withdrawals, transfers, and portfolio management.
"""

from bank import Bank
from decimal import Decimal, InvalidOperation
from exceptions import InsufficientFundsError


def main():
    """
    Runs the main CLI loop. Handles account creation, deposits, withdrawals,
    transfers, and portfolio management. Raises ValueError, KeyError,
    and InsufficientFundsError which are caught and displayed to the user.
    """

    bank = Bank()
    savings_rate = 0.05
    overdraft_limit = 200

    print("Welcome")
    while True:
        try:
            print("""
                1. Create Account
                2. Open Account
                3. Portfolio
                4. Exit
            """)
            user_input = input("How can we help you today? (1-4)")

            if user_input == "1":
                user_input = input(
                    "1. SavingsAccount\n2. CheckingAccount\nAccount Type(1-2): "
                )
                if user_input == "1":
                    name_input = input("Name: ")
                    balance_input = input("Starting Balance: ")
                    print(f"""Account successfully created!
                        {
                        bank.create_account(
                            "SavingsAccount", name_input, balance_input, savings_rate
                        )
                    }
                        """)
                elif user_input == "2":
                    name_input = input("Name: ")
                    balance_input = input("Starting Balance: ")
                    print(f"""Account successfully created!
                        {
                        bank.create_account(
                            "CheckingAccount",
                            name_input,
                            balance_input,
                            overdraft_limit,
                        )
                    }
                        """)

            elif user_input == "2":
                user_input = input("Enter account number: ")
                account_id_input = user_input
                account = bank.get_account(user_input)
                print(f"Hello {account.owner}")
                user_action = input("""
                                    1. Balance and recent transactions
                                    2. Deposit 
                                    3. Withdraw
                                    4. Transfer
                                    Account action(1-4): 
                                    """)
                if user_action == "1":
                    print(account)
                    account.show_history()

                elif user_action == "2":
                    user_input = input("Amount to deposit: ")
                    bank.bank_deposit(account_id_input, user_input)
                    print(f"Successfully deposited: ${user_input}")

                elif user_action == "3":
                    user_input = input("Amount to withdraw: ")
                    bank.bank_withdraw(account_id_input, user_input)
                    print(f"Successfully withdrew: ${user_input}")

                elif user_action == "4":
                    from_input = input("From (account number): ")
                    to_input = input("To (account number): ")
                    amount_input = input("Amount to be transferred: ")
                    bank.transfer_account(from_input, to_input, amount_input)
                    print("Successfully completed")
                else:
                    print("Enter correct option")

            elif user_input == "3":
                user_input = input("""
                                1. Add positions
                                2. My positions
                                3. Balance 
                                Type(1-3): 
                                """)
                if user_input in ["1", "2", "3"]:
                    account_input = input("Enter account number: ")
                    portfolio_account = bank.get_portfolio(account_input)
                    print(f"Hello {portfolio_account.owner}")

                    if user_input == "1":
                        ticker_input = input("Symbol: ")
                        share_input = int(input("Shares: "))
                        cost_input = Decimal(str(input("Cost: ")))
                        portfolio_account.add_position(
                            ticker_input, share_input, cost_input
                        )

                    elif user_input == "2":
                        portfolio_account.get_position()

                    elif user_input == "3":
                        prices = portfolio_account.get_prices()
                        print(portfolio_account.total_value(prices))
                        print(portfolio_account.total_gain_loss(prices))

                else:
                    print("Enter correct option")

            elif user_input == "4":
                print("Thanks!!")
                break
            else:
                print("Enter correct option")

        except ValueError as e:
            print(e)
        except KeyError as e:
            print(e)
        except InsufficientFundsError as e:
            print(e)
        except InvalidOperation:
            print("Invalid input for amount. Please enter a valid number.")


if __name__ == "__main__":
    main()
