import streamlit as st
from datetime import datetime, timedelta
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.constants import MAX_TAKEN_BOOKS, BOOK_OVERDUE_DAYS


def user_card_box(new_lib):
    if 'messages' not in st.session_state:
        st.session_state.messages = {}

    # if 'taken_books_session' not in st.session_state:
    #     st.session_state.taken_books_session = {}

    # taken_books_session = st.session_state.taken_books_session

    def return_book(taken_book):
        try:
            new_lib.return_book(taken_book.book)
            st.rerun()
            # taken_books_session.pop(taken_book.book.name)
            # for name, sess_book in taken_books_session.items():
            #     print(sess_book == taken_book.book)
            # print(taken_book in st.session_state.taken_books_session)

            return {'success': 'knyga grąžinta'}
        except LookupError as err:
            return {'error': str(err)}
        except ValueError as err:
            return {'error': str(err)}
        except Exception as err:
            return {'error': str(err)}
        # return True

    if new_lib.log_consumer != None and isinstance(new_lib.log_consumer, User):
        # for taken_book in new_lib.log_consumer.taken_books:
        #     st.session_state.taken_books_session[taken_book.book.name] = taken_book
        user = new_lib.log_consumer
        user_container = st.container(border=True)
        user_container.markdown(f'Daugiausiai galite paimti {MAX_TAKEN_BOOKS}')
        user_container.markdown(
            f"""***{user.name}*** - Nr: {user.user_card.card_number}
    (Paimta: {len(user.taken_books)} knyg)""")
        user_container.divider()

        # for name, taken_book in taken_books_session.items():

        for taken_book in user.taken_books:
            col1, col2 = user_container.columns([3, 1])
            overdue_days = (datetime.now() -
                            taken_book.taken_at).days - BOOK_OVERDUE_DAYS
            with col1:
                col1.markdown(
                    f""":book: **{taken_book.book.name}**  
    *Author:* {taken_book.book.author} | {taken_book.book.release_year} y.  
    {f':red[Knyga uždelsta gražinti {overdue_days} d.]' if overdue_days > 0 else ''}""")
            with col2:
                if col2.button(label="Grąžinti", key=taken_book.book.name,
                               type="primary", use_container_width=True):
                    message = return_book(taken_book)
                    if message.get('error'):
                        col1.markdown(f':red[{message["error"]}]')
                    if message.get('success'):
                        col1.markdown(f':green[{message["success"]}]')
