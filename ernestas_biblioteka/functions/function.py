import bcrypt
import datetime as dt
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.classes.records import LibRecords, UserRecords, Records
import ernestas_biblioteka.functions.validation_func as v_fn
from ernestas_biblioteka.constants import BOOK_OVERDUE_DAYS, MAX_TAKEN_BOOKS

# from __future__ import annotations


def check_is_user_unique(users: list[User], name) -> bool:
    if name not in [user.name for user in users]:
        return True
    return False


def check_is_librarian_unique(librarians: list[Librarian], name) -> bool:
    if name not in [user.name for user in librarians]:
        return True
    return False


def check_user_for_log(users: list[User], card_num: str) -> User:
    # if not card_num
    log_user = next(
        (user for user in users if user.user_card.card_number == str(card_num)), None)
    if not log_user != None:
        raise LookupError(
            'Neteisingas kortles NR., iveskite iš 8 simbolių!')
    return log_user


def check_librarian_for_log(librarians: list[Librarian], name: str,  password: str) -> Librarian:
    log_librarian = next(
        (lib for lib in librarians if lib.name == name), None)
    if log_librarian:
        if log_librarian.check_password(password):
            return log_librarian
    raise LookupError(
        'Neteisingas slaptažodis arba vardas, iveskite is naujo!')


def set_take_book(user: User, book: Book) -> UserRecords:
    # if book.taken_at:
    #     raise LookupError('Knyga šiuo metu paimta.')

    if book.qty <= len(book.taken_by):
        raise LookupError('Paimti visi knygos egzemplioriai.')
    if len(user) > MAX_TAKEN_BOOKS:
        raise LookupError('Jus turite max kiekį knygų.')
    # for user_book in user.taken_books:
    #     if book.eq_book(user_book):
    #         raise LookupError('Jau turi šią knygą.')
    if book in user.taken_books:
        raise LookupError('Jau turi šią knygą.')

    for taken_book in user.taken_books:
        # print('Paimtos knygos', taken_book.taken_at)
        if taken_book.taken_at + dt.timedelta(days=BOOK_OVERDUE_DAYS) < dt.datetime.now():
            raise LookupError(
                'Kol turite uždelstų knygų, paimti naujų negalite.')

    user.add_book(book)
    book.set_taken(user)

    # create records
    return UserRecords(user, book)


def find_taken_book_record(user: User, book: Book, records: Records):
    # print(book.taken_at)
    # raise LookupError('testas.')
    taken_book = user.find_taken_book(book)
    print('paimta knyga', taken_book)
    if not records.user_records or not taken_book:
        raise LookupError('Irašų nerasta.')

    # for user_r in records.user_records:
    #     if user_r.pick_up_date == book.taken_at:
    #         print(user_r.book.taken_at, book.taken_at)
    # return

    book_rec = next((user_r for user_r in records.user_records if (user_r.book ==
                    book) and (user_r.pick_up_date == taken_book.taken_at)), None)
    if not book_rec:
        raise LookupError('Irašų nerasta.')
    # book_rec.return_book()
    return book_rec


def set_return_book(user_record: UserRecords):
    user_record.user.return_book(user_record.book)
    user_record.book.set_return(user_record.user)
    user_record.return_book()
    return user_record


def create_book(author: str, name: str, release_year: int, genre: str, qty: str | int) -> Book:
    v_fn.validate_name(author)
    if len(str(name)) < 1:
        raise ValueError('įveskite knygos pavadinimą.')
    v_fn.validate_year(release_year)
    v_fn.validate_book_genre(genre)
    v_fn.validate_qty(qty)
    return Book(author, name, release_year, genre, qty)
