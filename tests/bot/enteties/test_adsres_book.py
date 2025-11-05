import pytest

from src.bot.entities.addres_book import AddressBook
from src.bot.entities.record import Record


@pytest.fixture
def record():
    result = Record("Hanna")
    result.add_phone("1234567890")
    return result


@pytest.fixture
def book():
    return AddressBook()


def test_add_record_success(book, record):
    assert book.add_record(record) is True
    assert "Hanna" in book.data
    assert book.data["Hanna"] is record


def test_add_record_duplicate(book, record):
    book.add_record(record)
    assert book.add_record(record) is False  # вдруге — не додається
    assert len(book.data) == 1


def test_find_record(book, record):
    book.add_record(record)
    found = book.find("Hanna")
    assert found is record
    assert found.name.value == "Hanna"


def test_find_record_not_found(book):
    assert book.find("Unknown") is None


def test_delete_record_success(book, record):
    book.add_record(record)
    assert book.delete("Hanna") is True
    assert book.find("Hanna") is None


def test_delete_record_not_found(book):
    assert book.delete("SomeoneElse") is False
