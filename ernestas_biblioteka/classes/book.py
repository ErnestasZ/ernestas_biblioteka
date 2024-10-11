import uuid
from dataclasses import dataclass
from datetime import datetime as dt
from ernestas_biblioteka.constants import GENRES
from ernestas_biblioteka.classes.cus_exeptions import InvalidGenreError
# from ernestas_biblioteka.classes.consumers.user import User


@dataclass
class Book:
    def __init__(self, author: str, name: str, release_year: int, genre: str):
        if genre not in GENRES:
            raise InvalidGenreError(genre)
        self.author = author
        self.name = name
        self.release_year = release_year
        self.genre = genre
        self.taken_at: dt = None
        self.is_active: bool = True
        self.uuid = uuid.uuid4()

    def set_taken(self):
        self.taken_at = dt.now()

    def set_return(self):
        self.taken_at = None

    def set_remove(self):
        self.is_active = False

    def eq_book(self, other) -> bool:
        if isinstance(other, Book):
            return self.name == other.name and self.author == other.author
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, Book):
            return self.uuid == other.uuid
        return False

    def __str__(self) -> str:
        return f'"{self.name}" - {self.author}, išleista {self.release_year}m. ({self.genre})'

    def __repr__(self) -> str:
        return f'"{self.name}" - {self.author}, išleista {self.release_year}m. ({self.genre})'
