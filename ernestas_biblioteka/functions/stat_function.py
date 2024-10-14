import datetime as dt
from ernestas_biblioteka.classes.records import LibRecords, UserRecords, Records
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.constants import BOOK_OVERDUE_DAYS


def get_overdue_averange_by_user(user_records: list[UserRecords]) -> float:
    list_overdue_count = {}
    for rec in user_records:
        is_overdue = ((rec.return_date if rec.return_date else dt.datetime.now(
        )) - rec.pick_up_date).days > BOOK_OVERDUE_DAYS
        # print('Paimtos knygos', taken_book.taken_at)
        if is_overdue:
            list_overdue_count[rec.user] = list_overdue_count.get(
                rec.user, 0) + 1
    if not list_overdue_count:
        return 0

    average = sum(list_overdue_count.values()) / len(list_overdue_count)
    return average


def get_most_genre(active_books: list[Book]) -> dict:
    list_by_books_genre = {}
    for book in active_books:
        list_by_books_genre[book.genre] = list_by_books_genre.get(
            book.genre, 0) + 1

    if not list_by_books_genre:
        raise LookupError('Knygų bibliotekoje nerasta.')

    top_5_genres = dict(sorted(list_by_books_genre.items(),
                        key=lambda item: item[1], reverse=True)[:5])
    # print(top_5_genres)
    return top_5_genres


def get_most_taken_genre(user_records: list[UserRecords]) -> dict:
    list_most_popular = {}
    for rec in user_records:
        list_most_popular[rec.book.genre] = list_most_popular.get(
            rec.book.genre, 0) + 1

    if not list_most_popular:
        raise LookupError('Irašų apie paimtas knygas dar nėra.')

    top_5_genres = dict(sorted(list_most_popular.items(),
                        key=lambda item: item[1], reverse=True)[:5])

    return top_5_genres


def get_overdue_at_now(user_records: list[UserRecords]) -> list[Book]:
    overdue_books = []
    for rec in user_records:
        if not rec.return_date and (dt.datetime.now() - rec.pick_up_date).days > BOOK_OVERDUE_DAYS:
            overdue_books.append((rec.book, rec.user))

    return overdue_books

