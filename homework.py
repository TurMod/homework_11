from collections import UserDict
from collections.abc import Iterator
from datetime import datetime

class ContactExistsError(Exception):
    ...

class ContactDoesNotExistError(Exception):
    ...

class PhoneExistsError(Exception):
    ...

class PhoneDoesNotExistError(Exception):
    ...

class OnlyNumbersError(Exception):
    ...

class AddressBook(UserDict):
    def add_record(self, name: str, phone: str, birthday: str | None =None) -> str:
        if name in self.data:
            raise ContactExistsError
        else:
            self.data[name] = Record(name, phone, birthday)
            return f'Contact with name {name} and phone {phone} was successfully added!'
    
    def delete_record(self, name: str) -> str:
        if name not in self.data:
            raise ContactDoesNotExistError
        else:
            self.data.pop(name)
            return f'Contact with name {name} was successfully removed!'
    
    def change_record(self, command: str, data: list) -> str:
        if data[0] not in self.data:
            raise ContactDoesNotExistError
        elif command == 'phone':
            result = [i.value for i in self.data.get(data[0]).phones]
            return result
        else:
            changes = getattr(self.data.get(data[0]), command)
            result = changes(*data[1:])
            return result
    
    


class Record:
    def __init__(self, name: str, phone: str, birthday: str | None) -> None:
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.birthday = Birthday(birthday)

    def add(self, user_phone: str) -> str:
        phone_in = self.get_phone(user_phone)
        if phone_in:
            raise PhoneExistsError
        else:
            self.phones.append(Phone(user_phone))
            return f'The phone number {user_phone} was successfully added to contact {self.name.value}!'

    def delete(self, user_phone: str) -> str:
        phone_in = self.get_phone(user_phone)
        if not phone_in:
            raise PhoneDoesNotExistError
        else:
            self.phones.remove(phone_in)
            return f'The phone number {user_phone} was successfully removed from contact {self.name.value}!'
    
    def change(self, old_phone: str, new_phone: str) -> str:
        phone_in = self.get_phone(old_phone)
        if not phone_in:
            raise PhoneDoesNotExistError
        else:
            phone_in.value = new_phone
            return f'The phone number {old_phone} in contact {self.name.value} was successfully changed to {new_phone}'
    
    def get_phone(self, user_phone):
        for phone in self.phones:
            if user_phone == phone.value:
                return phone
        return False
    
    def days_to_birthday(self):
        if self.birthday.value == None:
            return 'This contact has not birthday date!'
        else:
            today = datetime.today()
            birthday = datetime(year=today.year, day=self.birthday.value.day, month=self.birthday.value.month)

            if birthday < today:
                birthday = datetime(year=today.year + 1, day=self.birthday.value.day, month=self.birthday.value.month)

            diff = birthday - today
            diff = diff.days
            return diff


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value.isdigit():
            self.__value = value
        else:
            raise OnlyNumbersError


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value == None:
            self.__value = None
        else:
            self.__value = datetime.strptime(value, '%d.%m.%Y')
