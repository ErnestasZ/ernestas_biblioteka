import uuid
import datetime as dt


class UserTakenBookDTO:
    # def __init__(self, uuid, title, author, genre, qty, taken_qty, release_year, is_active, overdue_days):
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('book_uuid')
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')
        self.genre = kwargs.get('genre')
        self.qty = kwargs.get('qty')
        self.taken_qty = kwargs.get('taken_qty')
        self.release_year = kwargs.get('release_year')
        self.is_active = kwargs.get('is_active')
        self.overdue_days = kwargs.get('overdue_days')

    def __eq__(self, other) -> bool:
        if isinstance(other, UserTakenBookDTO):
            return self.uuid == other.uuid
        return False

    def __hash__(self) -> int:
        return hash(self.uuid)


class LoginUserDataDTO:
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('user_uuid')
        self.name = kwargs.get('name')
        self.birth_year = kwargs.get('birth_year')
        self.card_number = kwargs.get('card_number')
        self.taken_books_list = []

    def __eq__(self, other) -> bool:
        if isinstance(other, LoginUserDataDTO):
            return self.uuid == other.uuid
        return False

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __len__(self):
        return len(self.taken_books_list)
    
class LoginLibDataDTO:
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('lib_uuid')
        self.birth_year =  kwargs.get('birth_year')



