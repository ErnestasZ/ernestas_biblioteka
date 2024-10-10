from ernestas_biblioteka.classes.biblioteka import Biblioteka, Book
# from ernestas_biblioteka.classes.cus_exeptions import InvalidGenreError


new_lib = Biblioteka()
# new_lib.add_book(Book(author="George Orwell", name="1984",
#                  release_year=1949, genre="Distopijos ir utopijos"))
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
print(new_lib.librarians)

for user in new_lib.users:
    print(f'{user.user_card.card_number}')

# new_lib.login_librarian('Onute', 'seacret123')
new_lib.login_user('599826923')
# new_lib.logout()
if new_lib.log_consumer:
    print(new_lib.log_consumer.name)
