import streamlit as st
from ernestas_biblioteka.constants import GENRES


def lib_add_book_box(new_lib):
    if 'book_title' not in st.session_state:
        st.session_state['book_title'] = ''
    if 'author' not in st.session_state:
        st.session_state['author'] = ''
    if 'book_year' not in st.session_state:
        st.session_state['book_year'] = ''
    if 'book_genre' not in st.session_state:
        st.session_state['book_genre'] = None
    if 'book_qty' not in st.session_state:
        st.session_state['book_qty'] = 1

    if 'book_add_err' not in st.session_state:
        st.session_state['book_add_err'] = ''
    if 'book_add_succ' not in st.session_state:
        st.session_state['book_add_succ'] = ''

    def clear_book_input():
        st.session_state['book_title'] = ''
        st.session_state['author'] = ''
        st.session_state['book_year'] = ''
        st.session_state['book_genre'] = None
        st.session_state['book_qty'] = 1

    def add_book():
        title = st.session_state['book_title']
        author = st.session_state['author']
        year = st.session_state['book_year']
        genre = st.session_state['book_genre']
        qty = st.session_state['book_qty']
        try:
            book = new_lib.add_book(author, title, year, genre, qty)
            st.session_state['book_add_succ'] = 'Knyga išsaugota'
            clear_book_input()
        except LookupError as err:
            st.session_state['book_add_err'] = str(err)
        except ValueError as err:
            st.session_state['book_add_err'] = str(err)
        except Exception as err:
            st.session_state['book_add_err'] = str(err)

    with st.expander("Pridėti naują knygą"):
        title = st.text_input(
            "Knygos pavadinimas", key='book_title', placeholder='Įveskite pavadinimą')

        author = st.text_input("Autorius", key='author',
                               placeholder='Įveskite Vardas Pavardė')

        col_year, col_genre = st.columns(2)
        with col_year:
            year = col_year.text_input(
                "Išleidimo metai", key='book_year', placeholder='MMMM')

            qty = col_year.number_input(
                'Knygų kiekis', 1, 10, step=1, key='book_qty')

        with col_genre:
            genre = col_genre.selectbox(
                "Knygos žanras:",
                (GENRES),
                key='book_genre',
                index=None,
                placeholder="Pasirinkite žanrą..."
            )

        st.button(label="Išsaugoti knygą", key='add_book',
                  type="primary", on_click=add_book, use_container_width=True)

        if st.session_state['book_add_err']:
            st.markdown(f':red[{st.session_state["book_add_err"]}]')
            st.session_state['book_add_err'] = ''
        if st.session_state['book_add_succ']:
            st.markdown(f':green[{st.session_state["book_add_succ"]}]')
            st.session_state['book_add_succ'] = ''

    if 'remove_err' not in st.session_state:
        st.session_state['remove_err'] = ''

    if 'remove_succ' not in st.session_state:
        st.session_state['remove_succ'] = ''

    def remove_books():
        # year = args
        st.session_state['remove_err'] = ''
        year = st.session_state['before_year']
        try:
            book = new_lib.remove_book_before_years(year)
            st.session_state['remove_succ'] = 'Knygos isimtos'
            st.session_state['before_year'] = ''
        except LookupError as err:
            st.session_state['remove_err'] = str(err)
        except ValueError as err:
            st.session_state['remove_err'] = str(err)
        except Exception as err:
            st.session_state['remove_err'] = str(err)

    with st.expander("Išimti knygas pagal metus"):
        st.write("išimti visas knygas iki pasirinktų metų")
        col_year, col_genre = st.columns(2)
        with col_year:
            year = col_year.text_input(
                "Išleidimo metai", key='before_year', placeholder='MMMM')

        st.button(label="Išimti knygas", key='remove', on_click=remove_books,
                  type="primary", use_container_width=True)
        if st.session_state['remove_err']:
            st.markdown(f':red[{st.session_state["remove_err"]}]')
            st.session_state['remove_err'] = ''
        if st.session_state['remove_succ']:
            st.markdown(f':green[{st.session_state["remove_succ"]}]')
            st.session_state['remove_succ'] = ''
