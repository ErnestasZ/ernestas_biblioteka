from datetime import datetime as dt
from typing import Literal
from ernestas_biblioteka.classes.consumers.user import User, TakenBook
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
        self.pick_up_date = self.__set_pick_up(user, book)
        self.return_date: dt = None

    def __set_pick_up(self, user: User, book: Book) -> TakenBook:
        taken_book = user.find_taken_book(book)
        if not taken_book:
            return None
        return taken_book.taken_at

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
