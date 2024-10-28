import ernestas_biblioteka.functions.db_psql_functions as pg_fn
from ernestas_biblioteka.classes.consumers.user import User
# from ernestas_biblioteka.classes.biblioteka import Biblioteka
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.constants import SUPER_LIB, LIB_MIN_AGE, BOOK_OVERDUE_DAYS, MAX_TAKEN_BOOKS
import ernestas_biblioteka.functions.validation_func as v_fn
import ernestas_biblioteka.functions.function as fn
import ernestas_biblioteka.functions.dto_functions as dto_fn
from ernestas_biblioteka.classes_dto.login_user_data import UserTakenBookDTO, LoginUserDataDTO, LoginLibDataDTO


# biblioteka_fn = Biblioteka()
class BibliotekaDB:
    def __init__(self):
        self.log_consumer: LoginUserDataDTO | LoginLibDataDTO = None
        self.librarians = []
        self.__check_default_librarian()
        self.__get_login_consumer()
        # self.__load_loginconsumer()

    def __get_login_consumer(self):
        login_q = """Select user_uuid, librarian_uuid from login"""

        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(login_q)
            log_uuid = c.fetchone()
        if log_uuid['user_uuid']:
            self.log_consumer = self.get_user_with_book(log_uuid['user_uuid'])
            return
        if log_uuid['librarian_uuid']:
            return

    def __check_default_librarian(self):
        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute("""SELECT l.uuid, name, birth_year, password, registration_date
                      FROM librarians l
                      Join consumers c ON consumer_uuid = c.uuid
                      Where name = %s""", (SUPER_LIB['name'], ))
            default_l = c.fetchone()
            if default_l:
                self.librarians.append(Librarian.lib_from_db(default_l))
        if not default_l:
            new_lib = self.add_librarian(
                SUPER_LIB['name'], SUPER_LIB['year'], SUPER_LIB['password'])
            pg_fn.create_librarian(new_lib, pg_fn.db_connection())

        print(default_l)

    def get_books(self, search: str = '', search_type: str = 'author', is_active: bool | None = True):

        if search_type not in ['author', 'title']:
            raise ValueError('Neteisingas paieskos parametras')
        base_query = f"""SELECT 
                    b.uuid as book_uuid,
                    b.*, 
                    count(ur.uuid) as taken_qty
                    From books b
                    Left Join user_records ur ON b.uuid = ur.book_uuid
                    and ur.return_at Is Null
                    Where {search_type} ILIKE %(search)s
                    """
        query_params = {'search': f'%{search}%'}
        if is_active != None:
            base_query += ' and b.is_active = %(is_active)s'
            query_params['is_active'] = is_active
        base_query += ' Group by b.uuid Order by b.title'
        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(
                base_query, query_params)
            results = c.fetchall()
        book_dto = dto_fn.create_books_DTO(results)
        if not book_dto:
            book_dto = []
        return book_dto

    def top_5_genre_by_user(self):
        base_query = """Select b.genre, count(b.genre) as book_count from user_records ur
                        left join books b on ur.book_uuid = b.uuid
                        Group by b.genre 
                        order by book_count DESC
                        Limit 5
                        """
        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(
                base_query)
            results = c.fetchall()
            return results

    def top_5_genre_by_library(self):
        base_query = """Select genre, count(genre) as book_count 
                        from books
                        where is_active = True
                        Group by genre 
                        order by book_count DESC
                        Limit 5
                        """
        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(
                base_query)
            results = c.fetchall()
            return results

    def get_overdue_books(self):
        base_query = """Select b.title, u.name 
                        from user_records ur
                        Join (Select users.uuid, consumers.name from users 
                        Join consumers on users.consumer_uuid = consumers.uuid) u
                        on ur.user_uuid = u.uuid
                        Join books b on ur.book_uuid = b.uuid
                        where ur.return_at Is Null
                        and (NOW() - ur.taken_at) > INTERVAL %(overdue_days)s
                        order by b.title
                        """
        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(
                base_query, {'overdue_days': f'{BOOK_OVERDUE_DAYS} days'})
            results = c.fetchall()
            return results

    def get_book_overdue_mean_stat(self):
        base_query = """SELECT avg(book_count.count) as avg_count
                        FROM (
                            SELECT COUNT(ur.uuid) AS count
                            FROM users AS u
                            JOIN user_records ur ON u.uuid = ur.user_uuid
                            WHERE (
                                (ur.return_at IS NOT NULL 
                                AND (ur.return_at::timestamp - ur.taken_at) > INTERVAL %(overdue_days)s)
                                OR
                                (ur.return_at IS NULL 
                                AND (NOW() - ur.taken_at) > INTERVAL %(overdue_days)s)
                            )
                            GROUP BY u.uuid
                        ) as book_count
                        """
        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(
                base_query, {'overdue_days': f'{BOOK_OVERDUE_DAYS} days'})
            # base_query, {'overdue_days': BOOK_OVERDUE_DAYS})
            results = c.fetchone()[0]
            return results

    def get_users_with_overdue(self):
        base_query = """SELECT 
                        u.uuid
                        c.name, 
                        c.birth_year
                        uc.card_number, 
                        b.*, 
                        count(urc.uuid)
                        From users u
                        Join consumers c On u.consumer_uuid = c.uuid
                        Join user_cards uc On u.card_uuid = uc.uuid
                        Left Join user_records ur On ur.user_uuid = u.uuid
                            AND ur.return_at IS NULL 
                            AND (NOW() - ur.taken_at) > INTERVAL %(overdue_days)s
                        Left Join books b On ur.book_uuid = b.uuid
                        Left Join user_records urc On urc.user_uuid = u.uuid 
                            AND urc.return_at IS NULL
                        GROUP BY c.name, uc.card_number, b.title
                        Order by c.name
                        """
        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(
                base_query, {'overdue_days': f'{BOOK_OVERDUE_DAYS} days'})
            results = c.fetchall()
            return results

    def get_user_with_book(self, user_uuid: str):
        base_query = """Select 
                        u.uuid as user_uuid,
                        c.*, 
                        b.uuid as book_uuid,
                        b.*, 
                        uc.*,
                        (EXTRACT(DAY FROM (NOW() - ur.taken_at)) - %(overdue_days)s) as overdue_days
                        from users u
                        Join consumers c on u.consumer_uuid = c.uuid
                        Join user_cards uc on u.card_uuid = uc.uuid
                        Join user_records ur On u.uuid = ur.user_uuid
                            and return_at Is Null
                        Join books b on ur.book_uuid = b.uuid
                        Where u.uuid = %(user_uuid)s
                        """
        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(
                base_query, {'user_uuid': user_uuid, 'overdue_days': BOOK_OVERDUE_DAYS})
            results = c.fetchall()
        return dto_fn.create_login_user_data_DTO(results)
        # return results

    def add_librarian(self, name: str, birth_year: str, password: str) -> Librarian | bool:
        # ceck name > 2 +
        v_fn.validate_name(name)
        # check birh_year >= 18 +
        v_fn.validate_year(birth_year, LIB_MIN_AGE)
        # check password >=6 Ž
        v_fn.validate_password(password)
        if fn.check_is_librarian_unique(self.librarians, name):
            new_librarian = Librarian(name, birth_year, password)
            # self.librarians.append(new_librarian)
            # self.__save_lib()
            return new_librarian
        raise LookupError(f'Bibliotekininkas tokiu "{name}" vardu egzistuoja')
        # print(f'Bibliotekininkas tokiu "{name}" vardu egzistuoja')
        # return False

    #####
    # Just started, not finished

    def login_user(self, card_number: int):
        # # from db
        # find user by card number
        print('take_book')
        find_user_query = """Select 
                            u.uuid 
                            from users u
                            Join user_cards uc On u.card_uuid = uc.uuid
                            Where uc.card_number = %(card_number)s"""

        clear_login = """TRUNCATE login RESTART IDENTITY"""

        save_login = """INSERT INTO login (user_uuid) Values (%(user_uuid)s)"""

        with pg_fn.db_connection() as conn:
            c = conn.cursor()
            c.execute(
                find_user_query, {'card_number': card_number})
            found_user = c.fetchone()
            print(found_user['uuid'])

            if not found_user:
                raise LookupError("Nerasta skaitytojo kortelė")

            # clear login table
            c.execute(clear_login)

            # save to login table
            c.execute(save_login, {'user_uuid': found_user['uuid']})

        self.log_consumer = self.get_user_with_book(found_user['uuid'])

        # # from class
        # create user class object

        # save to class

    def take_book(self, book: UserTakenBookDTO) -> None:
        # check if login
        # print('gavau')
        self.__check_login_user()
        # check if book has free qty +
        if book.qty <= book.taken_qty:
            raise LookupError('Paimtos visos knygos')
        # check if user can take book by count +
        log_user = self.log_consumer
        if len(log_user) >= MAX_TAKEN_BOOKS:
            raise LookupError('Paemes max kieki knygų')
        # check if user can take book by is not overdue +
        # check if user had book by author and title +
        if len(log_user):
            for u_book in log_user.taken_books_list:
                # print(book.overdue_days)
                if u_book == book:
                    raise LookupError('Jau turi tokia knyga paemes')
                if u_book.overdue_days > 0:
                    raise LookupError('Turi pradelstu grazinti knygu')
        

        # new_user_record = set_take_book(self.log_consumer, book)
        
        # self.records.add_record(new_user_record)
        # self.__save_lib()
        # print("paemete knyga sekmingai")

    def add_book(self, author: str, name: str, release_year: str, genre: str, qty: str | int = 1):
        pass
        # # only register librarian +
        # self.__check_login_lib()
        # # check if book exist
        # for book in self.books:
        #     if author == book.author and name == book.name:
        #         raise LookupError(
        #             'Tokia knyga jau yra binbliotekoje, pakeiskite kiekį.')
        # # check author non digits only letters > 3 +
        # # check name > 0 +
        # # relese date 4 digits and year <= current year +
        # # genre from Genre List +
        # # check qty is int
        # new_book = fn.create_book(
        #     author.strip(), name, release_year, genre, qty)
        # # create lib records
        # self.records.add_record(LibRecords(self.log_consumer, new_book, 'add'))
        # # self.books.append(new_book)
        # # self.__save_lib()
        # return new_book

    def __check_login_user(self) -> None:
        if self.log_consumer == None or not isinstance(self.log_consumer, LoginUserDataDTO):
            raise LookupError('Turi buti prisijunges skaitytojas')
