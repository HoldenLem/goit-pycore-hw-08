from calendar import isleap
from collections import UserDict
from datetime import date, timedelta

from src.bot.entities.record import Record


class AddressBook(UserDict):
    def add_record(self, record: Record) -> bool:
        name = record.name.value
        if name in self.data:
            return False
        self.data[name] = record
        return True

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        return self.data.pop(name, None) is not None

    def get_upcoming_birthday(self, today: date | None = None):
        congratulation_list = []
        if today is None:
            today = date.today()
        for record in self.data.values():
            if record.birthday is None:
                continue
            try:
                birthday_object = record.birthday.date
                birthday_this_year = AddressBook.normalize_birthday_for_year(birthday_object, today.year)

                if birthday_this_year < today:
                    next_year = today.year + 1
                    birthday_this_year = AddressBook.normalize_birthday_for_year(birthday_object, next_year)
                days_until_birthday = (birthday_this_year - today).days

                if days_until_birthday < 0:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                    days_until_birthday = (birthday_this_year - today).days
                if 0 <= days_until_birthday <= 7:
                    birthday_this_year = AddressBook.shift_to_weekday(birthday_this_year)
                    congratulation_list.append(f'{record.name.value}: {birthday_this_year}')

            except (ValueError, KeyError) as e:
                print(f"Warning: Skipping entry due to error: {e}. Entry: {record}")
            except Exception as e:
                print(f"Unexpected error: {e}. Entry: {record}")
        return congratulation_list

    @staticmethod
    def shift_to_weekday(date_obj: date) -> date:
        if date_obj.weekday() == 5:
            return date_obj + timedelta(days=2)
        elif date_obj.weekday() == 6:
            return date_obj + timedelta(days=1)
        return date_obj

    @staticmethod
    def normalize_birthday_for_year(bday: date, year: int) -> date:
        """Returns the birthday date in the specified year, taking into account February 29 in non-leap years."""
        if bday.month == 2 and bday.day == 29 and not isleap(year):
            return date(year, 2, 28)
        return bday.replace(year=year)
