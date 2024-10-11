from datetime import datetime as dt
from typing import Literal
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.classes.book import Book


class LibRecords:
    def __init__(self, librarian: Librarian, book: Book, type: Literal['remove', 'add']):
        self.librarian = librarian
        self.book = book
        self.type = type
        self.date = dt.now()


class UserRecords:
    def __init__(self, user: User, book: Book):
        self.user = user
        self.book = book
        self.pick_up_date = book.taken_at
        self.return_date: dt = None

    def return_book(self):
        self.return_date = dt.now()


class Records:
    def __init__(self):
        self.user_records: list[LibRecords] = []
        self.lib_records: list[UserRecords] = []

    def add_record(self, add_object: LibRecords | UserRecords):
        if isinstance(add_object, LibRecords):
            self.lib_records.append(add_object)
        if isinstance(add_object, UserRecords):
            self.user_records.append(add_object)
