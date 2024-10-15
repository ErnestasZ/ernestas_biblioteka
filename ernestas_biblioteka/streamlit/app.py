import streamlit as st
# import pandas as pd
import numpy as np

st.title('Sveiki atvyke į biblioteką')
st.markdown(
    "Noredami pradėti prisijunkite kaip *skaitytojas* arba *bibliotekininkas*.")


# if 'sidebar_open' not in st.session_state:
#     st.session_state.sidebar_open = False


# def toggle_sidebar():
#     st.session_state.sidebar_open = not st.session_state.sidebar_open


col1, col2 = st.columns(2)


# if st.session_state.sidebar_open:
#     with st.sidebar:
#         st.title("User Login")
#         st.write("This is the sidebar content triggered by the button.")
#         st.text_input("Username")
#         st.text_input("Password", type="password")
#         st.button("Submit")


# def open_lib_login():
#     st.sidebar.selectbox("Bibliotekininkas", ["A", "B", "C"], key="group")


def open_login_user():
    print('user')


def open_login_lib():
    print('librarian')

# st.markdown("""
#     <style>
#     .stButton > button:first-child {
#         color: white;
#         border-radius: 5px;
#     }
#     .stButton > button:nth-child(1) {
#         background-color: #1E90FF;  /* Blue color for Skaitytojas */
#     }
#     .stButton > button:nth-child(2) {
#         background-color: #32CD32;  /* Green color for Bibliotekininkas */
#     }
#     </style>
# """, unsafe_allow_html=True)

# if st.button("Skaitytojas"):
#     switch_button()

# if st.button("Bibliotekininkas"):
#     switch_button()


with col1:
    st.button(
        label="Skaitytojui",
        type="primary",
        on_click=open_login_user,
        # args=[st.session_state.tweet],
    )

# Button in the second column (Green)
with col2:
    st.button(
        label="Bibliotekininkui",
        type="secondary",
        on_click=open_login_lib,
        # args=[st.session_state.tweet],
    )


# options = st.multiselect(
#     "What are your favorite colors",
#     ["Green", "Yellow", "Red", "Blue"],
#     ["Yellow", "Red"],
# )

# st.write("You selected:", options)


# st.page_link("app.py", label="Home", icon="🏠")
# st.page_link("pages/user.py", label="Skaitytojas", icon="🏠")
# st.page_link("pages/librarian.py", label="Bibliotekininkas", icon="🏠")
# st.page_link("pages/lib/librarian.py", label="Bibliotekininkas", icon="🏠")

genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary"],
    captions=[
        "Laugh out loud.",
        "Get the popcorn.",
        "Never stop learning.",
    ],
)

if genre == ":rainbow[Comedy]":
    st.write("You selected comedy.")
else:
    st.write("You didn't select comedy.")


vertical_alignment = st.selectbox(
    "Vertical alignment", ["top", "center", "bottom"], index=2
)

left, middle, right = st.columns(3, vertical_alignment=vertical_alignment)
left.image("https://static.streamlit.io/examples/cat.jpg")
middle.image("https://static.streamlit.io/examples/dog.jpg")
right.image("https://static.streamlit.io/examples/owl.jpg")
