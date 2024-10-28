import streamlit as st

from ernestas_biblioteka.classes.db_biblioteka import BibliotekaDB
from ernestas_biblioteka.streamlit.db_functions.function import login_user_box
from ernestas_biblioteka.streamlit.db_functions.fn_user_card import user_card_box
from ernestas_biblioteka.streamlit.db_functions.fn_user_search import user_search_book


if 'new_lib_db' not in st.session_state:
    st.session_state["new_lib_db"] = BibliotekaDB()

new_lib_db = st.session_state["new_lib_db"]

st.title('Sveikas skaitytojau')


login_user_box(new_lib_db)

# user card
user_card_box(new_lib_db)

#################################
# active_books = new_lib_db.get_books()

# search active book
search_book = user_search_book(new_lib_db)
if search_book != None:
    active_books = search_book

st.subheader(f"Pasirink knygą iš {len(active_books)}")

# print(active_books[0].title)


def take_book_db(book):
    try:
        new_lib_db.take_book(book)
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
        if not book.is_active:
            col1.markdown(f':bin: **Išimta**')
        col1.markdown(f':book: **{book.title}**')
        col1.markdown(f"""*Author:* {book.author} | {book.release_year} y.   
*{book.genre}*   
Qty: {book.qty} / taken: {book.taken_qty}""")

    with col2:
        if col2.button(label="Paimti skaitymui",  key=f'{book.uuid}_button',
                       type="secondary", use_container_width=True):
            message = take_book_db(book)
            if message.get('error'):
                col1.markdown(f':red[{message["error"]}]')
            if message.get('success'):
                col1.markdown(f':green[{message["success"]}]')
