import psycopg2
import random
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.classes.records import UserRecords, LibRecords
from ernestas_biblioteka.classes.book import Book
from dotenv import load_dotenv
import os


# try:
#     with conn:
#         c = conn.cursor()
#         # Run a simple query to confirm connectivity
#         c.execute("SELECT version();")
#         db_version = c.fetchone()
#         print("Database version:", db_version)

# except psycopg2.DatabaseError as e:
#     print('Klaida', e)


def db_connection():
    load_dotenv()

    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn


def create_tables():
    conn = db_connection()

    try:
        with conn:
            c = conn.cursor()

            # Enable the uuid-ossp extension for UUID generation
            c.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

            # Create consumers table with uuid as primary key
            c.execute("""CREATE TABLE IF NOT EXISTS consumers (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                name VARCHAR(255) NOT NULL,
                birth_year SMALLINT NOT NULL
            )""")

            # Create user_cards table with uuid as primary key
            c.execute("""CREATE TABLE IF NOT EXISTS user_cards (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                card_number BIGINT NOT NULL UNIQUE  
            )""")

            # Create users table with uuid as primary key
            c.execute("""CREATE TABLE IF NOT EXISTS users (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                consumer_uuid UUID,
                card_uuid UUID,
                FOREIGN KEY (consumer_uuid) REFERENCES consumers(uuid),
                FOREIGN KEY (card_uuid) REFERENCES user_cards(uuid)
            )""")

            # Create librarians table with uuid as primary key
            c.execute("""CREATE TABLE IF NOT EXISTS librarians (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                consumer_uuid UUID,
                password VARCHAR(255) NOT NULL,  
                FOREIGN KEY (consumer_uuid) REFERENCES consumers(uuid)
            )""")

            # Create login table with uuid as primary key
            c.execute("""CREATE TABLE IF NOT EXISTS login (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                librarian_uuid UUID DEFAULT NULL,
                user_uuid UUID DEFAULT NULL,
                FOREIGN KEY (librarian_uuid) REFERENCES librarians(uuid),
                FOREIGN KEY (user_uuid) REFERENCES users(uuid)
            )""")

            # Create books table with uuid as primary key
            c.execute("""CREATE TABLE IF NOT EXISTS books (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                author VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                release_year SMALLINT NOT NULL,  -- Used SMALLINT as years typically range from 1900-2100
                genre VARCHAR(100) NOT NULL,  -- Specified a length for genre
                qty SMALLINT NOT NULL,  -- Used SMALLINT for quantity
                is_active BOOLEAN DEFAULT TRUE
            )""")

            # Create lib_records table with uuid as primary key
            c.execute("""CREATE TABLE IF NOT EXISTS lib_records (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                type VARCHAR(255) NOT NULL,
                action_date DATE DEFAULT CURRENT_DATE,
                librarian_uuid UUID,
                book_uuid UUID,
                FOREIGN KEY (librarian_uuid) REFERENCES librarians(uuid),
                FOREIGN KEY (book_uuid) REFERENCES books(uuid)
            )""")

            # Create user_records table with uuid as primary key
            c.execute("""CREATE TABLE IF NOT EXISTS user_records (
                uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                taken_at DATE DEFAULT CURRENT_DATE,
                return_at DATE,
                user_uuid UUID,
                book_uuid UUID,
                FOREIGN KEY (user_uuid) REFERENCES users(uuid),
                FOREIGN KEY (book_uuid) REFERENCES books(uuid)
            )""")
    except psycopg2.DatabaseError as e:
        print('Klaida:', e)


# create_tables()


def create_user_db(user: User, conn: psycopg2):
    c = conn.cursor()

    # try:
    consumer_id = create_consumer(user, c)
    # return (consumer_id)

    print('consumer id', consumer_id)
    # create user card
    card_id = create_and_get_card_id(conn)

    print('Consumer and card ids', consumer_id, card_id)

    c.execute("""INSERT INTO users (uuid, card_uuid, consumer_uuid)
            Values (%s, %s, %s)""", (str(user.uuid), card_id, consumer_id))
    # except psycopg2.DatabaseError as e:
    #     print("Klaida", e)


def create_consumer(consumer: User | Librarian, cursor: psycopg2):
    cursor.execute("""INSERT INTO consumers (name, birth_year)
                Values (%s, %s)
                RETURNING uuid""", (consumer.name, consumer.con_year))
    consumer_id = cursor.fetchone()[0]
    print(consumer_id)
    return consumer_id


def create_and_get_card_id(conn) -> int:
    c = conn.cursor()

    while True:
        card_number = ''.join(
            [str(random.randint(1, 9)) for _ in range(8)])
        c.execute("""SELECT 1 FROM user_cards 
              WHERE card_number = (%s)""", (card_number, ))
        result = c.fetchone()

        if not result:
            # try:
            c.execute("""INSERT INTO user_cards (card_number) 
                          VALUES (%s)
                      RETURNING uuid""", (card_number,))
            card_id = c.fetchone()[0]
            print('Kortele sukurta', card_id)
            return card_id
            # except psycopg2.DatabaseError as e:
            #     print('Klaida', e)


def create_librarian(librarian: Librarian, conn: psycopg2):
    c = conn.cursor()
    consumer_id = create_consumer(librarian, c)
    c.execute("""INSERT INTO librarians (uuid, password, consumer_uuid)
                Values (%s,%s,%s)""", (str(librarian.uuid), librarian.get_password(), consumer_id))


def create_book(book: Book, conn: psycopg2):
    c = conn.cursor()
    c.execute("""INSERT INTO books (uuid, author, title, release_year, qty, genre, is_active)
              Values (%s,%s,%s,%s,%s,%s,%s)""", (str(book.uuid), book.author, book.name, book.release_year, book.qty, book.genre, book.is_active))


def create_user_record(user_record: UserRecords, conn: psycopg2):
    c = conn.cursor()
    c.execute("""INSERT INTO user_records (user_uuid, book_uuid, taken_at, return_at)
              Values (%s,%s,%s,%s)""", (str(user_record.user.uuid), str(user_record.book.uuid), user_record.pick_up_date, user_record.return_date))


def create_lib_record(lib_record: LibRecords, conn: psycopg2):
    c = conn.cursor()
    c.execute("""INSERT INTO lib_records (librarian_uuid, book_uuid, type, action_date)
              Values (%s,%s,%s,%s)""", (str(lib_record.librarian.uuid), str(lib_record.book.uuid), lib_record.type, lib_record.date))
