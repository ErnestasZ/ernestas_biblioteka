# from db_connection import db_connection
# from models.user import User
# from models.user_record import UserRecord

from ernestas_biblioteka.orm.classes.records import UserRecord
from ernestas_biblioteka.orm.classes.book import Book
from ernestas_biblioteka.orm.classes.consumer import User
from ernestas_biblioteka.orm.functions.db_function import db_connection


Session, engine = db_connection()
session = Session()
# Example: Using session for a query
all_taken_book = session.query(UserRecord).filter(
    UserRecord.return_at.is_(None)).all()

for rec in all_taken_book:
    print(rec.taken_at)  # Close session after using it
# results = session.query()
