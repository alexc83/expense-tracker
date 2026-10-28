import sqlite3, sys
from asyncio import print_call_graph


### HELPER METHODS ###

# create sqlite DB and table
def create_db():
    con = sqlite3.connect("expenses.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS 
                expenses(   id INTEGER PRIMARY KEY AUTOINCREMENT,
                            description TEXT NOT NULL,
                            amount REAL NOT NULL,
                            created_at TEXT DEFAULT (date('now', 'localtime')));''')
    con.close()


# use to remember what index is what in args
def print_args():
    for index, item in enumerate(sys.argv):
        print(f"{index}: {item}")


# get text for month digits
def get_month_text(month):
    match month:
        case "1":
            return "January"
        case "2":
            return "February"
        case "3":
            return "March"
        case "4":
            return "April"
        case "5":
            return "May"
        case "6":
            return "June"
        case "7":
            return "July"
        case "8":
            return "August"
        case "9":
            return "September"
        case "10":
            return "October"
        case "11":
            return "November"
        case "12":
            return "December"

def args_long_enough():
    return len(sys.argv) > 3

def args_data_dict():
    args_data = dict()

    for i in range(len(sys.argv)):
        if sys.argv[i].startswith("--"):
            key = sys.argv[i][2:]
            if i + 1 >= len(sys.argv):
                print(f"Please provide {key} argument")
                sys.exit(1)
            data = sys.argv[i + 1]
            args_data[key] = data

    return args_data

def validate_amount(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return False
        return True
    except ValueError:
        return False


def command_choice(command, connection):
    # argv data
    argv_data = args_data_dict()
    # match-case
    match command:
        case "add":
            if ("description" in argv_data
                    and "amount" in argv_data):
                add_expense(connection, argv_data)
            else:
                print("Invalid commands")
                print("Please provide description and amount")
        case "update":
            if ("description" in argv_data and "id" in argv_data
                    and "amount" in argv_data):
                update_expense(connection, argv_data)
            else:
                print("Invalid commands")
                print("Please provide expense id, description and amount")
        case "delete":
            if "id" in argv_data:
                delete_expense(connection, argv_data)
            else:
                print("Invalid commands")
                print("Please provide expense id")
        case "list":
            list_expenses(connection)
        case "summary":
            if "month" in argv_data:
                get_summary(connection, argv_data)
            else:
                get_summary(connection)
        case _:
            print("Invalid command")
            print("Enter add, delete, list or summary")


def add_expense(connection, argv_data):
    # get expense data from command line arguments
    description = argv_data["description"]
    amount = argv_data["amount"]

    if not validate_amount(amount):
        print("Amount must be a valid positive number")
        return

    # set up DB cursor
    cur = connection.cursor()

    # insert new expense
    cur.execute('''INSERT INTO expenses(description, amount) 
                        VALUES (?, ?)''',
                (description, amount))

    # save to the database
    connection.commit()

    # print success message
    print(f"new expense added: (ID: {cur.lastrowid})")

    # close cursor
    cur.close()

def update_expense(connection, argv_data):
    # get data from command line arguments
    description = argv_data["description"]
    amount = argv_data["amount"]
    id = argv_data["id"]

    if not validate_amount(amount):
        print("Amount must be a valid positive number")
        return

    cur = connection.cursor()
    cur.execute('''
                UPDATE expenses 
                SET amount = ?, description = ? 
                WHERE id = ?''',
                (amount, description, id))

    # print success message
    if cur.rowcount > 0:
        print(f"expense ID: {id} updated")
    else:
        print(f"No expense with id {id} found")

def delete_expense(connection, argv_data):
    id_to_delete = argv_data["id"]
    cur = connection.cursor()

    deleted_result = cur.execute('''DELETE FROM expenses WHERE id = ?''', (id_to_delete,)).fetchone()

    if cur.rowcount > 0:
        print("Expense deleted successfully")
    else:
        print(f"No expense with id {id_to_delete} found")

    cur.close()


def list_expenses(connection):
    # set up cursor
    cur = connection.cursor()

    # pull database rows
    expenses = cur.execute('''SELECT * FROM expenses''').fetchall()

    # print out the expenses
    if expenses:
        print("ID\tDate\t\tDescription\t\tAmount")
        for expense in expenses:
            print(f"{expense[0]}\t{expense[3]}\t{expense[1]}\t\t\t${expense[2]:.2f}")
    else:
        print("No expenses found")

    # close cursor
    cur.close()


def get_summary(connection, argv_data = None):
    cur = connection.cursor()
    if argv_data and "month" in argv_data:
        month = argv_data["month"]
        month_word = get_month_text(month)
        month = month.zfill(2)
        expenses_monthly_total = cur.execute(
            '''SELECT SUM(amount) 
                FROM expenses 
                WHERE strftime('%Y', created_at) = strftime('%Y', 'now', 'localtime') 
                AND strftime('%m', created_at) = ?
            ''', (month,)).fetchone()
        if expenses_monthly_total[0]:
            print(f"Total expenses for {month_word}: ${expenses_monthly_total[0]:.2f}")
        else:
            print("No expenses found")
    else:
        expenses_total = cur.execute('''SELECT SUM(amount) FROM expenses''').fetchone()
        if expenses_total[0]:
            print(f"Total expenses: ${expenses_total[0]:.2f}")
        else:
            print("No expenses found")

    cur.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter add, update, delete, list or summary")
        sys.exit(1)
    print_args()
    # creates a DB if it doesn't exist
    create_db()
    con = None
    try:
        con = sqlite3.connect("expenses.db")
        with con:
            command_choice(sys.argv[1], con)

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        if con is not None:
            con.close()
