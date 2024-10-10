from ernestas_biblioteka.constants import GENRES
from dataclasses import dataclass


class InvalidGenreError(Exception):
    """Kai netinkamas zanras"""
    pass


@dataclass
class Book:
    def __init__(self, author: str, name: str, release_year: int, genre: str):
        if genre not in GENRES:
            raise InvalidGenreError(
                f"Žanras '{genre}' neegzistuoja. Pasirinkite viena is egzistuojanciu žanrų.")
        self.author = author
        self.name = name
        self.release_year = release_year
        self.genre = genre

    def __str__(self) -> str:
        return f'"{self.name}" - {self.author}, išleista {self.release_year}m. ({self.genre})'

    def __repr__(self) -> str:
        return f'"{self.name}" - {self.author}, išleista {self.release_year}m. ({self.genre})'
