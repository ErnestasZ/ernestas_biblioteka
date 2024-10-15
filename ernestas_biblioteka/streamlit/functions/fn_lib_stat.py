import streamlit as st
from ernestas_biblioteka.classes.consumers.librarian import Librarian
from ernestas_biblioteka.constants import LIB_MIN_AGE


def lib_stat_box(new_lib):
    lib_stat_container = st.container(border=True)
    lib_stat_container.markdown(f"""Sveiki {new_lib.log_consumer.name}.  
                                Jūs sėkmingai prisijungėte prie bibliotekos!""")
    lib_stat_container.subheader('Knygų statistika', divider=True)
    lib_stat_container.markdown(
        f'Vid. skaitytojai pradelsia po {new_lib.get_book_overdue_mean_stat()} kng.')

    lib_stat_container.divider()

    col1, col2 = lib_stat_container.columns(2)

    with col1:
        col1.subheader('***Top 5 populiariausi žanrai***')
        if len(new_lib.most_taken_genre()) < 1:
            col1.markdown('šios informacijos dar nėra')
        else:
            for genre, count in new_lib.most_taken_genre().items():
                col1.markdown(f"""**{genre}**:   
                              paimta {count} kart. """)

    with col2:
        col2.subheader('***Top 5 žanrai pagal aktyvias knygas bibliotekoje***')
        if len(new_lib.most_active_book_genre()) < 1:
            col2.markdown('šios informacijos dar nėra')
        else:
            for genre, count in new_lib.most_active_book_genre().items():
                col2.markdown(f"""**{genre}**:   
                              paimta {count} kart. """)
