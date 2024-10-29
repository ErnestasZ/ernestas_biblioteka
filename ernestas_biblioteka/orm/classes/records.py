from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Uuid, ForeignKey, text, create_engine, and_, or_
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import text, exists
from datetime import datetime
from ernestas_biblioteka.orm.classes.consumer import User
# from ernestas_biblioteka.orm.classes.book import Book
from ernestas_biblioteka.orm.functions.db_function import db_connection


# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from ernestas_biblioteka.orm.classes.consumer import User

Base = declarative_base()
# Session, engine = db_connection()
# session = Session()


class UserRecord(Base):
    __tablename__ = 'user_records'
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    user_uuid = Column(Uuid, ForeignKey('users.uuid'))
    book_uuid = Column(Uuid, ForeignKey('books.uuid'))
    taken_at = Column(DateTime, default=datetime.now())
    return_at = Column(DateTime, nullable=True)
    user = relationship(User, backref="user_records")
    # book = relationship('Book', backref="user_records")

    def __init__(self, user_uuid, book_uuid, return_at=None):
        self.user_uuid = user_uuid
        self.book_uuid = book_uuid
        self.return_at = return_at


# Base.metadata.create_all(engine)

# all_taken_book = session.query(UserRecord).filter(
#     UserRecord.return_at.is_(None)).all()

# for rec in all_taken_book:
#     print(rec.taken_at)
