import re
from datetime import datetime
from ernestas_biblioteka.constants import GENRES
from ernestas_biblioteka.classes.cus_exeptions import InvalidGenreError


def validate_name(name: str) -> bool:
    name = name.strip()

    if len(name) < 3 or len(name) > 50:
        raise ValueError(
            'Iveskite pilną vardą (nuo 3 iki 50 simbolių).')

    if not re.match(r'^[A-Za-z\s\-]+$', name):
        raise ValueError(
            'Autoriaus vardas tik iš raidžių.')

    return True


def validate_year(year: str, min_age: int = 0) -> bool:
    if len(str(year)) != 4 or not str(year).isdigit():
        raise ValueError(
            'Metai iš 4 skaičių.')

    year_int = int(year)
    if year_int < 1000 or year_int >= (datetime.now().year - min_age):
        raise ValueError(
            f'Iveskite teisingus metus, negali būti > už {datetime.now().year - min_age}, ir < už 1000.')

    return True


def validate_book_genre(genre: str) -> bool:
    if str(genre) not in GENRES:
        raise InvalidGenreError(genre)

    return True


def validate_password(password: str) -> bool:
    if len(str(password)) < 6 or len(str(password)) > 20:
        raise ValueError(
            'Slaprazodį turi sudaryti ne mažiau nei 6 ir ne daugiau nei 20 simbolių.')

    if re.search(r'\s', password):
        raise ValueError(
            'Slaptažodis turi būti be tarpų.')

    return True


def validate_qty(qty: str | int) -> bool:
    if not str(qty).isdigit():
        raise ValueError('Iveskite kiekį skaičiai.')
    if int(qty) < 1 and int(qty) > 100:
        raise ValueError('Kiekis turi būti nuo 1 iki 100.')

    return True
