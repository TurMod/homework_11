from homework import *

def main():

    addressbook = AddressBook()

    def input_error(func):
        print('List of available commands:')
        print('add_record name phone(only numbers) birthday(format: DD.MM.YYYY)\ndelete_record name\nadd name phone\ndelete name phone\nchange name old_phone new_phone\nclose/exit\nphone name\ndays_to_birthday name')
        while True:
            try:
                result = func()
                if result == 'break':
                    break
            except TypeError:
                print('You didn\'t put user\'s phone or name!')
            except (UnboundLocalError, KeyError):
                print('Error!')
            except ContactExistsError:
                print('This contact already exist!')
            except ContactDoesNotExistError:
                print('This contact does not exist!')
            except PhoneDoesNotExistError:
                print('The phone number that you\'re trying to change/delete does not exist!')
            except PhoneExistsError:
                print('The phone number that you\'re trying to add already exist!')
            except (AttributeError, IndexError):
                print('This command does not exist!')
            except ValueError:
                print('Put birthday in format DD.MM.YYYY')
            except OnlyNumbersError:
                print('Phone number must include only numbers!')

    @input_error
    def main_handler():
        while True:
            command, *data = input('Write command: ').lower().strip().split(' ', 1)
            if data:
                data = data[0].split(' ')
            else:
                if command in ['close', 'exit']:
                    return 'break'
            if command in ['add_record', 'delete_record']:
                changes = getattr(addressbook, command)
                result = changes(*data)
            elif command == 'show_all':
                result = addressbook.iterator()
            else:
                result = addressbook.change_record(command, data)

            if result == 'break':
                return 'break'
            else:
                print(result)
    

if '__main__' == __name__:
    main()