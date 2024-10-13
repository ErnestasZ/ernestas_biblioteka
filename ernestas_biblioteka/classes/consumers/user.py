from datetime import datetime as dt
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.classes.consumers.consumer import Consumer

from ernestas_biblioteka.classes.consumers.user_card import UserCard


class TakenBook:
    def __init__(self, book: 'Book'):
        self.book = book
        self.taken_at = dt.now()

    def __eq__(self, other) -> bool:
        if isinstance(other, TakenBook):
            return self.book == other.book
        if isinstance(other, Book):
            return self.book == other
        return False

    def __repr__(self):
        return str(self.book)


class User(Consumer):
    def __init__(self, name: str,  con_year: int):
        super().__init__(name, con_year, type='skaitytojas')
        self.user_card = UserCard()
        self.taken_books: list[TakenBook] = []

    def add_book(self, book: 'Book'):
        self.taken_books.append(TakenBook(book))

    def return_book(self, book: 'Book'):
        self.taken_books.remove(book)

    def find_taken_book(self, book: 'Book') -> TakenBook:
        return next((taken_book for taken_book in self.taken_books if book == taken_book.book), None)

    def __eq__(self, other) -> bool:
        if isinstance(other, User):
            return self.name == other.name
        return False

    def __str__(self):
        return f'{self.type} - {self.name}, registracija nuo {self.registration_data}, šiuo metu turi paėmęs {len(self)}'

    def __repr__(self):
        return f'{self.type} - {self.name}, registracija nuo {self.registration_data}, šiuo metu turi {len(self)} kng.'

    def __len__(self):
        return len(self.taken_books)
