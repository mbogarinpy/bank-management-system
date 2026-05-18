# Bank Management System with Portfolio Tracker

A command-line bank management system with an integrated stock portfolio tracker built in Python for a CIS final project.

## What it does

- Create savings and checking accounts
- Deposit, withdraw, and transfer funds between accounts
- Overdraft protection on checking accounts
- Interest application on savings accounts
- Track stock positions with live prices via the Yahoo Finance API
- View unrealized gain/loss on your portfolio
- All data persists between runs using SQLite

## How to install and run

Install dependencies:

```
pip install yfinance
```

Run the program:

```
python main.py
```

## How to use it

1. Select `1` to create a savings or checking account — you will be given a UUID account ID, copy it
2. Select `2` to open an existing account by pasting its ID — from here you can deposit, withdraw, transfer, or view your balance and transaction history
3. Select `3` to access your portfolio — you can add stock positions by symbol, view current positions, and calculate total value and unrealized gain/loss using live prices
4. Select `4` to exit — all data is saved automatically

**Note:** Account IDs are UUIDs. Always copy and paste them when prompted — do not type them by hand.

## File manifest

```
bank_system/
├── main.py            # Entry point — run this
├── account.py         # Account, SavingsAccount, CheckingAccount classes
├── bank.py            # Bank class — manages accounts and portfolios
├── bank_data_base.py  # Database class — SQLite persistence
├── portfolio.py       # Portfolio and Position classes
├── exceptions.py      # Custom InsufficientFundsError exception
├── test_plan.md       # Manual test plan
└── README.md          # This file
```

## Known limitations

- Transaction history is stored in memory only and is not persisted between sessions
- There is no menu option to apply interest — it must be called from code
- Stock prices require an active internet connection
- Account IDs are UUIDs and must be copied exactly — there is no name-based lookup

## Author

Mathias Bogarin

## Date

May 2026

## Course

CIS 131 — Introduction to Programming
