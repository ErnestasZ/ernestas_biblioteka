import sqlite3
import random
from ernestas_biblioteka.constants import LIBRARY_DB
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.classes.records import UserRecords
from ernestas_biblioteka.classes.book import Book


def create_tables():
    try:
        with sqlite3.connect(LIBRARY_DB) as conn:
            c = conn.cursor()

            # create consumers
            c.execute("""CREATE TABLE IF NOT EXISTS consumers
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birth_year INTEGER NOT NULL)
                    """)

            # Create user_cards table
            c.execute("""CREATE TABLE IF NOT EXISTS user_cards
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_number INTEGER NOT NULL UNIQUE) """)

            # Create users table
            c.execute("""CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      consumer_id INTEGER,
                      card_id INTEGER,
                      FOREIGN KEY (consumer_id) REFERENCES consumers(id),
                      FOREIGN KEY (card_id) REFERENCES user_cards(id)
                    )""")

            # Create librarians table
            c.execute("""CREATE TABLE IF NOT EXISTS librarians
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      consumer_id INTEGER,
                      password TEXT NOT NULL,
                      FOREIGN KEY (consumer_id) REFERENCES consumers(id)
                    )""")

            # Create librarians table
            c.execute("""CREATE TABLE IF NOT EXISTS login
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      librarian_id INTEGER default NULL,
                      user_id INTEGER default NULL,
                      FOREIGN KEY (librarian_id) REFERENCES librarians(id)
                      FOREIGN KEY (user_id) REFERENCES users(id)
                    )""")

            # Create books table
            c.execute("""CREATE TABLE IF NOT EXISTS books
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      author TEXT NOT NULL,
                      title TEXT NOT NULL,
                      release_year INTEGER NOT NULL,
                      genre TEXT NOT NULL,
                      qty INTEGER NOT NULL,
                      is_active INTEGER NOT NULL DEFAULT 0)""")

            # Create lib_records table
            c.execute("""CREATE TABLE IF NOT EXISTS lib_records
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type VARCHAR(255) NOT NULL,
                    action_date DATE DEFAULT (DATE('now')),
                    librarian_id INTEGER,
                    book_id INTEGER,
                    FOREIGN KEY (librarian_id) REFERENCES librarians(id),
                    FOREIGN KEY (book_id) REFERENCES books(id)
                    )""")

            # Create user_records table
            c.execute("""CREATE TABLE IF NOT EXISTS user_records
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    taken_at DATE DEFAULT (DATE('now')),
                    return_at DATE,
                    user_id INTEGER,
                    book_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (book_id) REFERENCES books(id)
                    )""")
    except sqlite3.Error as e:
        print('Klaida:', e)


def setLogin():
    pass


def create_user_db(user: User, conn: sqlite3):
    c = conn.cursor()

    try:
        consumer_id = create_consumer(user, c)

        print('consumer id', consumer_id)
        # create user card
        card_id = create_and_get_card_id(conn)

        print('Consumer and card ids', consumer_id, card_id)

        c.execute("""INSERT INTO users (card_id, consumer_id)
                Values (?,?)""", (card_id, consumer_id))
    except sqlite3.Error as e:
        print("Klaida", e)


def create_consumer(consumer: User | Librarian, cursor: sqlite3):
    cursor.execute("""INSERT INTO consumers (name, birth_year)
                Values (?,?)""", (consumer.name, consumer.con_year))
    consumer_id = cursor.lastrowid
    return consumer_id


def create_and_get_card_id(conn) -> int:
    c = conn.cursor()

    while True:
        card_number = ''.join(
            [str(random.randint(1, 9)) for _ in range(8)])
        c.execute("""SELECT 1 FROM user_cards 
              WHERE card_number = (?)""", (card_number, ))
        result = c.fetchone()

        if not result:
            try:
                c.execute("""INSERT INTO user_cards (card_number) 
                          VALUES (?)""", (card_number,))
                card_id = c.lastrowid
                print('Kortele sukurta', card_id)
                return card_id
            except sqlite3.Error as e:
                print('Klaida', e)


def create_librarian(librarian: Librarian, conn: sqlite3):
    c = conn.cursor()
    consumer_id = create_consumer(librarian, c)
    c.execute("""INSERT INTO librarians (password, consumer_id)
                Values (?,?)""", (librarian.get_password(), consumer_id))


def create_book(book: Book, conn: sqlite3):
    c = conn.cursor()
    c.execute("""INSERT INTO books (author, title, release_year, qty, genre, is_active)
              Values (?,?,?,?,?,?)""", (book.author, book.name, book.release_year, book.qty, book.genre, book.is_active))


def create_user_record(user_record: UserRecords, conn: sqlite3):
    c = conn.cursor()
    c.execute("""INSERT INTO user_records (user_id, book_id, taken_at, return_at)
              Values (?,?,?,?)""", (user_record.user.id, user_record.book.id, user_record.pick_up_date, user_record.return_date))