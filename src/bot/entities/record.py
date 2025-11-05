import datetime
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    PHONE_PATTERN = r'\d{10}'

    def __init__(self, value: str):
        if not re.fullmatch(Phone.PHONE_PATTERN, value):
            raise ValueError('Phone should be 10 digit')
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            dt = datetime.datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)
        self.date = dt


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def __str__(self):
        birthday_str = self.birthday.value if self.birthday and self.birthday.value else "not set"

        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "no phones"

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones_str}; "
            f"birthday: {birthday_str}"
        )

    def add_phone(self, phone: str) -> bool:
        if self.find_index(phone) is None:
            self.phones.append(Phone(phone))
            return True
        return False

    def add_birthday(self, birthday) -> bool:
        if birthday is None:
            return False
        self.birthday = Birthday(birthday)
        return True

    def find_phone(self, phone: str) -> Phone | None:
        index = self.find_index(phone)
        if index is not None:
            return self.phones[index]
        return None

    def remove_phone(self, phone: str) -> bool:
        ph = self.find_phone(phone)
        if ph is None:
            return False
        self.phones.remove(ph)
        return True

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        idx = self.find_index(old_phone)
        if idx is None:
            return False
        candidate = Phone(new_phone)
        if any(i != idx and p.value == candidate.value for i, p in enumerate(self.phones)):
            return False
        self.phones[idx].value = candidate.value
        return True

    def find_index(self, value: str) -> int | None:
        for i, p in enumerate(self.phones):
            if p.value == value:
                return i
        return None
