from ernestas_biblioteka.classes.consumers.consumer import Consumer
import bcrypt

# def check_password(password: str, hashed: str) -> bool:
#     # Check if the given password matches the hashed password
#     return bcrypt.checkpw(password.encode(), hashed.encode())


class Librarian(Consumer):
    def __init__(self, name: str,  con_year: int, password: str):
        super().__init__(name, con_year, type='bibliotekininkas')
        self.__password = self.__hash_password(password)

    def __hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    @classmethod
    def lib_from_db(cls, result: tuple[str, str, int, str]):
        """
        Args:
            result (tuple[str, str, int, str]): A tuple containing:
                - uuid: (str) The UUID of the librarian.
                - name: (str) The name of the librarian.
                - birth_year: (int) The birth year of the librarian.
                - password: (str) The hashed password of the librarian.
        """
        uuid, name, birth_year, password, registration_date = result
        librarian = cls(name=name, con_year=birth_year,
                        password=password)
        librarian.uuid = uuid
        librarian.type = 'bibliotekininkas'
        librarian.registration_data = registration_date
        return librarian

    def check_password(self, log_password: str) -> bool:
        if bcrypt.checkpw(log_password.encode(), self.__password.encode()):
            return True
        return False

    def get_password(self):
        return self.__password

    def __eq__(self, other) -> bool:
        if isinstance(other, Librarian):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __str__(self):
        return f'{self.type} - {self.name}, dirba nuo {self.registration_data}'

    def __repr__(self):
        return f'{self.type} - {self.name}, dirba nuo {self.registration_data}'
