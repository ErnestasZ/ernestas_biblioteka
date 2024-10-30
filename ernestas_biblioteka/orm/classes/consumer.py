from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Uuid, Boolean, ForeignKey, CheckConstraint, text, create_engine, and_, or_
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import text, exists
from datetime import datetime
import random
import bcrypt
from ernestas_biblioteka.orm.functions.db_function import db_connection

# from sqlalchemy.ext.declarative import declarative_base
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
# from ernestas_biblioteka.orm.classes.records import UserRecord

Base = declarative_base()

# engine = create_engine(DATABASE_URL)
# Base = declarative_base()

# Session = sessionmaker(bind=engine)

Session, engine = db_connection()
session = Session()


class Consumer(Base):
    __tablename__ = 'consumers'
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    name = Column(String(255))
    birth_year = Column(Integer)
    registration_date = Column(DateTime, default=datetime.now())

    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year


class UserCard(Base):
    __tablename__ = 'user_cards'
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    card_number = Column(Integer, unique=True)

    def __init__(self, session):
        self.card_number = self.__generate_unique_number(session)

    def __generate_unique_number(self, session):
        while True:
            number = int(self.__generate_number())
            if not session.query(UserCard).filter_by(card_number=number).first():
                return number

    def __generate_number(self):
        card_number = ''.join(
            [str(random.randint(1, 9)) for _ in range(8)])
        return card_number


class User(Base):
    __tablename__ = 'users'
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    card_uuid = Column(Uuid, ForeignKey('user_cards.uuid'))
    consumer_uuid = Column(Uuid, ForeignKey('consumers.uuid'))
    consumer = relationship("Consumer", backref="users")
    card = relationship("UserCard", backref="users")
    # user_records = relationship('UserRecord', back_populates='user')

    def __init__(self, name, birth_year, session):
        self.consumer = Consumer(name, birth_year)
        self.card = UserCard(session)


class Librarian(Base):
    __tablename__ = 'librarians'
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    consumer_uuid = Column(Uuid, ForeignKey('consumers.uuid'))
    password = Column(String(255))
    consumer = relationship("Consumer", backref="librarians")

    def __init__(self, name, birth_year, password):
        self.consumer = Consumer(name, birth_year)
        self.password = self.__hash_password(password)

    def __hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()


class Login(Base):
    __tablename__ = 'login'
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    user_uuid = Column(Uuid, ForeignKey('users.uuid'), nullable=True)
    librarian_uuid = Column(Uuid, ForeignKey('librarians.uuid'), nullable=True)
    user = relationship("User", backref="login")
    lib = relationship("Librarian", backref="login")

    def __init__(self, session, user_uuid=None, librarian_uuid=None):
        if user_uuid and session.query(exists().where(User.uuid == user_uuid)).scalar():
            self.clear_logins(session)
            self.user_uuid = user_uuid
        elif librarian_uuid and session.query(exists().where(Librarian.uuid == librarian_uuid)).scalar():
            self.clear_logins(session)
            self.librarian_uuid = librarian_uuid
        else:
            raise ValueError("Tokio vartotojo nera")

    @staticmethod
    def clear_logins(session):
        session.query(Login).delete()
        session.commit()


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


class UserRecord(Base):
    __tablename__ = 'user_records'
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    user_uuid = Column(Uuid, ForeignKey('users.uuid'))
    book_uuid = Column(Uuid, ForeignKey('books.uuid'))
    taken_at = Column(DateTime, default=datetime.now())
    return_at = Column(DateTime, nullable=True)
    user = relationship('User', backref="user_records")
    book = relationship('Book', backref="user_records")

    def __init__(self, user_uuid, book_uuid, return_at=None):
        self.user_uuid = user_uuid
        self.book_uuid = book_uuid
        self.return_at = return_at


class LibRecord(Base):
    __tablename__ = 'lib_records'
    uuid = Column(Uuid, primary_key=True,
                  server_default=text("uuid_generate_v4()"))
    type = Column(String(255), nullable=False)
    __table_args__ = (
        CheckConstraint("type IN ('add', 'remove')", name='check_action_type'),
    )
    action_date = Column(DateTime, default=datetime.now())
    librarian_uuid = Column(Uuid, ForeignKey('librarians.uuid'))
    book_uuid = Column(Uuid, ForeignKey('books.uuid'))
    lib = relationship('Librarian', backref="lib_records")
    book = relationship('Book', backref="lib_records")

    def __init__(self, librarian_uuid, book_uuid, type='add'):
        self.librarian_uuid = librarian_uuid
        self.book_uuid = book_uuid
        self.type = type
# new_user = User(name="Alice", birth_year=1990, session=session)
# session.add(new_user)
# session.commit()


# new_lib = Librarian(name="Kazys", birth_year=1985, password='seacret123')
# session.add(new_lib)
# session.commit()

# results = session.query(User).all()
# for user in results:
#     print(user.consumer.name)

# login_user = Login(
#     session=session, user_uuid='98271220-877f-470f-aeca-b0abdcb5f74f')
# session.add(login_user)
# session.commit()

# session.close()
# all_taken_book = session.query(UserRecord).filter(
#     UserRecord.return_at.is_(None)).all()

# for rec in all_taken_book:
#     print(rec.user.consumer.name, rec.book.title)

all_added_books = session.query(LibRecord).filter(
    LibRecord.type == 'add').all()

for rec in all_added_books:
    print(rec.lib.consumer.name, rec.book.title)
