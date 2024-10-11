from dataclasses import dataclass
import pickle
import os
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.classes.records import Records
from ernestas_biblioteka.functions.function import check_is_user_unique, check_is_librarian_unique, check_user_for_log, check_librarian_for_log, set_take_book
import ernestas_biblioteka.functions.function as fn
import ernestas_biblioteka.functions.validation_func as v_fn
from ernestas_biblioteka.constants import LIB_FILE, USER_MIN_AGE, LIB_MIN_AGE


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

    def add_book(self, author: str, name: str, release_year: str, genre: str) -> Book:
        # only register librarian +
        self.__check_login_lib()
        # check author non digits only letters > 3 +
        # check name > 0 +
        # relese date 4 digits and year <= current year +
        # genre from Genre List +
        new_book = fn.create_book(author, name, release_year, genre)
        self.books.append(new_book)
        self.__save_lib()
        return new_book

    def add_user(self, name: str, birth_year: str) -> User:
        # ceck name > 2 +
        v_fn.validate_name(name)
        # check year int 4 numbers and > 16 +
        v_fn.validate_year(birth_year, USER_MIN_AGE)
        if check_is_user_unique(self.users, name):
            new_user = User(name, birth_year)
            self.users.append(new_user)
            self.__save_lib()
            return new_user
        raise LookupError(f'Skaitytojas tokiu "{name}" vardu egzistuoja.')

    def add_librarian(self, name: str, birth_year: str, password: str) -> Librarian | bool:
        # ceck name > 2 +
        v_fn.validate_name(name)
        # check birh_year >= 18 +
        v_fn.validate_year(birth_year, LIB_MIN_AGE)
        # check password >=6 Ž
        v_fn.validate_password(password)
        if check_is_librarian_unique(self.librarians, name):
            new_librarian = Librarian(name, birth_year, password)
            self.librarians.append(new_librarian)
            self.__save_lib()
            return new_librarian
        print(f'Bibliotekininkas tokiu "{name}" vardu egzistuoja')
        return False

    def login_user(self, card_num: str) -> User:
        # check card_number int, == 8 , No need +
        user = check_user_for_log(self.users, card_num)
        self.log_consumer = user
        print("prisijungei sėkmingai")
        return user

    def login_librarian(self, name: str, password: str) -> Librarian:
        # check name > 2, no need +
        # check password min >=6 no need +
        librarian = check_librarian_for_log(self.librarians, name, password)
        self.log_consumer = librarian
        print("prisijungei sėkmingai")
        return librarian

    def logout(self) -> bool:
        self.log_consumer = None
        print('atsijungiai')
        return True

    def take_book(self, book: Book) -> None:
        # check if login
        self.__check_login_user()
        # check if book not taken +
        # check if user can take book by count +
        # check if user can take book by is not overdue +
        # check if user had book by author and title +
        new_user_record = set_take_book(self.log_consumer, book)
        self.records.add_record(new_user_record)
        self.__save_lib()
        print("paemete knyga sekmingai")

    def return_book(self, book: Book) -> None:
        self.__check_login_user()
        # check if user has this book
        if book not in self.log_consumer.taken_books:
            raise LookupError('Neturi sios knygos')
        # find book records
        book_records = fn.find_taken_book_record(
            book, self.records)
        # return book_records
        new_rec = fn.set_return_book(book_records)
        # self.records.add_record(new_return_record)
        self.__save_lib()
        print("grazinote knyga")
        return new_rec

    def __check_login_user(self) -> None:
        if self.log_consumer == None or not isinstance(self.log_consumer, User):
            raise LookupError('Turi buti prisijunges skaitytojas')

    def __check_login_lib(self) -> None:
        if self.log_consumer == None or not isinstance(self.log_consumer, Librarian):
            raise LookupError('Turi buti prisijunges bibliotekininkas')

    def __len__(self):
        return len(self.books)
