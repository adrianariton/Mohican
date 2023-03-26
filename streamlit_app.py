# here is going to be the implementation
# of the deployed app - for now the file
# will be empty for streamlit's setup !!

import streamlit as st
from scraper import get_heuristics
from assembler import run_mohican
import streamlit.components.v1 as components

def my_app():
    url = st.text_input('Enter URL')
    
    option = st.selectbox(
    'What service would you like to use?',
    ('Site Heuristics', 'Generate Ad'))
    st.write('You selected:', option)

    if url:
        if option == "Site Heuristics":
            st.write(get_heuristics(url))
        else:
            run_mohican(url, True)
            p = open("adver.html")
            components.html(p.read())


if __name__ == "__main__":
    my_app()