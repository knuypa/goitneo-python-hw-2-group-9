from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)
    
    @staticmethod
    def validate(phone_number):
        return phone_number.isdigit() and len(phone_number) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {', '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        else:
            return False

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(handler):
    def inner(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except Exception as e:
            return str(e)
    return inner

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Error: Missing name or phone number.")
    name, phone = args
    if name in book:
        record = book[name]
        record.add_phone(phone)
        return "Phone number added to the existing contact."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Error: Missing name, old phone, or new phone number.")
    name, old_phone, new_phone = args
    if name in book:
        record = book[name]
        if record.edit_phone(old_phone, new_phone):
            return "Contact phone updated."
        else:
            return "Old phone number not found."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_phone(args, book):
    if not args:
        raise IndexError("Error: Missing name.")
    name = args[0]
    if name in book:
        return book[name].__str__()
    else:
        raise KeyError("Contact not found.")

@input_error
def show_all(book):
    if not book:
        return "No contacts saved."
    return '\n'.join(str(record) for record in book.values())

def handle_command(command, args, book):
    if command == "add":
        return add_contact(args, book)
    elif command == "change":
        return change_contact(args, book)
    elif command == "phone":
        return show_phone(args, book)
    elif command == "all":
        return show_all(book)
    elif command == "hello":
        return "How can I help you?"
    else:
        return "Invalid command."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() in ["exit", "close"]:
            print("Goodbye!")
            break
        command, *args = user_input.split()
        print(handle_command(command, args, book))

if __name__ == "__main__":
    main()