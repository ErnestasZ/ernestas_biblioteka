from dataclasses import dataclass
from ernestas_biblioteka.classes.book import Book


@dataclass
class Biblioteka:
    def __init__(self):
        self.books: list[Book] = []

    def add_book(self, book: Book):
        self.books.append(book)

    def __len__(self):
        return len(self.books)
