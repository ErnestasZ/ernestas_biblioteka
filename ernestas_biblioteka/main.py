from ernestas_biblioteka.classes.biblioteka import Biblioteka, Book
# from ernestas_biblioteka.classes.cus_exeptions import InvalidGenreError


new_lib = Biblioteka()
# new_lib.add_book(Book(author="George Orwell", name="1984",
#                       release_year=1949, genre="Distopijos ir utopijos"))
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


# new_lib.add_user('Jurate', 1980)
# new_lib.add_librarian('Onute', 1986, 'seacret123')


# print(len(new_lib))
# print(new_lib.books)
print(new_lib.users)
# print(new_lib.librarians)

for user in new_lib.users:
    print(f'{user.user_card.card_number}')

# new_lib.login_librarian('Onute', 'seacret123')
new_lib.login_user('13221407')
# # new_lib.logout()
if new_lib.log_consumer != None:
    print(new_lib.log_consumer.taken_books)

# new_lib.take_book(new_lib.books[-1])
