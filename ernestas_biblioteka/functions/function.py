import bcrypt
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian

# from __future__ import annotations


def check_is_user_unique(users: list[User], name) -> bool:
    if name not in [user.name for user in users]:
        return True
    return False


def check_is_librarian_unique(librarians: list[Librarian], name) -> bool:
    if name not in [user.name for user in librarians]:
        return True
    return False


def check_user_for_log(users: list[User], card_num: int) -> User:
    log_user = next(
        (user for user in users if user.user_card.card_number == str(card_num)), None)
    if not log_user:
        raise ValueError(
            'Nerasta kortelė arba skaitytojas, iveskite iš naujo!')
    return log_user


def check_librarian_for_log(librarians: list[Librarian], name: str,  password: str) -> Librarian:
    log_librarian = next(
        (lib for lib in librarians if lib.name == name), None)
    if log_librarian:
        if log_librarian.check_password(password):
            return log_librarian
    raise ValueError(
        'Neteisingas slaptažodis arba vardas, iveskite is naujo!')
