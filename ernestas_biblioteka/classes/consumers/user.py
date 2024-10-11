from ernestas_biblioteka.classes.consumers.consumer import Consumer
from ernestas_biblioteka.classes.book import Book
from ernestas_biblioteka.classes.consumers.user_card import UserCard


class User(Consumer):
    def __init__(self, name: str,  con_year: int):
        super().__init__(name, con_year, type='skaitytojas')
        self.user_card = UserCard()
        self.taken_books = []

    def add_book(self, book: Book):
        self.taken_books.append(book)

    def return_book(self, book: Book):
        self.taken_books.pop(book)

    def __str__(self):
        return f'{self.type} - {self.name}, registracija nuo {self.registration_data}, šiuo metu turi paėmęs {len(self)}'

    def __repr__(self):
        return f'{self.type} - {self.name}, registracija nuo {self.registration_data}, šiuo metu turi {len(self)} kng.'

    def __len__(self):
        return len(self.taken_books)


# new_user = User("Onute", 1980)
# print(new_user)
# print(new_user.user_card.card_number)
