from ernestas_biblioteka.classes.consumers.consumer import Consumer
from ernestas_biblioteka.classes.consumers.user_card import UserCard


class User(Consumer):
    def __init__(self, name: str,  con_year: int):
        super().__init__(name, con_year, type='skaitytojas')
        self.user_card = UserCard()

    def __str__(self):
        return f'{self.type} - {self.name}, registracija nuo {self.registration_data}'


# new_user = User("Onute", 1980)
# print(new_user)
# print(new_user.user_card.card_number)
