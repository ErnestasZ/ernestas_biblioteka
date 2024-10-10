from ernestas_biblioteka.classes.consumers.consumer import Consumer
import bcrypt

# def check_password(password: str, hashed: str) -> bool:
#     # Check if the given password matches the hashed password
#     return bcrypt.checkpw(password.encode(), hashed.encode())


class Librarian(Consumer):
    def __init__(self, name: str,  con_year: int, password: str):
        super().__init__(name, con_year, type='bibliotekininkas')
        self.password = self.__hash_password(password)

    def __hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def __str__(self):
        return f'{self.type} - {self.name}, dirba nuo {self.registration_data}'

    def __repr__(self):
        return f'{self.type} - {self.name}, dirba nuo {self.registration_data}'
