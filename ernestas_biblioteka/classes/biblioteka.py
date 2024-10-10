from dataclasses import dataclass
import pickle
import os
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.constants import LIB_FILE


@dataclass
class Biblioteka:
    def __init__(self):
        self.books: list[Book] = []
        # self.users: list[Users] = []
        # self.librarians: list[Librarian] = []
        self.__load_data()

    def __load_data(self):
        if os.path.exists(LIB_FILE):
            try:
                with open(LIB_FILE, 'rb') as file:
                    data = pickle.load(file)
                self.books = data.books
                # self.users = data.users
                # self.librarians = data.librarians
            except Exception as err:
                print(err)

    def __save_lib(self):
        try:
            with open(LIB_FILE, 'wb') as file:
                pickle.dump(self, file)
        except Exception as err:
            print(err)
        print('Išsaugota sekmingai')

    def add_book(self, book: Book):
        self.books.append(book)
        self.__save_lib()

    def __len__(self):
        return len(self.books)
