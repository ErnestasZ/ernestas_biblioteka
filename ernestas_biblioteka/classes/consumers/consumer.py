import uuid
from dataclasses import dataclass
import datetime as dt


@dataclass
class Consumer:
    def __init__(self, name: str, con_year: int, type: str):
        self.name = name
        self.type = type
        self.con_year = con_year
        self.registration_data = dt.datetime.now()
        self.uuid = uuid.uuid4()
