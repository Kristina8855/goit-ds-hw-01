
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def init(self, value):
        self.value = value

    def str(self):
        return str(self.value)

class Name(Field):
    def init(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().init(value)

class Phone(Field):
    def init(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")
        super().init(value)

class Birthday(Field):
    def init(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def init(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def str(self):
        phones = ', '.join(str(phone) for phone in self.phones)
        birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else "Not set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_by_name(self, name):
        return self.data.get(name)

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= next_week:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays

    def str(self):
        return "\n".join(str(record) for record in self.data.values())

def parse_input(user_input):
    tokens = user_input.split()
    command = tokens[0].lower()  # перший елемент - команда
    args = tokens[1:]  # решта елементів - аргументи
    return command, args

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            print(f"Input error: {e}")
    return wrapper

@input_error
def add_contact(book, name, phone_number):
    record = book.search_by_name(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone_number)
    print("Contact added.")

@input_error
def change_contact(book, name, new_phone_number):
    record = book.search_by_name(name)
    if record:
        record.add_phone(new_phone_number)
        print("Contact updated.")
    else:
        print("Contact not found.")

@input_error
def show_phone(book, name):
    record = book.search_by_name(name)
    if record:
        print(", ".join(str(phone) for phone in record.phones))
    else:
        print("Contact not found.")

@input_error
def show_all(book):
    print(book)

@input_error
def add_birthday(book, name, birthday):
    record = book.search_by_name(name)
    if record:
        record.add_birthday(birthday)
        print("Birthday added to the contact.")
    else:
        print("Contact not found.")

@input_error
def show_birthday(book, name):
    record = book.search_by_name(name)
    if record:
        if record.birthday:
            print(f"{record.name.value}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}")
        else:
            print("Birthday not set for this contact.")
    else:
        print("Contact not found.")

@input_error
def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        print("Upcoming birthdays:")
        for record in upcoming_birthdays:
            print(f"{record.name.value}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}")
    else:
        print("No upcoming birthdays in the next week.")

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    if Path(filename).exists():
        with open(filename, "rb") as f:
            return pickle.load(f)
    return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def main():
    book = load_data()
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command == "add":
            add_contact(book, *args)
        elif command == "change":
            change_contact(book, *args)
        elif command == "phone":
            show_phone(book, *args)
        elif command == "all":
            show_all(book)
        elif command == "add-birthday":
            add_birthday(book, *args)
        elif command == "show-birthday":
            show_birthday(book, *args)
        elif command == "birthdays":
            birthdays(book)
        elif command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()



