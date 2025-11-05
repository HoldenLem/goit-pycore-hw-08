from src.bot.entities.addres_book import AddressBook
from src.bot.entities.record import Record
from src.bot.facade.serealizator import save_data, load_data


def test_save_and_load():
    p = "ab.pkl"
    book = AddressBook()
    r = Record("Hanna")
    r.add_phone("1234567890")
    book.add_record(r)

    save_data(book, p)
    loaded = load_data(p)

    assert len(list(loaded)) == 1
    same = loaded.find("Hanna")
    assert same is not None
    assert any(ph.value == "1234567890" for ph in same.phones)