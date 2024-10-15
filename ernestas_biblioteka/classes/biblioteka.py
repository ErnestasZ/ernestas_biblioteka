from dataclasses import dataclass
import pickle
import os
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.classes.records import Records, LibRecords
from ernestas_biblioteka.functions.function import check_is_user_unique, check_is_librarian_unique, check_user_for_log, check_librarian_for_log, set_take_book
import ernestas_biblioteka.functions.function as fn
import ernestas_biblioteka.functions.validation_func as v_fn
import ernestas_biblioteka.functions.stat_function as stat_fn
from ernestas_biblioteka.constants import LIB_FILE, USER_MIN_AGE, LIB_MIN_AGE, SUPER_LIB


@dataclass
class Biblioteka:
    def __init__(self):
        self.books: list[Book] = []
        self.users: list[User] = []
        self.librarians: list[Librarian] = []
        self.records: Records = None
        self.log_consumer: User | Librarian = None
        # self.log_new = None
        # defaul Librarian
        self.__load_data()
        if not self.librarians:
            self.add_librarian(
                SUPER_LIB['name'], SUPER_LIB['year'], SUPER_LIB['password'])

    # def __post_init__(self):
    #     self.__load_data()

    def __load_data(self):
        if os.path.exists(LIB_FILE):
            try:
                with open(LIB_FILE, 'rb') as file:
                    data = pickle.load(file)
                print('log_consumer', data.log_consumer)
                self.log_consumer = data.log_consumer
                print('setf_log_consumer', self.log_consumer)
                self
                self.books = data.books
                self.users = data.users
                self.librarians = data.librarians
                if data.records:
                    self.records = data.records
                else:
                    self.records = Records()
                return True
            except Exception as err:
                print(err)

        self.records = Records()

    def __save_lib(self):
        try:
            with open(LIB_FILE, 'wb') as file:
                pickle.dump(self, file)
        except Exception as err:
            print(err)
        print('Išsaugota sekmingai')

    def add_book(self, author: str, name: str, release_year: str, genre: str, qty: str | int = 1) -> Book:
        # only register librarian +
        self.__check_login_lib()
        # check if book exist
        for book in self.books:
            if author == book.author and name == book.name:
                raise LookupError(
                    'Tokia knyga jau yra binbliotekoje, pakeiskite kiekį.')
        # check author non digits only letters > 3 +
        # check name > 0 +
        # relese date 4 digits and year <= current year +
        # genre from Genre List +
        # check qty is int
        new_book = fn.create_book(
            author.strip(), name, release_year, genre, qty)
        # create lib records
        self.records.add_record(LibRecords(self.log_consumer, new_book, 'add'))
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
        self.__save_lib()
        print("prisijungei sėkmingai")
        return user

    def login_librarian(self, name: str, password: str) -> Librarian:
        # check name > 2, no need +
        # check password min >=6 no need +
        librarian = check_librarian_for_log(self.librarians, name, password)
        self.log_consumer = librarian
        self.__save_lib()
        print("prisijungei sėkmingai")
        return librarian

    def logout(self) -> bool:
        self.log_consumer = None
        self.__save_lib()
        print('atsijungiai')
        return True

    def take_book(self, book: Book) -> None:
        # check if login
        self.__check_login_user()
        # check if book has free qty +
        # check if user can take book by count +
        # check if user can take book by is not overdue +
        # check if user had book by author and title +
        new_user_record = set_take_book(self.log_consumer, book)
        self.records.add_record(new_user_record)
        self.__save_lib()
        print("paemete knyga sekmingai")

    def take_book_fake(self, book: Book, user: User):
        new_user_record = set_take_book(user, book)
        self.records.add_record(new_user_record)
        self.__save_lib()
        print("paemete knyga sekmingai")
        return new_user_record

    def return_book(self, book: Book) -> None:
        self.__check_login_user()
        # check if user has this book
        if book not in self.log_consumer.taken_books:
            raise LookupError('Neturi sios knygos')
        # find book records
        book_records = fn.find_taken_book_record(self.log_consumer,
                                                 book, self.records)
        # return book_records
        new_rec = fn.set_return_book(book_records)
        # self.records.add_record(new_return_record)
        self.__save_lib()
        print("grazinote knyga")
        return new_rec

    def remove_book_before_years(self, year: int | str):
        self.__check_login_lib()
        # remove all book before year
        find_books = fn.find_all_book_before(self.active_books(), year)
        # set book is active = False

        # list(map(lambda book: book.set_remove(), find_books))
        for book in find_books:
            book.set_remove()
            self.records.add_record(LibRecords(
                self.log_consumer, book, 'remove'))
        self.__save_lib()
        print("Knygos išimtos")

    def active_books(self) -> list[Book]:
        return [book for book in self.books if book.is_active]

    def get_overdue_books(self) -> list[(Book, User)]:
        overdue_at_now = stat_fn.get_overdue_at_now(self.records.user_records)
        return overdue_at_now

    def find_by_author(self, author: str) -> list[Book]:
        v_fn.validate_name(author)
        author = author.strip()
        act_books = self.active_books()
        return [book for book in act_books if author.lower() in book.author.lower()]

    def find_by_book_tite(self, title: str):
        title_str = str(title)
        if len(str(title_str)) < 1:
            raise ValueError('įveskite knygos pavadinimą.')
        act_books = self.active_books()
        return [book for book in act_books if title_str.lower() in book.name.lower()]

    def get_overdue_books_by_user(self, user: User):
        overdue_books = fn.get_user_overdue(user)
        return overdue_books

    ######################################################
    ######################################################
    # stat

    def get_overdue_books(self) -> list[(Book, User)]:
        overdue_at_now = stat_fn.get_overdue_at_now(self.records.user_records)
        return overdue_at_now

    def get_book_overdue_mean_stat(self) -> float:
        # !!!!!!! kas yra vidutinis vieluojanciu knygu skaicius? Cia vieno skaitytojo?
        overdue_average = stat_fn.get_overdue_averange_by_user(
            self.records.user_records)

        print(overdue_average)
        return overdue_average

    def most_active_book_genre(self) -> dict:
        # top 5
        return stat_fn.get_most_genre(self.active_books())

    def most_taken_genre(self) -> dict:
        # top 5
        return stat_fn.get_most_taken_genre(self.records.user_records)

    def __check_login_user(self) -> None:
        if self.log_consumer == None or not isinstance(self.log_consumer, User):
            raise LookupError('Turi buti prisijunges skaitytojas')

    def __check_login_lib(self) -> None:
        if self.log_consumer == None or not isinstance(self.log_consumer, Librarian):
            raise LookupError('Turi buti prisijunges bibliotekininkas')

    def __len__(self):
        return len(self.books)
