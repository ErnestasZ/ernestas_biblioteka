import streamlit as st
# from datetime import datetime, timedelta
from ernestas_biblioteka.classes.consumers.user import User
from ernestas_biblioteka.constants import USER_MIN_AGE


def login_user_box(new_lib):

    if 'login_user' not in st.session_state:
        st.session_state["login_user"] = False

    if 'new_user' not in st.session_state:
        st.session_state["new_user"] = False

    if new_lib.log_consumer != None and isinstance(new_lib.log_consumer, User):
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
                # st.session_state['login_user'] = True
    else:
        # pass
        st.markdown(
            "Norėdamas pasiimti knygų prisijunk, arba prisiregistruok kaip naujas")

        def login_user(card_num):
            # 04117872
            # 08577684
            try:
                user = new_lib.login_user(card_num)
                # st.session_state['log_user'] = user
                st.rerun()
            except LookupError as err:
                return {'error': str(err)}
            except ValueError as err:
                return {'error': str(err)}
            except Exception as err:
                return {'error': str(err)}

        col_log, col_new, col_empt = st.columns(3)
        with col_log:
            if col_log.button(label="Prisijungti", key='login',
                              type="primary", use_container_width=True):
                st.session_state['login_user'] = True
                st.session_state['new_user'] = False
        with col_new:
            if col_new.button(label="Naujas sk.", key='add_new',
                              type="secondary", use_container_width=True):
                st.session_state['new_user'] = True
                st.session_state['login_user'] = False

        if st.session_state['login_user']:
            text_input = st.text_input(
                "Korteles nr.",
                # "pavadinimą arba autorių",
                key="login_us",
                placeholder="įvesk kortelės nr. iš 8 skaičių")

            if st.button(label="pateikti", key='set_login',
                         type="secondary", use_container_width=True):
                message = login_user(text_input)
                if message and message.get('error'):
                    st.markdown(f':red[{message["error"]}]')

        def add_user(name, year):
            # 05017450
            try:
                new_user = new_lib.add_user(name, year)
                print(new_user.user_card.card_number)
                login_user(new_user.user_card.card_number)
                # st.session_state['log_user'] = user
                # st.rerun()
                return {'success': new_user}
            except LookupError as err:
                return {'error': str(err)}
            except ValueError as err:
                return {'error': str(err)}
            except Exception as err:
                return {'error': str(err)}

        if st.session_state['new_user']:
            st.subheader('Registracija', divider=True)
            col_name, col_year = st.columns(2)
            with col_name:
                name = col_name.text_input(
                    "Vardas Pavardė",
                    # "pavadinimą arba autorių",
                    key="user_name",
                    placeholder="įvesk Vardą ir Pavardę")
            with col_year:
                year = col_year.text_input(
                    f"Gimimo metai (min {USER_MIN_AGE} m. amžius)",
                    # "pavadinimą arba autorių",
                    key="user_year",
                    placeholder="MMMM")

            if st.button(label="pateikti", key='set_login',
                         type="secondary", use_container_width=True):
                message = add_user(name, year)
                if message and message.get('error'):
                    st.markdown(f':red[{message["error"]}]')
                # if message and message.get('success'):
                #     # print('priregistruoti pavyko', message['success'])
                #     # log_message = login_user(
                #     #     message["success"].user_card.card_number)
                #     if log_message and log_message.get('error'):
                #         st.markdown(f':red[{log_message["error"]}]')
