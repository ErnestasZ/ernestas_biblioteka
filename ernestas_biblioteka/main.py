import sqlite3
import psycopg2
from ernestas_biblioteka.classes.biblioteka import Biblioteka, Book
from ernestas_biblioteka.classes.db_biblioteka import BibliotekaDB
from ernestas_biblioteka.constants import SUPER_CARD_NUM, LIBRARY_DB
# from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.functions.faker_function import create_user_list, create_book_list, create_books_from_list, create_user_and_records_history
# from ernestas_biblioteka.classes.cus_exeptions import InvalidGenreError
from ernestas_biblioteka.functions.db_functions import create_book, create_librarian, create_tables, create_user_db
import ernestas_biblioteka.functions.db_psql_functions as pg_fn


lib_db = BibliotekaDB()
# print(lib_db.get_books())
# for book in lib_db.get_books('mar', 'author', None):
#     print(book.uuid, book.title)

# lib_db.take_book('boook')

lib_db.login_user('59864142')
# for book in lib_db.top_5_genre_by_user():
#     print(book)

# for book in lib_db.top_5_genre_by_library():
#     print(book)

# for book in lib_db.get_overdue_books():
#     print(book)

# for user in lib_db.get_book_overdue_mean_stat():
#     print(user)
# print(lib_db.get_book_overdue_mean_stat())


# for user in lib_db.get_users_with_overdue():
#     print(user)

# for user in lib_db.get_user_with_book('bc41c4da-78fa-465c-9040-4850a7641489'):
#     print(user['name'], user['user_uuid'], user['book_uuid'])

# dto_user = lib_db.get_user_with_book('bc41c4da-78fa-465c-9040-4850a7641489')
# for book in dto_user.taken_books_list:
#     print(book.title)

##############################
##############################
# new_lib = Biblioteka()
# print(new_lib.users[0].uuid)

###############################
###############################
# conn = pg_fn.db_connection()
# data base
# create_tables()
# try:
#     with pg_fn.db_connection() as conn:
#         for user in new_lib.users:
#             pg_fn.create_user_db(user, conn)
#         for lib in new_lib.librarians:
#             pg_fn.create_librarian(lib, conn)
#         for book in new_lib.books:
#             pg_fn.create_book(book, conn)
#         for u_record in new_lib.records.user_records:
#             pg_fn.create_user_record(u_record, conn)
#         # pass
#         for l_record in new_lib.records.lib_records:
#             pg_fn.create_lib_record(l_record, conn)
# except Exception as e:
#     print('Klaida', e)

# finally:
#     if conn:
#         conn.close()

###############################
###############################

# #############
# # Faker data
# users_list = create_user_list(12)
# books_list = create_book_list(30)


# create_books_from_list(new_lib, books_list)
# create_user_and_records_history(new_lib, users_list)


###############################
###############################


# new_lib.login_librarian('Onute', 'seacret123')

# new_lib.add_book(Book(author="George Orwell", name="1984",
#                       release_year=1949, genre="Distopijos ir utopijos"))
# new_lib.add_book(author="George Orwell", name="1984",
#                  release_year=1949, genre="Distopijos ir utopijos", qty=3)
# new_lib.add_book(author="Aldous Huxley", name="Brave New World",
#                  release_year=1932, genre="Distopijos ir utopijos")
# new_lib.add_book(author="Yevgeny Zamyatin", name="We",
#                  release_year=1924, genre="Distopijos ir utopijos", qty=2)

# new_lib.add_book(author="Margaret Atwood", name="The Handmaid's Tale",
#                  release_year=1985, genre="Distopijos ir utopijos", qty=2)
# new_lib.add_book(author="Ray Bradbury", name="Fahrenheit 451",
#                  release_year=1953, genre="Distopijos ir utopijos", qty=2)
# new_lib.add_book(author="Lois Lowry", name="The Giver",
#                  release_year=1993, genre="Distopijos ir utopijos", qty=2)

# try:
#     new_lib.add_book(Book(author="George Orwell", name="1984",
#                           release_year=1949, genre="Distopijos ir utopijos 4"))
# except Exception as err:
#     print(err)

#########################


# new_lib.add_user('Arvydas', 2000)
# new_lib.add_librarian('Onute', 1890, 'seacret123')


# print(len(new_lib))
# print(new_lib.active_books())

# print(new_lib.users)
# print(new_lib.librarians)
# print(new_lib.log_consumer)

# for user in new_lib.users:
#     print(f'{user.user_card.card_number}')

# new_lib.login_user('93101285')
# new_lib.login_user(SUPER_CARD_NUM)
# print(new_lib.log_consumer)
# # new_lib.logout()
# if new_lib.log_consumer != None and isinstance(new_lib.log_consumer, User):
#     print(new_lib.log_consumer.taken_books)

# new_lib.take_book(new_lib.books[1])
# print(new_lib.books[0].is_active)
# new_rec = new_lib.return_book(new_lib.books[1])

# print('naujas',
#       f'{new_rec.book.name} - {new_rec.user.name} - {new_rec.pick_up_date}, {new_rec.return_date}')

# for rec in new_lib.records.user_records:
#     print(f'{rec.book.uuid} {rec.book.name} - {rec.user.name} - {rec.pick_up_date}, {rec.return_date}')

# for rec in new_lib.records.lib_records:
#     print(f'{rec.book.uuid} {rec.book.name} - {rec.librarian.name} - {rec.type}, {rec.date}')

# print(new_lib.books[-1].taken_at)
# print(new_lib.users[-1].taken_books)

# print(new_lib.remove_book_before_years(1001))


# all active books
# print(new_lib.active_books()) +

# all overdue books
# print(new_lib.get_overdue_books())

# get overdue by user
# print(new_lib.get_overdue_books_by_user(new_lib.users[0])) +

# find by author name
# print(new_lib.find_by_author('mar')) +

# find by book title
# print(new_lib.find_by_book_tite('line')) +


# stat averange overdue
# new_lib.get_book_overdue_mean_stat() +

# top 5 genre in library
# print(new_lib.most_taken_genre()) +

# top 5 genre in library
# print(new_lib.most_active_book_genre()) +
