from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Uuid, Boolean, ForeignKey, text, create_engine, and_, or_
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import text, exists
from datetime import datetime
from ernestas_biblioteka.orm.functions.db_function import db_connection
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from ernestas_biblioteka.orm.classes.records import UserRecord

Base = declarative_base()
# Session, engine = db_connection()
# session = Session()


class Book(Base):
    __tablename__ = ('books')
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    author = Column(String(255))
    title = Column(String(255))
    release_year = Column(Integer)
    qty = Column(Integer)
    genre = Column(String(255))
    is_active = Column(Boolean, default=True)
    # user_records = relationship('UserRecord', back_populates='book')

    def __init__(self, author, title, release_year, genre, qty=1, is_active=True):
        self.author = author
        self.title = title
        self.release_year = release_year
        self.qty = qty
        self.genre = genre
        self.is_active = is_active


# all_book = session.query(Book).filter(
#     Book.is_active.is_(True)).all()

# for book in all_book:
#     print(book.title)
