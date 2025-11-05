from src.bot.contact_handler import (
    add_contact,
    change_contact,
    get_phone,
    show_all, add_birthday, show_birthday, birthdays,
)
from src.bot.entities.addres_book import AddressBook
from src.bot.facade.serealizator import load_data, save_data


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, *args


def print_help():
    return (
        " Available commands:\n"
        "  add <name> <phone>              — add a new contact or append phone to existing\n"
        "  change <name> <old> <new>       — replace phone for a contact\n"
        "  phone <name>                    — show phones of a contact\n"
        "  all                             — list all contacts\n"
        "  add-birthday <name> <DD.MM.YYYY>— set birthday for a contact\n"
        "  show-birthday <name>            — show contact's birthday\n"
        "  birthdays                       — upcoming birthdays within 7 days\n"
        "  hello                           — greeting\n"
        "  exit / close                    — quit the bot\n"
    )


def run_cli(book: AddressBook):
    hello = ("Welcome to the assistant bot! \n"
             "Type 'help' to see available commands.")
    print(hello)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "hello":
            print(hello)
        elif command == "":
            continue
        else:
            print("Unknown command. Type 'help' to see what I can do.")


def main():
    book: AddressBook = load_data()

    try:
        run_cli(book)
    finally:
        save_data(book)


if __name__ == "__main__":
    main()
