import pytest

from src.bot.entities.record import Record


@pytest.fixture
def phones():
    return ["1234567890", "0987654321"]


@pytest.fixture
def record():
    return Record("Hanna")


def test_add_phone(record, phones):
    assert record.add_phone(phones[0]) is True
    assert record.add_phone(phones[0]) is False
    assert record.phones[0].value == phones[0]


def test_add_existing_phone(record, phones):
    record.add_phone(phones[0])
    assert record.add_phone(phones[0]) is False


def test_find_phone(record, phones):
    record.add_phone(phones[0])
    ph = record.find_phone(phones[0])
    assert ph is not None
    assert ph.value == phones[0]


def test_find_phone_not_found(record, phones):
    assert record.find_phone(phones[1]) is None


def test_remove_phone(record, phones):
    record.add_phone(phones[0])
    assert record.remove_phone(phones[0]) is True
    assert record.remove_phone(phones[0]) is False


def test_edit_phone_success(record, phones):
    record.add_phone(phones[0])
    assert record.edit_phone(phones[0], phones[1]) is True
    assert record.find_phone(phones[0]) is None
    ph = record.find_phone(phones[1])
    assert ph is not None and ph.value == phones[1]


def test_edit_phone_not_found(record, phones):
    assert record.edit_phone(phones[0], phones[1]) is False


def test_edit_phone_duplicate_blocked(record, phones):
    record.add_phone(phones[0])
    record.add_phone(phones[1])
    assert record.edit_phone(phones[0], phones[1]) is False
    assert record.find_phone(phones[0]) is not None
    assert record.find_phone(phones[1]) is not None


def test_find_index(record, phones):
    assert record.find_index(phones[0]) is None
    record.add_phone(phones[0])
    idx = record.find_index(phones[0])
    assert isinstance(idx, int) and idx == 0


def test_add_phone_invalid_format_raises(record):
    with pytest.raises(ValueError):
        record.add_phone("12345")

    with pytest.raises(ValueError):
        record.add_phone("12345678901")

    with pytest.raises(ValueError):
        record.add_phone("12345abcde")


def test_edit_phone_invalid_format_raises(record, phones):
    record.add_phone(phones[0])
    with pytest.raises(ValueError):
        record.edit_phone(phones[0], "abc")
