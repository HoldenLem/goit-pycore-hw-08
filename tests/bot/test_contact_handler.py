import pytest
from src.bot import contact_handler as ch
from src.bot.entities.addres_book import AddressBook


@pytest.fixture()
def book():
    return AddressBook()


def test_valid_add_contact(book):
    msg = ch.add_contact(["Alice", "1234567890"], book)
    assert msg == "Contact Alice added with phone 1234567890."
    rec = book.find("Alice")
    assert rec is not None
    assert [p.value for p in rec.phones] == ["1234567890"]


def test_add_contact_invalid_format(book):
    res1 = ch.add_contact(["John", "12345"], book)
    assert str(res1) == "Phone should be 10 digit"
    assert book.find("John") is None

    res2 = ch.add_contact(["Ann", "+1234567890"], book)
    assert str(res2) == "Phone should be 10 digit"
    assert book.find("Ann") is None


def test_add_contact_usage_when_args_missing(book):
    res = ch.add_contact(["OnlyName"], book)
    assert res == "Please provide name and phone."
    assert book.find("OnlyName") is None


def test_change_contact_not_found(book):
    res = ch.change_contact(["Bob", "1111111111", "2222222222"], book)
    assert res == '"Contact \'Bob\' does not exist."'


def test_change_contact_invalid_phone(book):
    # додаємо контакт з валідним телефоном
    ch.add_contact(["Eve", "1234567890"], book)
    # намагаємось змінити на невалідний
    res = ch.change_contact(["Eve", "1234567890", "abcd123"], book)
    assert str(res) == "Phone should be 10 digit"
    # телефон залишився старим
    assert [p.value for p in book.find("Eve").phones] == ["1234567890"]


def test_change_contact_success(book):
    ch.add_contact(["Mike", "1111111111"], book)
    res = ch.change_contact(["Mike", "1111111111", "2222222222"], book)
    assert res == "Phone number for Mike updated to 2222222222."
    assert [p.value for p in book.find("Mike").phones] == ["2222222222"]


def test_change_contact_usage_when_args_missing(book):
    res = ch.change_contact(["Mike"], book)
    assert res == "Please provide a <name> <old_phone> <new_phone> after a command <phone>."


def test_get_phone_found_and_not_found(book):
    ch.add_contact(["Lara", "3333333333"], book)

    found = ch.get_phone(["Lara"], book)
    assert found == "Lara: 3333333333"

    usage = ch.get_phone([], book)
    assert usage == "Please provide a name after a command <phone>."


def test_show_all_empty_and_non_empty(book):
    empty = ch.show_all(book)
    assert empty == "No contacts yet."

    ch.add_contact(["Ann", "4444444444"], book)
    out = ch.show_all(book)
    assert out.startswith("Contacts list:")
    assert "Contact name: Ann" in out
    assert "4444444444" in out


def test_add_birthday_invalid_format(book):
    ch.add_contact(["Test", "1234567890"], book)
    res = ch.add_birthday(["Test", "2000-11-10"], book)

    assert res == "Invalid date format. Use DD.MM.YYYY"
    assert book.find("Test").birthday is None


def test_show_birthday_set(book):
    ch.add_contact(["Kate", "1234567890"], book)
    ch.add_birthday(["Kate", "01.01.1990"], book)

    res = ch.show_birthday(["Kate"], book)
    assert res == "01.01.1990"


def test_show_birthday_not_set(book):
    ch.add_contact(["Bob", "1234567890"], book)

    res = ch.show_birthday(["Bob"], book)
    assert res == "Not set."


def test_birthdays_empty(book):
    res = ch.birthdays(book)
    assert res == "No birthdays in this week."
