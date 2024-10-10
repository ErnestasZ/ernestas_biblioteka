from ernestas_biblioteka.classes.biblioteka import Biblioteka, Book

new_lib = Biblioteka()
new_lib.add_book(Book(author="George Orwell", name="1984",
                 release_year=1949, genre="Distopijos ir utopijos"))
# new_lib.add_book(Book(author="George Orwell", name="1984",
#                  release_year=1949, genre="Distopijos ir utopijos 4"))
print(len(new_lib))
print(new_lib.books)
