from ernestas_biblioteka.classes.biblioteka import Biblioteka, Book
# from ernestas_biblioteka.classes.cus_exeptions import InvalidGenreError


new_lib = Biblioteka()
new_lib.add_book(Book(author="George Orwell", name="1984",
                 release_year=1949, genre="Distopijos ir utopijos"))
try:
    new_lib.add_book(Book(author="George Orwell", name="1984",
                          release_year=1949, genre="Distopijos ir utopijos 4"))
except Exception as err:
    print(err)



print(len(new_lib))
print(new_lib.books)
