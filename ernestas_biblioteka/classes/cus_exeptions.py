class InvalidGenreError(Exception):
    def __init__(self, genre, message="toks žanras neegzistuoja."):
        self.genre = genre
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"'{self.genre}': {self.message} Pasirinkite viena is egzistuojanciu žanrų."


