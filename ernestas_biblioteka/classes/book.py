from dataclasses import dataclass
from ernestas_biblioteka.constants import GENRES
from ernestas_biblioteka.classes.cus_exeptions import InvalidGenreError


@dataclass
class Book:
    def __init__(self, author: str, name: str, release_year: int, genre: str):
        if genre not in GENRES:
            raise InvalidGenreError(genre)
        self.author = author
        self.name = name
        self.release_year = release_year
        self.genre = genre

    def __str__(self) -> str:
        return f'"{self.name}" - {self.author}, išleista {self.release_year}m. ({self.genre})'

    def __repr__(self) -> str:
        return f'"{self.name}" - {self.author}, išleista {self.release_year}m. ({self.genre})'
