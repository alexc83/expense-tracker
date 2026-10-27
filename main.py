import sys

# use to remember what index is what in args
def print_args():
    for index, item in enumerate(sys.argv):
        print(f"{index}: {item}")

def command_choice(command):
    # match-case
    match command:
        case "add":
            pass
        case "delete":
            pass
        case "list":
            pass
        case "summary":
            pass
        case "_":
            print("Invalid command")
            print("Enter add, delete, list or summary")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_args()
    command_choice(sys.argv[1])

