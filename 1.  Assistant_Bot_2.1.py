def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(handler):
    def inner(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError as ke:
            return str(ke)
        except IndexError as ie:
            return str(ie)
    return inner

@input_error
def add_contact(args, contacts):
    if len(args) < 2:
        raise ValueError("Error: Missing name or phone number.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) < 2:
        raise ValueError("Error: Missing name or new phone number.")
    name, phone = args
    if name not in contacts:
        raise KeyError("Contact not found.")
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    if not args:
        raise IndexError("Error: Missing name.")
    name = args[0]
    if name not in contacts:
        raise KeyError("Contact not found.")
    return contacts[name]

@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts saved."
    return '\n'.join(f"{name}: {phone}" for name, phone in contacts.items())

def handle_command(command, args, contacts):
    if command == "add":
        return add_contact(args, contacts)
    elif command == "change":
        return change_contact(args, contacts)
    elif command == "phone":
        return show_phone(args, contacts)
    elif command == "all":
        return show_all(contacts)
    elif command == "hello":
        return "How can I help you?"
    else:
        return "Invalid command."

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            response = handle_command(command, args, contacts)
            print(response)

if __name__ == "__main__":
    main()