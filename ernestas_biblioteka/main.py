from ernestas_biblioteka.classes.biblioteka import Biblioteka, Book
from ernestas_biblioteka.classes.consumers.user import User
# from ernestas_biblioteka.classes.cus_exeptions import InvalidGenreError


new_lib = Biblioteka()
# new_lib.add_book(Book(author="George Orwell", name="1984",
#   release_year=1949, genre="Distopijos ir utopijos"))
# new_lib.add_book(author="George Orwell", name="1984",
#                  release_year=1949, genre="Distopijos ir utopijos")
# new_lib.add_book(author="Aldous Huxley", name="Brave New World",
#                  release_year=1932, genre="Distopijos ir utopijos")
# try:
#     new_lib.add_book(Book(author="George Orwell", name="1984",
#                           release_year=1949, genre="Distopijos ir utopijos 4"))
# except Exception as err:
#     print(err)

#########################


new_lib.add_user('Arvydas', 2000)
# new_lib.add_librarian('Onute', 1986, 'seacret123')


# print(len(new_lib))
print(new_lib.books)
# print(new_lib.users)
# print(new_lib.librarians)

for user in new_lib.users:
    print(f'{user.user_card.card_number}')

new_lib.login_librarian('Onute', 'seacret123')
# new_lib.login_user('12863734')
# # new_lib.logout()
if new_lib.log_consumer != None and isinstance(new_lib.log_consumer, User):
    print(new_lib.log_consumer.taken_books)

# new_lib.take_book(new_lib.books[1])
# new_rec = new_lib.return_book(new_lib.books[-1])

# print('naujas',
#       f'{new_rec.book.name} - {new_rec.user.name} - {new_rec.pick_up_date}, {new_rec.return_date}')

# for rec in new_lib.records.user_records:
#     print(f'{rec.book.uuid} {rec.book.name} - {rec.user.name} - {rec.pick_up_date}, {rec.return_date}')

# print(new_lib.books[-1].taken_at)
# print(new_lib.users[-1].taken_books)
