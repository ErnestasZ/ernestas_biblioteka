import uuid
import datetime as dt


class UserDB:
    def __init__(self, name=None, birth_year=None):
        self.uuid = uuid.uuid4()
        self.name = name
        self.birth_year = birth_year
        self.registration_date = dt.datetime.now()
        self.card_number = None

    @classmethod
    def user_from_db(cls, result: tuple[str, str, int, int, str]):
        """
        Args:
            result (tuple[str, str, int, str]): A tuple containing:
                - uuid: (str) The UUID of the user.
                - name: (str) The name of the user.
                - birth_year: (int) The birth year of the user.
                - card_number: (int) The user card number form 8 digits.
                - registration_date: (str) Registration date of the user.
        """
        uuid, name, birth_year, card_number, registration_date = result
        user = cls(uuid=uuid, name=name, con_year=birth_year,
                   card_number=card_number)
        user.registration_date = registration_date
        return user
