import random
from faker import Faker
from datetime import datetime, timedelta
from ernestas_biblioteka.constants import USER_MIN_AGE, GENRES, SUPER_LIB
from ernestas_biblioteka.classes.biblioteka import Biblioteka


fake = Faker()


def create_user_list(user_num: int) -> list:
    current_year = datetime.now().year
    earliest_birth_year = current_year - USER_MIN_AGE

    unique_names = set()
    user_data = []

    while len(user_data) < user_num:
        name = fake.name()
        birth_year = random.randint(1910, earliest_birth_year)

        if name not in unique_names:
            unique_names.add(name)
            user_data.append({
                'name': name,
                'birth_year': birth_year
            })

    return user_data


def create_book_list(book_num: int) -> list:
    min_year = 1800
    current_year = datetime.now().year
    books = []
    for _ in range(book_num):
        author_name = fake.name()
        book_title = fake.sentence(nb_words=random.randint(2, 5)).rstrip('.')
        release_year = random.randint(min_year, current_year)
        selected_genre = random.sample(GENRES, 1)[0]

        book_entry = {
            'author': author_name,
            'title': book_title,
            'release_year': release_year,
            'genre': selected_genre,
            'qty': random.randint(1, 3)
        }

        books.append(book_entry)

    return books


def create_books_from_list(biblioteka: Biblioteka, books_list: list) -> None:
    biblioteka.login_librarian(SUPER_LIB['name'], SUPER_LIB['password'])

    for book in books_list:
        try:
            biblioteka.add_book(book['author'], book['title'],
                                book['release_year'], book['genre'], book['qty'])
        except Exception as err:
            print(err)
            continue

    print('Knygos sukeltos')


def create_user_and_records_history(biblioteka: Biblioteka, users_list) -> None:
    book_indeces = list(range(len(biblioteka.books)))
    for user in users_list:
        try:
            user = biblioteka.add_user(user['name'], user['birth_year'])
        except Exception as err:
            print(err)
            continue

        unique_indices = random.sample(book_indeces, 4)
        for i in unique_indices:
            book = biblioteka.books[i]
            try:
                user_record = biblioteka.take_book_fake(
                    biblioteka.books[i], user)
            except Exception as err:
                print(err)
                continue
            taken_book = next(
                (taken_book for taken_book in user.taken_books if taken_book.book == book), None)
            # set pick_up and taken_at, return date
            pick_up_date, return_date = generate_rand_date(30)
            user_record.pick_up_date = pick_up_date
            taken_book.taken_at = pick_up_date
            user_record.return_date = return_date


def generate_rand_date(max_day_before):
    current_date = datetime.now()
    start_date = current_date - timedelta(days=max_day_before)
    random_pick_days = random.randint(0, max_day_before)
    random_return_days = random.randint(0, random_pick_days)

    random_pick_date = start_date + timedelta(days=random_pick_days)
    # if random.choice([True, False]):
    #     rand_return_date = start_date + timedelta(days=random_return_days)
    # else:
    #     rand_return_date = None
    rand_return_date = None
    return random_pick_date, rand_return_date
