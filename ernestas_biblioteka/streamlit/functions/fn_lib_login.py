import streamlit as st
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.constants import LIB_MIN_AGE


def login_librarian_box(new_lib):

    if new_lib.log_consumer != None and isinstance(new_lib.log_consumer, Librarian):
        st.markdown(
            "Nepamiršk atsijungti!")

        def logout():
            new_lib.logout()
            st.rerun()

        col_out, col_empt = st.columns([1, 3])
        with col_out:
            if col_out.button(label="Atsijungti", key='logout',
                              type="primary", use_container_width=True):
                message = logout()
                if message and message.get('error'):
                    st.markdown(f':red[{message["error"]}]')

    else:

        def log_lib(name, password):
            try:
                # Onute seacret123
                librarian = new_lib.login_librarian(name, password)
                # st.session_state['log_user'] = user
                st.rerun()
            except LookupError as err:
                return {'error': str(err)}
            except ValueError as err:
                return {'error': str(err)}
            except Exception as err:
                return {'error': str(err)}
        st.markdown(
            "Noredami pradėti darbą, prisijunkite!")
        col_name, col_pass = st.columns(2)
        with col_name:
            name = col_name.text_input(
                "Vardas Pavardė",
                # "pavadinimą arba autorių",
                key="lib_name",
                placeholder="įvesk Vardą ir Pavardę")
        with col_pass:
            password = col_pass.text_input(
                f"Slaptazodis",
                key="lib_password",
                placeholder="įveskite savo slaptažodį")

        if st.button(label="pateikti", key='set_login',
                     type="secondary", use_container_width=True):
            message = log_lib(name, password)
            if message and message.get('error'):
                st.markdown(f':red[{message["error"]}]')
