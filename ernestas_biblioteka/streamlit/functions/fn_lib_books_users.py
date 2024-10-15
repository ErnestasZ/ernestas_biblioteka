import streamlit as st
from datetime import datetime
from ernestas_biblioteka.constants import BOOK_OVERDUE_DAYS
# from typing import Literal


def all_books(new_lib):
    st.subheader(f"***visos knygos***")

    books = new_lib.books

    for book in books:
        container = st.container(border=True)
        # col1, col2 = container.columns([3, 1])

        # with col1:
        if not book.is_active:
            container.markdown(f'📚 :red[**Išimta**]')
        container.markdown(f':book: **{book.name}**')
        container.markdown(f"""*Author:* {book.author} | {book.release_year} y.      
*{book.genre}*          
Qty: {book.qty} / taken: {len(book.taken_by)}""")


def overdue_books(new_lib):
    st.subheader(f"***pradelstos knygos***")

    books = new_lib.get_overdue_books()
    for book, user in books:
        # print(book)
        container = st.container(border=True)
        col1, col2 = container.columns([3, 1])

        with col1:
            if not book.is_active:
                col1.markdown(f'📚 :red[**Išimta**]')
            col1.markdown(f':book: **{book.name}**')
            col1.markdown(f"""*Author:* {book.author} | {book.release_year} y.  
    *{book.genre}*   
    Qty: {book.qty} / taken: {len(book.taken_by)}""")

        with col2:
            col2.markdown(f'**Skaitytojas**')
            col2.markdown(f"""*{user.name}*""")
            taken_book = next(
                (taken_book for taken_book in user.taken_books if taken_book.book == book), None)
            overdue_days = (datetime.now() -
                            taken_book.taken_at).days - BOOK_OVERDUE_DAYS
            col2.markdown(f""":red[Pradelsta {overdue_days} d.]""")


def all_users(new_lib):
    st.subheader(f"***visi skaitytojai***")

    users = new_lib.users
    for user in users:
        container = st.container(border=True)
        container.markdown(
            f"""***{user.name}*** - Nr: {user.user_card.card_number}
        (Paimta: {len(user.taken_books)} knyg)""")
        # user_container.divider()
        over_books = new_lib.get_overdue_books_by_user(user)
        container.markdown('Pradelstos knygos:')
        if not over_books:
            container.markdown(f':green[*Nėra*]')
        for ov_book in over_books:
            container.markdown(f':red[*"{ov_book.name}"*]')

        print(over_books)


def books_users_box(new_lib):
    st.subheader('Knygos ir skaitytojai', divider=True)
    # ['all_books', 'overdue_books', 'all_users']
    if 'lib_status' not in st.session_state:
        st.session_state['lib_status'] = 'all_books'

    col1, col2, col3 = st.columns(3)

    with col1:
        if col1.button("Visos knygos", type='primary', use_container_width=True):
            st.session_state['lib_status'] = 'all_books'
    with col2:
        if col2.button("Pradelstos knygos", type='secondary',
                       use_container_width=True):
            st.session_state['lib_status'] = 'overdue_books'
    with col3:
        if col3.button("Skaitytojai", type='secondary', use_container_width=True):
            st.session_state['lib_status'] = 'all_users'

    if st.session_state['lib_status'] == 'all_books':
        all_books(new_lib)

    if st.session_state['lib_status'] == 'overdue_books':
        overdue_books(new_lib)

    if st.session_state['lib_status'] == 'all_users':
        all_users(new_lib)
