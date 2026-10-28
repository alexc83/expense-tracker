# Expense Tracker

A simple command-line expense tracker built with Python and SQLite. Add, update, delete, and list expenses, or view totals for all expenses or a specific month of the current year.

Project: [roadmap.sh Expense Tracker](https://roadmap.sh/projects/expense-tracker)

## Setup

Requires Python 3.14 or later. No third-party dependencies are needed.

Download or clone this repository, then open a terminal in the project directory. Run commands using `python3 main.py`.

The SQLite database, `expenses.db`, is created automatically in the directory where you run the program. Run commands from the project directory to keep using the same database.

## Usage

Add an expense:

```bash
python3 main.py add --description "Lunch" --amount 20
```

Update an expense by ID (provide both description and amount):

```bash
python3 main.py update --id 1 --description "Dinner" --amount 25
```

Delete an expense:

```bash
python3 main.py delete --id 1
```

List all expenses:

```bash
python3 main.py list
```

View the total of all expenses:

```bash
python3 main.py summary
```

View the total for a month of the current year (use a month number from 1 to 12):

```bash
python3 main.py summary --month 10
```

Amounts must be positive numbers. Put descriptions containing spaces in quotes.
