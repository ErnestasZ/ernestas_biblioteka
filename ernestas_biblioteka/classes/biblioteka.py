from dataclasses import dataclass
import pickle
import os
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.classes.records import Records
from ernestas_biblioteka.functions.function import check_is_user_unique, check_is_librarian_unique, check_user_for_log, check_librarian_for_log, set_take_book

from ernestas_biblioteka.constants import LIB_FILE


@dataclass
class Biblioteka:
    def __init__(self):
        self.books: list[Book] = []
        self.users: list[User] = []
        self.librarians: list[Librarian] = []
        self.records: Records = None
        self.__load_data()
        self.log_consumer: User | Librarian = None

    def __load_data(self):
        if os.path.exists(LIB_FILE):
            try:
                with open(LIB_FILE, 'rb') as file:
                    data = pickle.load(file)
                self.books = data.books
                self.users = data.users
                self.librarians = data.librarians
                if data.records:
                    self.records = data.records
                else:
                    self.records = Records()
            except Exception as err:
                print(err)

    def __save_lib(self):
        try:
            with open(LIB_FILE, 'wb') as file:
                pickle.dump(self, file)
        except Exception as err:
            print(err)
        print('Išsaugota sekmingai')

    def add_book(self, author: str, name: str, release_year: int, genre: str) -> Book:
        new_book = Book(author, name, release_year, genre)
        if new_book in self.books:
            raise LookupError('Ši knyga pridėta')
        try:
            new_book = Book(author, name, release_year, genre)
        except Exception as err:
            print(err)
            return False
        self.books.append(new_book)
        self.__save_lib()
        return new_book

    def add_user(self, name: str, birth_year: int) -> User | bool:
        # check year int 4 numbers and > 16
        # ceck name > 2
        if check_is_user_unique(self.users, name):
            new_user = User(name, birth_year)
            self.users.append(new_user)
            self.__save_lib()
            return new_user
        print(f'Skaitytojas tokiu "{name}" vardu egzistuoja')
        return False

    def add_librarian(self, name: str, birth_year: int, password: str) -> Librarian | bool:
        # check year int 4 numbers and > 16
        # ceck name > 2
        # check password >=6
        if check_is_librarian_unique(self.librarians, name):
            new_librarian = Librarian(name, birth_year, password)
            self.librarians.append(new_librarian)
            self.__save_lib()
            return new_librarian
        print(f'Bibliotekininkas tokiu "{name}" vardu egzistuoja')
        return False

    def login_user(self, card_num: str) -> User:
        # check name > 2
        # check card_number int, == 8
        user = check_user_for_log(self.users, card_num)
        self.log_consumer = user
        print("prisijungei sėkmingai")
        return user

    def login_librarian(self, name: str, password: str) -> Librarian:
        # check name > 2
        # check password min >=6
        librarian = check_librarian_for_log(self.librarians, name, password)
        self.log_consumer = librarian
        print("prisijungei sėkmingai")
        return librarian

    def logout(self) -> bool:
        self.log_consumer = None
        print('atsijungiai')
        return True

    def take_book(self, book: Book) -> None:
        # check if register
        if self.log_consumer == None or not isinstance(self.log_consumer, User):
            raise LookupError('Paimti knyga gali prisijunges skaitytojas')
        # check if book not taken +
        # check if user can take book by count +
        # check if user can take book by is not overdue +
        new_user_record = set_take_book(self.log_consumer, book)
        self.records.add_record(new_user_record)
        self.__save_lib()
        print("paemete knyga sekmingai")

    def __len__(self):
        return len(self.books)
