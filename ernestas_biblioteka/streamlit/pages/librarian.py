import streamlit as st
# from datetime import datetime, timedelta
from ernestas_biblioteka.classes.biblioteka import Biblioteka
from ernestas_biblioteka.streamlit.functions.fn_lib_login import login_librarian_box


if 'new_lib' not in st.session_state:
    st.session_state["new_lib"] = Biblioteka()

new_lib = st.session_state["new_lib"]


st.title('Bibliotekininkams')
