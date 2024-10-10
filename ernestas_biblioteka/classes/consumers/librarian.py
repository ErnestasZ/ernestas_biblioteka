from ernestas_biblioteka.classes.consumers.consumer import Consumer


class Librarian(Consumer):
    def __init__(self, name: str,  con_year: int, password: str):
        super().__init__(name, con_year, type='bibliotekininkas')
        self.password = password

    def __str__(self):
        return f'{self.type} - {self.name}, dirba nuo {self.registration_data}'
    

