from src.bot.facade.decoration import input_error
from src.bot.entities.addres_book import AddressBook
from src.bot.entities.record import Record


@input_error
def add_contact(args, book: AddressBook) -> str:
    name, phone = args[0], args[1]
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f"Contact {name} added with phone {phone}."
    if not record.add_phone(phone):
        raise ValueError(f"Phone {phone} already exists for {name}.")
    return f"Phone {phone} added to contact {name}."


@input_error
def change_contact(args, book: AddressBook) -> str:
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = ensure_contact_exists(name, book)
    changed = record.edit_phone(old_phone, new_phone)
    if not changed:
        raise ValueError(
            "Cannot change phone: old number not found or new number duplicates existing."
        )

    return f"Phone number for {name} updated to {new_phone}."


@input_error
def get_phone(args, book: AddressBook) -> str:
    name = args[0]
    record = ensure_contact_exists(name, book)
    phones = ", ".join(ph.value for ph in record.phones)
    if not phones:
        return f"{name} has no phones."
    return f"{name}: {phones}"


def show_all(book: AddressBook) -> str:
    if not book.data:
        return "No contacts yet."
    return (
            "Contacts list: \n"
            + "\n".join(f"{r}" for r in book.data.values())
    )


@input_error
def add_birthday(args, book):
    name, birthday = args[0], args[1]
    record = ensure_contact_exists(name, book)
    record.add_birthday(birthday)
    return f"Birthday {birthday} added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = ensure_contact_exists(name, book)
    birthday = record.birthday
    if not birthday:
        return "Not set."
    return f"{birthday.value}"


def birthdays(book: AddressBook):
    bd_list = book.get_upcoming_birthday()
    if not bd_list:
        return "No birthdays in this week."
    return book.get_upcoming_birthday()


def ensure_contact_exists(name: str, book: AddressBook) -> Record:
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' does not exist.")
    return record
