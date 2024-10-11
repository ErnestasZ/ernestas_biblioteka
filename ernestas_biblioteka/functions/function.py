import bcrypt
import datetime as dt
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.classes.records import LibRecords, UserRecords
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
    log_user = next(
        (user for user in users if user.user_card.card_number == str(card_num)), None)
    if not log_user != None:
        raise LookupError(
            'Neteisingas kortles NR., iveskite iš naujo!')
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
    if book.taken_at:
        raise LookupError('Knyga šiuo metu paimta.')
    if len(user) > MAX_TAKEN_BOOKS:
        raise LookupError('Jus turite max kiekį knygų.')
    for book in user.taken_books:
        if book.taken_at + dt.timedelta(days=BOOK_OVERDUE_DAYS) > dt.datetime.now():
            raise LookupError('Turite uždelstų knygų, paimti naujų negalite.')

    user.add_book(book)
    book.set_taken()

    # create records
    return UserRecords(user, book)
