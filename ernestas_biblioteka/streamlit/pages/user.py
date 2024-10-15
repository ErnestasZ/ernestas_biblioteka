import streamlit as st
# from datetime import datetime, timedelta
# import pandas as pd
from ernestas_biblioteka.classes.biblioteka import Biblioteka
# from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.streamlit.functions.function import login_user_box
from ernestas_biblioteka.streamlit.functions.fn_user_card import user_card_box
from ernestas_biblioteka.streamlit.functions.fn_user_search import user_search_book
# from ernestas_biblioteka.constants import SUPER_CARD_NUM, MAX_TAKEN_BOOKS, BOOK_OVERDUE_DAYS

# new_lib = Biblioteka()

if 'new_lib' not in st.session_state:
    st.session_state["new_lib"] = Biblioteka()

new_lib = st.session_state["new_lib"]


st.title('Sveikas skaitytojau')


# login user section
login_user_box(new_lib)


active_books = new_lib.active_books()

# user card
user_card_box(new_lib)


#################################
st.subheader("Pasirink knygą.")


# search active book
search_book = user_search_book(new_lib)
if search_book != None:
    active_books = search_book


def take_book(book):
    try:
        new_lib.take_book(book)
        st.rerun()
        return {'success': 'knyga paimta sekmingai !'}
    except LookupError as err:
        return {'error': str(err)}
    except ValueError as err:
        return {'error': str(err)}
    except Exception as err:
        return {'error': str(err)}
    # return 'gavau knyga'


for book in active_books:
    container = st.container(border=True)
    col1, col2 = container.columns([3, 1])

    with col1:
        col1.markdown(f':book: **{book.name}**')
        col1.markdown(f"""*Author:* {book.author} | {book.release_year} y.                
Qty: {book.qty} / taken: {len(book.taken_by)}""")

    with col2:
        if col2.button(label="Paimti skaitymui", key=book.uuid,
                       type="secondary", use_container_width=True):
            message = take_book(book)
            if message.get('error'):
                col1.markdown(f':red[{message["error"]}]')
            if message.get('success'):
                col1.markdown(f':green[{message["success"]}]')
