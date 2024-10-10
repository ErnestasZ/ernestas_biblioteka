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

for librarian in new_lib.librarians:
    print(f'{librarian.password}')
