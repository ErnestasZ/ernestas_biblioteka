import streamlit as st
# from datetime import datetime, timedelta
from ernestas_biblioteka.classes.biblioteka import Biblioteka
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.streamlit.functions.fn_lib_login import login_librarian_box
from ernestas_biblioteka.streamlit.functions.fn_lib_stat import lib_stat_box
from ernestas_biblioteka.streamlit.functions.fn_lib_add_book import lib_add_book_box
from ernestas_biblioteka.streamlit.functions.fn_lib_books_users import books_users_box


if 'new_lib' not in st.session_state:
    st.session_state["new_lib"] = Biblioteka()

new_lib = st.session_state["new_lib"]


st.title('Bibliotekininkams')

# login lib section
login_librarian_box(new_lib)

if (new_lib.log_consumer != None) and (isinstance(new_lib.log_consumer, Librarian)):
    # stat box
    lib_stat_box(new_lib)

    # add book
    lib_add_book_box(new_lib)
    # remove book by years

    # all buttons
    # all_books, overdue_book, all_users
    books_users_box(new_lib)
