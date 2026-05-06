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

## Project structure

```
bank_system/
├── main.py            # Entry point — run this
├── account.py         # Account, SavingsAccount, CheckingAccount classes
├── bank.py            # Bank class — manages accounts and portfolios
├── bank_data_base.py  # Database class — SQLite persistence
├── portfolio.py       # Portfolio and Position classes
├── exceptions.py      # Custom InsufficientFundsError exception
└── .gitignore
```

## How to run

```
python main.py
```

## Requirements

- Python 3
- yfinance

Install dependencies:

```
pip install yfinance
```

## Notes

- The `bank.db` file is created automatically on first run
- Account IDs are UUIDs — copy and paste them when prompted
- Stock prices require an internet connection
