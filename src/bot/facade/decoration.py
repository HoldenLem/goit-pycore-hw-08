def input_error(func):
    def inner(*args, **kwargs):
        current_func = func.__name__
        try:
            return func(*args, **kwargs)

        except ValueError as e:
            return str(e)

        except IndexError:
            if current_func == 'add_contact':
                return "Please provide name and phone."
            if current_func == 'change_contact':
                return "Please provide a <name> <old_phone> <new_phone> after a command <phone>."
            if current_func == 'get_phone':
                return "Please provide a name after a command <phone>."
            if current_func == 'add_birthday':
                return "Please provide name and phone after a command <add-birthday>."
            if current_func == 'show_birthday':
                return "Please provide name after a command <show-birthday>."
            return "Not enough arguments."

        except KeyError as e:
            return str(e)

    return inner
