import streamlit as st
from datetime import datetime, timedelta
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.constants import MAX_TAKEN_BOOKS, BOOK_OVERDUE_DAYS


def user_search_book(new_lib):
    search_books = None

    def clear_search():
        st.session_state["search"] = ""
        search_book = new_lib.active_books()
        return search_book

    def search_by_author(input):
        st.session_state['search_author_err'] = ''
        try:
            search_books = new_lib.find_by_author(input)
            return search_books
        except LookupError as err:
            st.session_state['search_author_err'] = str(err)
        except ValueError as err:
            st.session_state['search_author_err'] = str(err)
        # st.session_state['search_err'] = ''

    def search_by_title(input):
        st.session_state['search_title_err'] = ''
        try:
            search_books = new_lib.find_by_book_tite(input)
            print(search_books)
            return search_books
        except LookupError as err:
            st.session_state['search_title_err'] = str(err)
        except ValueError as err:
            st.session_state['search_title_err'] = str(err)

    search_container = st.container(border=True)

    text_input = search_container.text_input(
        "Knygų paieška",
        # "pavadinimą arba autorių",
        key="search",
        placeholder="įvesk pavadinimą arba autorių"

    )
    col1, col2, col3 = search_container.columns(3)
    with col1:
        col1.button(label="visos knygos", key='clear', on_click=clear_search,
                    type="primary", use_container_width=True)

    with col2:
        if col2.button(label="Pagal autorių", key='author',
                       type="secondary", use_container_width=True):
            if search_by_author(text_input) != None:
                search_books = search_by_author(text_input)
            if st.session_state['search_author_err']:
                search_container.markdown(
                    f":red[{st.session_state['search_author_err']}]")
                st.session_state['search_author_err'] = ''
    with col3:
        if col3.button(label="Pagal pavadinimą", key='title',
                       type="secondary", use_container_width=True):
            if search_by_title(text_input) != None:
                search_books = search_by_title(text_input)
            if st.session_state['search_title_err']:
                search_container.markdown(
                    f":red[{st.session_state['search_title_err']}]")
                st.session_state['search_title_err'] = ''

    return search_books
